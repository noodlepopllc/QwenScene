import json, copy
from pathlib import Path

class IdentityArbitrator:
    def __init__(self, variant_lut=None, lut_path="LUT"):
        # variant_lut lets you control how we "nudge" collisions
        # If None, we use simple hardcoded alternates.

        self.variant_lut = variant_lut or {
            "jawlineContour": ["soft", "oval", "angular", "square", "heart"],
            "cheekboneHeight": ["low", "mid", "high"],
            "eyeShape": ["monolid", "almond", "round", "hooded"],
            "noseBridgeShape": ["low", "low-mid", "mid", "high"],
            "shadowResponse": ["soft", "medium", "sharp"],
            "browDensity": ["sparse", "medium", "dense"],
            "lashDefinition": ["soft", "medium", "sharp"],
            "hairTexture": ["straight", "wavy", "curly"],
            "hairColor": ["black", "dark-brown", "brown", "blonde", "red"]
        }

        # fields we consider for collision
        self.anchor_fields = [
            "jawlineContour",
            "cheekboneHeight",
            "eyeShape",
            "noseBridgeShape",
            "shadowResponse",
            "browDensity",
            "lashDefinition",
            "hairTexture",
            "hairColor",
        ]
        self.lut_path = Path(lut_path)

        # Load ethnicity LUT (needed for silhouette allowed lists)
        gender_ethnicity = self._load_json(self.lut_path / "gender_ethnicity.json")
        self.ethnicity_lut = gender_ethnicity["ETHNICITY_DEFAULTS"]
        self.hair_silhouette_lut = self._load_json(Path(lut_path) / "hair_silhouette.json")
        self.gender_hair = self.hair_silhouette_lut['GENDER_HAIR']

    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)
        

    def enforce_hair_silhouette_diversity(self, registry):
        """
        Ensures no two characters with the same (ethnicity, gender, age)
        share the same hairSilhouette. If a collision occurs, pick a new
        silhouette from the ethnicity's allowed list.
        """

        used = {}  # (ethnicity, gender, age) → set of silhouettes

        for name, entry in registry.characters.items():
            ident = entry["identity"]
            eth = entry["ethnicity"]
            gen = entry["gender"]
            age = entry["age"]
            gender_hair = self.hair_silhouette_lut['GENDER_HAIR'][gen]["silhouetteBias"]
            hair_allowed = sorted(set(gender_hair) & set(self.ethnicity_lut[eth]["hairSilhouette"]["allowed"]))
            silhouette = ident.get("hairSilhouette")
            
            if silhouette is None:
                continue

            key = (eth, gen, age)

            # initialize bucket
            if key not in used:
                used[key] = {silhouette}
                continue

            # no conflict
            if silhouette not in used[key]:
                used[key].add(silhouette)
                continue

            # conflict → resolve
            allowed = (
                self.ethnicity_lut
                .get(eth, {})
                .get("hairSilhouette", {})
                .get("allowed", [])
            )

            # try to find an unused silhouette
            replacement = None
            for alt in allowed:
                if alt not in used[key]:
                    replacement = alt
                    break

            # fallback: deterministic hash-based selection
            if replacement is None and allowed:
                idx = abs(hash(name)) % len(allowed)
                replacement = allowed[idx]

            # apply replacement if found
            if replacement:
                ident["hairSilhouette"] = replacement
                used[key].add(replacement)


    def apply(self, registry):
        """
        Mutates registry.characters in-place to ensure
        group-level divergence of identity anchors.
        """
        chars = registry.characters  # {name: entry}
        names = list(chars.keys())

        # track used combinations to avoid exact duplicates
        used_signatures = {}

        for name in names:
            entry = chars[name]
            identity = entry.get("identity", {})
            signature = self._signature(identity)

            # if signature is unique, claim it
            if signature not in used_signatures:
                used_signatures[signature] = name
                continue

            # collision: adjust this character's anchors
            adjusted_identity = self._resolve_collision(identity, used_signatures)
            entry["identity"] = adjusted_identity

            # update signature map
            new_signature = self._signature(adjusted_identity)
            used_signatures[new_signature] = name
        
        self.enforce_hair_silhouette_diversity(registry)

        return registry

    def _signature(self, identity):
        """
        Build a tuple of anchor values for collision detection.
        Missing fields become None.
        """
        return tuple(identity.get(f) for f in self.anchor_fields)

    def _resolve_collision(self, identity, used_signatures):
        """
        Given an identity that collides, nudge its anchors until
        we get a unique signature.
        """
        identity = copy.deepcopy(identity)

        # try to adjust one field at a time in a stable order
        for field in self.anchor_fields:
            current = identity.get(field)
            variants = self.variant_lut.get(field, [])

            if not variants or current not in variants:
                continue

            # pick the next variant in the list (cyclic)
            idx = variants.index(current)
            for offset in range(1, len(variants)):
                candidate = variants[(idx + offset) % len(variants)]
                identity[field] = candidate
                sig = self._signature(identity)
                if sig not in used_signatures:
                    return identity

            # if we can't find a unique variant for this field, revert and move on
            identity[field] = current


        # if we somehow can't resolve, just return the last attempt
        return identity
