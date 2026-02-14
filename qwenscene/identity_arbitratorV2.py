import json
import copy
from pathlib import Path
from collections import deque
import random

class IdentityArbitrator:
    def __init__(self, variant_lut=None, lut_path="LUT"):
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

        self.anchor_fields = [
            "jawlineContour", "cheekboneHeight", "eyeShape", "noseBridgeShape",
            "shadowResponse", "browDensity", "lashDefinition", "hairTexture", "hairColor"
        ]
        
        self.lut_path = Path(lut_path)
        gender_ethnicity = self._load_json(self.lut_path / "gender_ethnicity.json")
        self.ethnicity_lut = gender_ethnicity["ETHNICITY_DEFAULTS"]
        self.hair_silhouette_lut = self._load_json(self.lut_path / "hair_silhouette.json")
        self.gender_hair_lut = self.hair_silhouette_lut["GENDER_HAIR"]
        
        # 🔹 PRECOMPUTE BASE POOLS ONCE AT INIT
        self.base_pools = self._build_base_pools()

    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _build_base_pools(self):
        """Build (ethnicity, gender) → list of VALID silhouettes (ethnicity ∩ gender)"""
        pools = {}
        for eth_key, eth_data in self.ethnicity_lut.items():
            ethnic_allowed = eth_data.get("hairSilhouette", {}).get("allowed", [])
            if not ethnic_allowed:
                continue
            
            for gen_key, gen_data in self.gender_hair_lut.items():
                gender_bias = gen_data.get("silhouetteBias", [])
                if not gender_bias:
                    continue
                
                # TRUE valid set = intersection, sorted for determinism
                valid = sorted(set(ethnic_allowed) & set(gender_bias))
                if valid:
                    pools[(eth_key, gen_key)] = valid
        return pools

    def enforce_hair_silhouette_diversity(self, registry):
        """
        Rotating pool allocator:
        - Each (ethnicity, gender, age) bucket gets its own depletion pool
        - Assign silhouettes FIFO from shuffled pool
        - When pool empties → refill with fresh shuffled copy
        - Guarantees distinctness for N ≤ pool size
        """
        from collections import deque
        
        # Bucket state: key → {pool: deque, rng: Random}
        bucket_state = {}
        
        # Process characters in DETERMINISTIC ORDER (by name)
        for name in sorted(registry.characters.keys()):
            entry = registry.characters[name]
            ident = entry["identity"]
            eth = entry["ethnicity"]
            gen = entry["gender"]
            age = entry["age"]
            key = (eth, gen, age)  # Bucket key
            
            # ── Initialize bucket on first encounter ──
            if key not in bucket_state:
                # Get base pool for (ethnicity, gender)
                base_pool = self.base_pools.get((eth, gen), [])
                
                # Fallback: ethnicity-only if no intersection exists
                if not base_pool:
                    base_pool = sorted(
                        self.ethnicity_lut
                        .get(eth, {})
                        .get("hairSilhouette", {})
                        .get("allowed", [])
                    )
                
                # Deterministic RNG per bucket (seeded by bucket key)
                bucket_seed = hash(key) & 0xFFFFFFFF
                rng = random.Random(bucket_seed)
                
                # Initial shuffle for natural distribution
                shuffled = base_pool.copy()
                rng.shuffle(shuffled)
                
                bucket_state[key] = {
                    "pool": deque(shuffled),
                    "rng": rng,
                    "base_pool": base_pool
                }
            
            # ── Assign silhouette ──
            state = bucket_state[key]
            pool = state["pool"]
            current = ident.get("hairSilhouette")
            
            # If current silhouette is available → claim it (preserves intentional assignments)
            if current in pool:
                pool.remove(current)
                continue
            
            # Pool exhausted? Refill with fresh shuffled copy
            if not pool:
                refill = state["base_pool"].copy()
                state["rng"].shuffle(refill)
                pool.extend(refill)
                state["pool"] = pool  # update reference
            
            # Assign next available silhouette (FIFO)
            replacement = pool.popleft()
            ident["hairSilhouette"] = replacement

    def apply(self, registry):
        """
        Main arbitration pass:
        1. Resolve facial anchor collisions (prevent identical faces)
        2. Enforce hair silhouette diversity (rotating pools)
        """
        # ── Step 1: Facial anchor collision resolution ──
        used_signatures = {}
        for name in sorted(registry.characters.keys()):  # deterministic order
            entry = registry.characters[name]
            identity = entry.get("identity", {})
            signature = self._signature(identity)
            
            if signature not in used_signatures:
                used_signatures[signature] = name
                continue
            
            # Collision → nudge anchors until unique
            adjusted = self._resolve_collision(identity, used_signatures)
            entry["identity"] = adjusted
            used_signatures[self._signature(adjusted)] = name
        
        # ── Step 2: Hair silhouette diversity (rotating pools) ──
        self.enforce_hair_silhouette_diversity(registry)
        
        return registry

    def _signature(self, identity):
        """Tuple of anchor values for collision detection"""
        return tuple(identity.get(f) for f in self.anchor_fields)

    def _resolve_collision(self, identity, used_signatures):
        """Nudge one anchor field at a time until signature is unique"""
        identity = copy.deepcopy(identity)
        
        for field in self.anchor_fields:
            current = identity.get(field)
            variants = self.variant_lut.get(field, [])
            
            if not variants or current not in variants:
                continue
            
            # Try next variants in cyclic order
            idx = variants.index(current)
            for offset in range(1, len(variants)):
                candidate = variants[(idx + offset) % len(variants)]
                identity[field] = candidate
                if self._signature(identity) not in used_signatures:
                    return identity
            
            # Revert if no unique variant found for this field
            identity[field] = current
        
        return identity  # best-effort (may still collide if space exhausted)