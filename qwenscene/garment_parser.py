import json
from pathlib import Path
from garment import Garment, get_zone

class ColorMaterialResolver:
    def __init__(self, lut):
        self.lut = lut

        # Pre-split LUT keys
        self.rgb_map = {k.split(":")[1]: v for k, v in lut.items() if k.startswith("rgb:")}
        self.brightness_map = {k.split(":")[1]: v for k, v in lut.items() if k.startswith("brightness:")}
        self.material_sat_map = {k.split(":")[1]: v for k, v in lut.items() if k.startswith("material_sat:")}
        self.pattern_map = {k.split(":")[1]: v for k, v in lut.items() if k.startswith("pattern:")}

    def resolve_color(self, color_tokens, material_tokens, brightness_tokens, default_hex):
        hue = None
        brightness = None
        material = None

        for t in color_tokens:
            if t in self.rgb_map:
                hue = t
            if t in self.brightness_map:
                brightness = t

        for t in material_tokens:
            if t in self.material_sat_map:
                material = t

        # choose base hue: explicit or default
        if hue:
            base_r, base_g, base_b = self.rgb_map[hue]
        else:
            base_r = int(default_hex[1:3], 16)
            base_g = int(default_hex[3:5], 16)
            base_b = int(default_hex[5:7], 16)

        # brightness only applies if hue exists
        b_mult = self.brightness_map.get(brightness, 1.0) if hue else 1.0

        # material always applies
        m_mult = self.material_sat_map.get(material, 1.0)

        r = int(base_r * b_mult * m_mult)
        g = int(base_g * b_mult * m_mult)
        b = int(base_b * b_mult * m_mult)

        if "white" in color_tokens:
            return "#FFFFFF"

        return "#{:02X}{:02X}{:02X}".format(r, g, b)


    def resolve_material(self, tokens):
        for t in tokens:
            if t in self.material_sat_map:
                return t
        return None

    def resolve_pattern(self, tokens):
        for t in tokens:
            if t in self.pattern_map:
                return t
        return "solid"

class ClothingParser:
    GENDER_TOKENS = ["he", "she", "they"]

    def __init__(self, lut_path="LUT"):
        # Load LUTs
        self.garment_types = self._load(Path(lut_path) / "garment_types.json")
        self.garments = self._load(Path(lut_path) / "comic_clothingV2.json")
        self.modifiers = self._load(Path(lut_path) / "garment_modifiers.json")
        self.color_material_lut = self._load(Path(lut_path) / "comic_materialV2.json")
        self.slots = self._load(Path(lut_path) / "slot_templates.json")

        # Color/material resolver
        self.cm = ColorMaterialResolver(self.color_material_lut)

        # Build lookup sets
        self.garment_set = set([x.lower() for x in self.garments.keys()])

        self.modifier_set = set()
        for group in ["SILHOUETTE", "NECKLINES", "ZIPPERS"]:
            if group in self.modifiers:
                self.modifier_set.update(k.lower() for k in self.modifiers[group].keys())
        if "DECORATORS" in self.modifiers:
            self.modifier_set.update(d.lower() for d in self.modifiers["DECORATORS"])

        # Color/material/pattern tokens
        self.color_tokens = set(k.split(":")[1] for k in self.color_material_lut if k.startswith("rgb:"))
        self.brightness_tokens = set(k.split(":")[1] for k in self.color_material_lut if k.startswith("brightness:"))
        self.material_tokens = set(k.split(":")[1] for k in self.color_material_lut if k.startswith("material_sat:"))
        self.pattern_tokens = set(k.split(":")[1] for k in self.color_material_lut if k.startswith("pattern:"))

        # Allowed tokens
        self.allowed = (
            self.garment_set |
            self.modifier_set |
            self.color_tokens |
            self.brightness_tokens |
            self.material_tokens |
            self.pattern_tokens |
            set(self.GENDER_TOKENS)
        )
    
    def make_garment(self, subtype_name):
        subtype = self.garments[subtype_name.upper()]
        base = self.garment_types[subtype["garment_type"]]
        slot = self.slots[subtype["slot"]]
        return Garment(slot, base, subtype)

    def _load(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def normalize(self, text):
        text = text.lower()
        out = []
        for c in text:
            o = ord(c)
            if (97 <= o <= 122) or o in (32, 95):
                out.append(c)
        return ''.join(out)

    def tokenize(self, text):
        text = text.replace(",", " , ")
        return text.split()

    def filter_tokens(self, tokens):
        return [t for t in tokens if t in self.allowed]

    def parse(self, text):
        norm = self.normalize(text)
        tokens = self.tokenize(norm)
        tokens = self.filter_tokens(tokens)

        # Extract gender
        gender_token = next((t for t in tokens if t in self.GENDER_TOKENS), None)
        gender = {"he": "male", "she": "female", "they": "neutral"}.get(gender_token, "neutral")

        # Remove gender tokens
        tokens = [t for t in tokens if t not in self.GENDER_TOKENS]

        garments = []
        current = {
            "garment": '',
            "modifiers": [],
            "colors": [],
            "materials": [],
            "patterns": []
        }

        for tok in tokens:

            # Garment type
            if tok in self.garment_set:
                if current:
                    current['garment'] = tok
                    garments.append(self._finalize(current))
                current = {
                    "garment": '',
                    "modifiers": [],
                    "colors": [],
                    "materials": [],
                    "patterns": []
                }
                continue

            # Modifiers
            if tok in self.modifier_set and current:
                current["modifiers"].append(tok)
                continue

            # Colors
            if tok in self.color_tokens and current:
                current["colors"].append(tok)
                continue

            # Brightness
            if tok in self.brightness_tokens and current:
                current["colors"].append(tok)
                continue

            # Materials
            if tok in self.material_tokens and current:
                current["materials"].append(tok)
                continue

            # Patterns
            if tok in self.pattern_tokens and current:
                current["patterns"].append(tok)
                continue

        return {
            "gender": gender,
            "garments": garments,
            "tokens": tokens
        }

    def _finalize(self, parsed):
        garment = self.make_garment(parsed["garment"])

        default_style = garment.style_tokens[0] if len(garment.style_tokens) > 0 else None
        garment.style_tokens = []
        default_zone = None
        if default_style:
            default_zone = get_zone(default_style)

        # structural modifiers
        for m in parsed["modifiers"]:
            if get_zone(m) == default_zone:
                default_style = None
            self.apply_structural_modifier(garment, m)
        if default_style:
            self.apply_structural_modifier(garment,default_style)

        # visual modifiers
        self.apply_visual_modifiers(garment, parsed)

        # final naming
        self.apply_name(garment)

        return garment

    def apply_structural_modifier(self, garment, m):
        M = m.upper()

        if M in self.modifiers["SILHOUETTE"]:
            mask = self.modifiers["SILHOUETTE"][M]["coverage"]
            garment.coverage = garment._merge(garment.coverage, mask)
            if M not in garment.style_tokens:
                garment.style_tokens.append(M)

        if M in self.modifiers["NECKLINES"]:
            mask = self.modifiers["NECKLINES"][M]["coverage"]
            garment.coverage = garment._merge(garment.coverage, mask)
            garment.neckline = M

        if M in self.modifiers["ZIPPERS"]:
            z = self.modifiers["ZIPPERS"][M]
            if "zipper_state" in z:
                garment.zipper_state = z["zipper_state"]
            if "zipper_exposed" in z:
                garment.zipper_exposed = z["zipper_exposed"]

        if M in self.modifiers["DECORATORS"]:
            garment.decorators.append(M)

    def apply_visual_modifiers(self, garment, parsed):
        color_tokens = parsed["colors"]
        material_tokens = parsed["materials"]
        if len(material_tokens) == 0:
            material_tokens.append(garment.material)
        pattern_tokens = parsed["patterns"]

        garment.primary_color_hex = self.cm.resolve_color(
            color_tokens=color_tokens,
            material_tokens=material_tokens,
            brightness_tokens=color_tokens,
            default_hex=garment.primary_color_hex
        )

        mat = self.cm.resolve_material(material_tokens)
        if mat:
            garment.material = mat

        garment.pattern = self.cm.resolve_pattern(pattern_tokens)
    
    def apply_name(self, garment):
        parts = []

        # color always first
        parts.append(garment.primary_color_hex)

        # pattern (skip solid)
        if garment.pattern != "solid":
            parts.append(garment.pattern)

        if len(garment.decorators) > 0:
            parts.append(garment.decorators[0].lower())

        if garment.zipper_state != 'na' and (garment.zipper_exposed == True or garment.zipper_state != 'closed'):
            parts.append(garment.zipper_state)
            parts.append('exposed zipper' if garment.zipper_exposed else '')
        
        # sleeve style (tops + onepiece only)
        if garment.slot in ("top"):
            for s in garment.style_tokens:
                if s in ("CROPPED"):
                    parts.append(s.lower().replace("_", " "))
                    break

        # sleeve style (tops + onepiece only)
        if garment.slot in ("top", "onepiece"):
            for s in garment.style_tokens:
                if s in ("SLEEVELESS", "SHORT_SLEEVE", "LONG_SLEEVE"):
                    parts.append(s.lower().replace("_", " "))
                    break

        # skirt/dress length (onepiece only)
        if garment.slot == "onepiece":
            for s in garment.style_tokens:
                if s in ("MINI", "MIDI", "MAXI"):
                    parts.append(s.lower())
                    break

        # neckline (tops + onepiece only, skip 'na')
        if garment.slot in ("top", "onepiece") and garment.neckline not in ("na", "STANDARD", "NORMAL"):
            parts.append(garment.neckline.lower().replace("_", "-"))

        # footwear height (footwear only)
        if garment.slot == "footwear":
            for s in garment.style_tokens:
                if s in ("LOW", "MID", "HIGH", "TALL"):
                    parts.append(s.lower())
                    break

        # vocab last
        parts.append(garment.name)

        garment.name = " ".join(parts)

if __name__ == '__main__':
    parser = ClothingParser()
    clothing = "she is wearing a mini sleeveless scoop tattered dress with brown synthetic flats"
    output = parser.parse(clothing)
    print(clothing)
    print(output['garments'][0])
    #print(output['garments'])
