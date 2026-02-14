import json
from pathlib import Path
import random

BODY_TYPE_VISUAL = {
    "thin": "narrow shoulders, long slender torso, slim arms, narrow hips, slender legs",
    "fit": "balanced shoulders, defined waist, visible arm tone, proportional hips, toned legs",
    "athletic": "broad shoulders, muscular upper body, defined arms, medium hips, strong legs",
    "soft": "rounded shoulders, soft torso, gentle waist definition, fuller hips, soft legs"
}

AGE_MORPHOLOGY_VISUAL = {
    "youthful": "full cheeks, smooth luminous skin, minimal under‑eye definition",
    "young_adult": "smooth skin with subtle definition around the eyes and cheeks",
    "adult": "fine lines around the eyes and mouth, reduced cheek fullness",
    "mature": "visible skin texture, deeper nasolabial folds, low soft‑tissue volume"
}


class CharacterIdentity:
    def __init__(
        self,
        height,
        ethnicity,
        gender,
        age,
        body_type,
        skin_tone,
        hair_color,
        hair_texture=None,
        hair_silhouette=None,
        contrast="MEDIUM",
        overrides=None,
        lut_path="LUT",
        mode='default',
        seed=None
    ):

        self.height = height
        self.ethnicity = ethnicity
        self.gender = gender
        self.age = age
        self.body_type = body_type
        self.skin_tone = skin_tone
        self.hair_color = hair_color
        self.hair_texture = hair_texture
        self.hair_silhouette = hair_silhouette

        self.contrast = contrast
        self.overrides = overrides or {}

        # load LUTs
        self.body_lut = self._load_json(Path(lut_path) / "body.json")
        self.gender_ethnicity_lut = self._load_json(Path(lut_path) / "gender_ethnicity.json")
        self.skin_hair_lut = self._load_json(Path(lut_path) / "skin_hair.json")
        self.hair_silhouette_lut = self._load_json(Path(lut_path) / "hair_silhouette.json")
        self.gender_hair = self.hair_silhouette_lut['GENDER_HAIR'][self.gender]
        self.hair_description = self.hair_silhouette_lut["HAIR_DESCRIPTION"]

        self.contrast_lut = self._load_json(Path(lut_path) / "contrast.json")

        # unpack modules
        self.height_data = self.body_lut["HEIGHT"]
        self.body_data = self.body_lut["BODY_TYPE"]
        self.age_data = self.body_lut["AGE_MORPHOLOGY"]

        self.gender_data = self.gender_ethnicity_lut["GENDER_FACE"]
        self.ethnicity_data = self.gender_ethnicity_lut["ETHNICITY_DEFAULTS"]

        self.skin_tone_data = self.skin_hair_lut["SKIN_TONE"]
        self.hair_color_data = self.skin_hair_lut["HAIR_COLOR"]
        self.hair_silhouette_data = self.hair_silhouette_lut["HAIR_SILHOUETTE"]
        self.mode = mode
        self.seed = seed
        self.rng = random.Random(seed) if seed is not None else random

        # resolve final identity block
        self.resolved = self._resolve()

    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _resolve(self):
        merged = {}

        # merge in deterministic order
        merge_order = [
            self.height_data.get(self.height, {}),
            self.ethnicity_data.get(self.ethnicity, {}),
            self.gender_data.get(self.gender, {}),
            self.age_data.get(self.age, {}),
            self.body_data.get(self.body_type, {}),
        ]
        eth = self.ethnicity_data.get(self.ethnicity, {})
        # hair texture from ethnicity unless overridden
        if self.hair_texture is None:
            if "hairTexture" in eth:
                merged["hairTexture"] = eth["hairTexture"]["default"]
        else:
            merged["hairTexture"] = self.hair_texture

        # hair silhouette selection
        if self.hair_silhouette is None:
            if "hairSilhouette" in eth:
                if self.mode == "default":
                    merged["hairSilhouette"] = eth["hairSilhouette"]["default"]
                else:
                    ethnic = set(eth["hairSilhouette"].get("allowed"))
                    gender = set(self.gender_hair['silhouetteBias'])

                    allowed = sorted(ethnic & gender)
                    merged["hairSilhouette"] = self.rng.choice(allowed) if allowed else eth["hairSilhouette"]["default"]
        else:
            merged["hairSilhouette"] = self.hair_silhouette

        # skin tone semantic selection
        if self.skin_tone in self.skin_tone_data:
            merged["skinTone"] = self.skin_tone_data[self.skin_tone][0]

        # hair color semantic selection
        if self.hair_color in self.hair_color_data:
            merged["hairColor"] = self.hair_color_data[self.hair_color][0]
            
        COMPOSITE_FIELDS = {"hairSilhouette"}

        # apply all LUT layers
        for layer in merge_order:
            for key, value in layer.items():
                if key in COMPOSITE_FIELDS:
                    continue
                if isinstance(value, dict):
                    if self.mode == "default":
                        merged[key] = value.get("default")
                    else:
                        allowed = value.get("allowed")
                        if allowed:
                            merged[key] = self.rng.choice(allowed)
                        else:
                            merged[key] = value.get("default")
                else:
                    merged[key] = value

        # apply overrides last
        for key, value in self.overrides.items():
            merged[key] = value

        # melanin contrast layer
        if self.contrast in self.contrast_lut:
            for key, value in self.contrast_lut[self.contrast].items():
                merged[key] = value

        return merged

    def describe_toon(self):
        r = self.resolved
        
        # Format ethnicity for natural language (e.g., "black_african" → "Black African")
        formatted_ethnicity = self.ethnicity.replace('_', ' ').title()
        hair_token = r.get('hairSilhouette', '').replace(' ', '_').replace('-', '_').lower()

        hair_description = self.hair_description.get(hair_token)
        
        return (
            f"Flat-color anime illustration of a young adult feminine {formatted_ethnicity} individual. "
            f"Facial structure: {r['jawlineContour']} jawline, {r['cheekboneHeight']} cheekbones, "
            f"{r['eyeShape']} eyes (monolid, no sparkle), {r['noseBridgeShape']} nasal bridge, {r['noseTipShape']} nose tip. "
            f"Contrast: {r.get('browDensity', 'None')} brows, {r.get('lashDefinition', 'None')} lashes. "
            f"Skin: flat {r['skinTone']} color fill, zero gradients, matte finish. "
            f"Hair: {hair_description} , {r['hairTexture']} texture, {r['hairColor']} color—"
            f"dramatic shape, no strand detail, no glowing highlights. "
            f"Body: slim, 7.5 heads tall, narrow shoulders, long legs, no muscle definition. "
            f"Rendered in strict flat-color anime style: bold black outlines, solid fills only, "
            f"no airbrushing, no cel-shading gradients, no specular reflections."
        )

    def describe_cartoon(self):
        r = self.resolved

        face = (
            f"{r.get('jawlineContour')} jawline, "
            f"{r.get('cheekboneHeight')} cheekbones, "
            f"{r.get('eyeShape')} eyes, "
            f"{r.get('noseBridgeShape')} nasal bridge, "
            f"{r.get('noseTipShape')} nose tip"
        )

        # simplified contrast cues for comic style
        contrast_bits = (
            f"{r.get('browDensity')} brows, "
            f"{r.get('lashDefinition')} lashes"
        )

        # cartoon age morphology (no soft‑tissue realism)
        age = (
            f"stylized {self.age.replace('_', ' ')} features with clean inked contours "
            f"and minimal anatomical shading"
        )

        # cartoon body silhouette (no muscle realism)
        body = (
            f"{BODY_TYPE_VISUAL[self.body_type]}, "
            f"with simplified {r.get('shoulderWidth')} shoulders, "
            f"{r.get('torsoProportion')} torso, "
            f"{r.get('waistDefinition')} waist, "
            f"{r.get('hipWidth')} hips"
        )

        hair = (
            f"{r.get('hairSilhouette')} silhouette, "
            f"{r.get('hairTexture')} texture, "
            f"{r.get('hairColor')} color"
        )

        return (
            f"A {self.age.replace('_', ' ')} {self.gender} presentation "
            f"{self.ethnicity.replace('_', ' ')} individual. "
            f"Facial structure includes a {face}. "
            f"Contrast features include {contrast_bits}. "
            f"Skin tone is {r.get('skinTone')} rendered as flat color. "
            f"Hair has {hair}. "
            f"Age morphology shows {age}. "
            f"Body silhouette is {body}."
        )


    def describe(self):
        r = self.resolved

        face = (
            f"{r.get('jawlineContour')} jawline, "
            f"{r.get('cheekboneHeight')} cheekbones, "
            f"{r.get('eyeShape')} eyes, "
            f"{r.get('noseBridgeShape')} nasal bridge, "
            f"{r.get('noseTipShape')} nose tip"
        )
        contrast_bits = (
            f"{r.get('shadowResponse')} shadow response, "
            f"{r.get('browDensity')} brow density, "
            f"{r.get('lashDefinition')} lash definition"
        )


        # --- AGE ---
        age_visual = AGE_MORPHOLOGY_VISUAL[self.age]
        age_detail = (
            f"{r.get('softTissueVolume')} soft‑tissue volume, "
            f"{r.get('cheekFullness')} cheek fullness, "
            f"{r.get('underEyeDefinition')} under‑eye definition, "
            f"{r.get('nasolabialFoldDepth')} nasolabial fold depth, "
            f"{r.get('skinTexture')} skin texture"
        )

        age = f"{age_visual}, with {age_detail}"

        # --- BODY ---
        body_visual = BODY_TYPE_VISUAL[self.body_type]
        body_detail = (
            f"{r.get('shoulderWidth')} shoulders, "
            f"{r.get('torsoProportion')} torso proportion, "
            f"{r.get('waistDefinition')} waist definition, "
            f"{r.get('hipWidth')} hips, "
            f"{r.get('muscleDefinition')} muscle definition"
        )

        body = f"{body_visual}, with {body_detail}"
        hair_token = r.get('hairSilhouette', '').replace(' ', '_').replace('-', '_').lower()

        hair_description = self.hair_description.get(hair_token)

        hair = (
            f"{hair_description} with "
            f"{r.get('hairTexture')} texture and "
            f"{r.get('hairColor')} color"
        )


        return (
            f"A {self.age.replace('_', ' ')} {self.gender} presentation "
            f"{self.ethnicity.replace('_', ' ')} individual. "
            f"Facial structure includes a {face}. "
            f"Contrast features include {contrast_bits}. "

            f"Skin tone is {r.get('skinTone')}. "
            f"Hair has {hair}. "
            f"Age morphology shows {age}. "
            f"Body silhouette is {body}."
        )
    def to_character_json(self, name=""):
        return {
            "name": name,
            "role": "",
            "biography": "",
            "personality": "",
            "clothingDescription": "",
            "theme": "",
            "setting": "",
            "visualStyle": "",
            "notes": "",
            "characterDescription": self.describe(),
            "characterDescriptionCartoon": self.describe_toon(),
            "height": self.height,
            "ethnicity": self.ethnicity,
            "gender": self.gender,
            "age": self.age,
            "body_type": self.body_type,
            "skin_tone": self.skin_tone,
            "hair_color": self.hair_color,
            "hair_texture": self.hair_texture,
            "hair_silhouette": self.hair_silhouette,
            "identity": self.resolved
        }

    @classmethod
    def from_json(cls, data, lut_path="LUT"):
        return cls(
            height=data["height"],
            ethnicity=data["ethnicity"],
            gender=data["gender"],
            age=data["age"],
            body_type=data["body_type"],
            skin_tone=data["skin_tone"],
            hair_color=data["hair_color"],
            hair_texture=data.get("hair_texture"),
            hair_silhouette=data.get("hair_silhouette"),
            overrides=data.get("identity", {}),
            lut_path=lut_path
    )


def export_characters(*characters):
    return {
        "characters": [char.to_character_json() for char in characters]
    }

    @classmethod
    def from_resolved(cls, data, lut_path="LUT"):
        obj = cls.__new__(cls)  # bypass __init__
        
        # raw semantic fields
        obj.height = data["height"]
        obj.ethnicity = data["ethnicity"]
        obj.gender = data["gender"]
        obj.age = data["age"]
        obj.body_type = data["body_type"]
        obj.skin_tone = data["skin_tone"]
        obj.hair_color = data["hair_color"]
        obj.hair_texture = data.get("hair_texture")
        obj.overrides = {}

        # load LUTs (optional, but harmless)
        obj.body_lut = obj._load_json(Path(lut_path) / "body.json")
        obj.gender_ethnicity_lut = obj._load_json(Path(lut_path) / "gender_ethnicity.json")
        obj.skin_hair_lut = obj._load_json(Path(lut_path) / "skin_hair.json")

        obj.height_data = obj.body_lut["HEIGHT"]
        obj.body_data = obj.body_lut["BODY_TYPE"]
        obj.age_data = obj.body_lut["AGE_MORPHOLOGY"]

        obj.gender_data = obj.gender_ethnicity_lut["GENDER_FACE"]
        obj.ethnicity_data = obj.gender_ethnicity_lut["ETHNICITY_DEFAULTS"]

        obj.skin_tone_data = obj.skin_hair_lut["SKIN_TONE"]
        obj.hair_color_data = obj.skin_hair_lut["HAIR_COLOR"]

        # the important part:
        obj.resolved = data["identity"]

        return obj


class CharacterRegistry:
    def __init__(self):
        self.characters = {}

    def add(self, name, character_identity, clothing_description=""):
        entry = character_identity.to_character_json(name=name)
        entry["clothingDescription"] = clothing_description
        self.characters[name] = entry

    def get(self, name):
        return self.characters.get(name)

    def update_clothing(self, name, clothing_description):
        if name in self.characters:
            self.characters[name]["clothingDescription"] = clothing_description

    def update_description(self, name, new_description):
        if name in self.characters:
            self.characters[name]["characterDescription"] = new_description

    def export(self):
        return {
            "characters": list(self.characters.values())
        }

if __name__ == '__main__':
    from identity_arbitrator import IdentityArbitrator
    from fuzzer_minimal import generate_outfit_sentence

    chaos = CharacterIdentity(
        height="average",
        ethnicity="east_asian",
        gender="feminine",
        age="young_adult",
        body_type="fit",
        skin_tone="light",
        hair_color="blonde",
        contrast="LOW",
        mode='random',
        seed=42
    )

    jade = CharacterIdentity(
        height="average",
        ethnicity="east_asian",
        gender="masculine",
        age="young_adult",
        body_type="fit",
        skin_tone="light",
        hair_color="black",
        contrast="LOW",
        mode='random',
        seed=99
    )

    registry = CharacterRegistry()
    registry.add(
        name="chaos",
        character_identity=chaos,
        clothing_description=generate_outfit_sentence(body_type=chaos.body_type, gender=chaos.gender, theme="professional", seed=chaos.seed)[0]
    )
    registry.add(
        name="Jade",
        character_identity=jade,
        clothing_description=generate_outfit_sentence(body_type=jade.body_type, gender=jade.gender, theme="professional", seed=jade.seed)[0]
    )

    # 🔹 Apply arbitration before export
    arbitrator = IdentityArbitrator()
    registry = arbitrator.apply(registry)

    output = registry.export()
    from json import dump
    with open('characters.json', 'w') as d:
        dump(output, d, indent=4)



