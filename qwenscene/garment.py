
STYLE_ZONE_MAP = [
    ("HALTER","SCOOP","V_CUT","CREW","NORMAL"),
    ("SLEEVELESS","SHORT_SLEEVE","LONG_SLEEVE"),
    ("MINI","MIDI","MAXI"),
    ("CROPPED"),
    ("ZIPPED","HALFZIPPED","UNZIPPED")
]

def get_zone(val):
    for zone in range(len(STYLE_ZONE_MAP)):
        if val in STYLE_ZONE_MAP[zone]:
            return zone

class Garment:
    def __init__(self, slot, base, subtype):
        # structural from slot
        self.slot = subtype['slot']
        self.coverage = slot["default_coverage"][:]
        self.zipper_state = slot.get("zipper_state", "na")
        self.zipper_exposed = slot.get("zipper_exposed", False)
        self.allowed_styles = slot.get("allowed_styles", [])

        # structural overrides from base
        if "default_coverage" in base:
            self.coverage = self._merge(self.coverage, base["default_coverage"])
        if "zipper_state" in base:
            self.zipper_state = base["zipper_state"]
        if "zipper_exposed" in base:
            self.zipper_exposed = base["zipper_exposed"]
        if "allowed_styles_override" in base:
            self.allowed_styles = base["allowed_styles_override"]

        # visual defaults from subtype
        self.vocab = subtype["vocab"]
        self.name = subtype["name"]
        self.garment_type = subtype["garment_type"]

        self.material = subtype.get("default_material","cotton")
        self.pattern = subtype.get("default_pattern","solid")
        self.primary_color_hex = subtype["default_primary_color_hex"]
        self.style_tokens = [subtype["default_style"]]
        self.neckline = subtype.get("default_neckline","na")

        self.decorators = []

    def _merge(self, base, mask):
        out = base[:]
        for i, v in enumerate(mask):
            if v is not None:
                out[i] = v
        return out

    def __str__(self):
        cov = "".join(str(c) for c in self.coverage)
        dec = ", ".join(self.decorators) if self.decorators else "none"
        styles = ", ".join(self.style_tokens)

        return (
            f"Garment(\n"
            f"  vocab='{self.vocab}', name='{self.name}', type='{self.garment_type}', slot='{self.slot}',\n"
            f"  material='{self.material}', pattern='{self.pattern}', color='{self.primary_color_hex}',\n"
            f"  neckline='{self.neckline}', styles=[{styles}], decorators=[{dec}],\n"
            f"  zipper_state='{self.zipper_state}', zipper_exposed={self.zipper_exposed},\n"
            f"  coverage={cov}\n"
            f")"
        )



