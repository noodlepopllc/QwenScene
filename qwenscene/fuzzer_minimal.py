import random

PRONOUNS = ["she", "he", "they"]

COLOR_PALETTES = {
    "LOW":    ["black", "white", "gray", "brown"],
    "MEDIUM": ["black", "white", "gray", "brown", "blue", "green"],
    "HIGH":   ["red", "pink", "orange", "yellow", "green", "blue"]
}

COLOR_HARMONY_SETS = {
    "monochrome_blue": ["navy", "blue", "lightblue"],
    "monochrome_gray": ["black", "gray", "white"],
    "analogous_warm": ["red", "orange", "yellow"],
    "analogous_cool": ["blue", "green", "teal"],
    "complementary_red": ["red", "green", "white"],
    "complementary_blue": ["blue", "orange", "white"],
    "triadic_primary": ["red", "blue", "yellow"],
    "triadic_secondary": ["orange", "green", "purple"]
}


TOPS = ["tshirt", "dress_shirt", "camisole","nightshirt"]
BOTTOMS = ["skirt", "shorts", "pants"]
ONEPIECES = ["catsuit", "dress", "utilitysuit"]
FOOTWEAR = ["boots", "sneakers", "flats"]

ALL_GARMENTS = TOPS + BOTTOMS + ONEPIECES + FOOTWEAR

INDEX_MAP = {
    "top": 0,
    "bottom": 1,
    "footwear": 2,
    "onepiece": 0
}


def choose_harmony_set(rng):
    key = rng.choice(list(COLOR_HARMONY_SETS.keys()))
    return COLOR_HARMONY_SETS[key]

def assign_color(garment, harmony, index_map):
    if garment in TOPS:
        return harmony[index_map["top"] % len(harmony)]
    if garment in BOTTOMS:
        return harmony[index_map["bottom"] % len(harmony)]
    if garment in FOOTWEAR:
        return harmony[index_map["footwear"] % len(harmony)]
    if garment in ONEPIECES:
        return harmony[index_map["onepiece"] % len(harmony)]
    return harmony[0]

# -----------------------------
# Utility
# -----------------------------
def surface(token: str) -> str:
    return token.lower()


def weighted_choice(weight_map, rng):
    population = []
    for item, w in weight_map.items():
        population.extend([item] * w)
    return rng.choice(population)


def choose_color(contrast, rng):
    palette = COLOR_PALETTES.get(contrast, COLOR_PALETTES["MEDIUM"])
    return rng.choice(palette)


# -----------------------------
# Gender / body / theme filters
# -----------------------------
def filter_by_gender(garments, gender):
    if gender == "masculine":
        return [g for g in garments if g not in ["flats","catsuit","nightshirt","skirt", "dress", "camisole"]]
    if gender == "feminine":
        return garments
    return garments  # neutral


def filter_by_body_type(garments, body_type):
    if body_type == "fit" or body_type == "athletic":
        return [g for g in garments if g != "catsuit"]
    if body_type == "thin":
        return garments
    if body_type == "soft":
        return [g for g in garments if g not in ["shorts"]]
    return garments


def filter_by_theme(garments, theme):
    if theme == "professional":
        return [g for g in garments if g not in ["tshirt","sneakers","catsuit","camisole", "nightshirt", "shorts"]]
    if theme == "casual":
        return garments
    if theme == "athletic":
        return [g for g in garments if g in ["sneakers","shorts","pants","tshirt"]]
    return garments


# -----------------------------
# Silhouette-aware garment selection
# -----------------------------
def choose_slot_safe_garments(
    body_type=None,
    gender=None,
    theme=None,
    used_silhouettes=None,
    rng=None
):
    rng = rng or random
    used_silhouettes = used_silhouettes or set()
    garments = []

    # Build filtered garment pools
    def pool(base):
        g = base
        g = filter_by_gender(g, gender)
        g = filter_by_body_type(g, body_type)
        g = filter_by_theme(g, theme)
        return g

    tops = pool(TOPS)
    bottoms = pool(BOTTOMS)
    onepieces = pool(ONEPIECES)
    footwear = pool(FOOTWEAR)

    # 1. One-piece path (33%)
    if rng.random() < 0.33 and onepieces:
        candidates = [g for g in onepieces if g not in used_silhouettes] or onepieces
        onepiece = rng.choice(candidates)
        garments.append(onepiece)
        used_silhouettes.add(onepiece)

        if rng.random() < 0.7 and footwear:
            fw = rng.choice(footwear)
            garments.append(fw)
            used_silhouettes.add(fw)

        return garments, used_silhouettes

    onepieces = []

    # 2. Top + bottom + footwear path
    if rng.random() < 0.95 and tops:
        candidates = [t for t in tops if t not in used_silhouettes] or tops
        top = rng.choice(candidates)
        garments.append(top)
        used_silhouettes.add(top)

    if rng.random() < 0.95 and bottoms:
        candidates = [b for b in bottoms if b not in used_silhouettes] or bottoms
        bottom = rng.choice(candidates)
        garments.append(bottom)
        used_silhouettes.add(bottom)

    if rng.random() < 0.90 and footwear:
        candidates = [f for f in footwear if f not in used_silhouettes] or footwear
        fw = rng.choice(candidates)
        garments.append(fw)
        used_silhouettes.add(fw)

    if not garments:
        fw = rng.choice(footwear or FOOTWEAR)
        garments.append(fw)
        used_silhouettes.add(fw)

    return garments, used_silhouettes


# -----------------------------
# Garment phrase builder
# -----------------------------
def garment_phrase(garment, contrast, rng):
    parts = []

    #if rng.random() < 0.7:
    #    parts.append(surface(choose_color(contrast, rng)))

    global harmony
    color = assign_color(garment, harmony, INDEX_MAP)
    parts.append(color)


    parts.append(surface(garment))
    return " ".join(parts)

global harmony
# -----------------------------
# Final outfit sentence
# -----------------------------
def generate_outfit_sentence(
    name_or_pronoun="she",
    contrast="MEDIUM",
    body_type=None,
    gender=None,
    theme=None,
    used_silhouettes=None,
    seed=None
):
    rng = random.Random(seed) if seed is not None else random
    global harmony
    harmony = choose_harmony_set(rng)
    random.shuffle(harmony)

    garments, used_silhouettes = choose_slot_safe_garments(
        body_type=body_type,
        gender=gender,
        theme=theme,
        used_silhouettes=used_silhouettes,
        rng=rng
    )

    phrases = [garment_phrase(g, contrast, rng) for g in garments]

    if len(phrases) == 1:
        garment_list = phrases[0]
    elif len(phrases) == 2:
        garment_list = " and ".join(phrases)
    else:
        garment_list = ", ".join(phrases[:-1]) + ", and " + phrases[-1]

    return f"{name_or_pronoun} is wearing a {garment_list}", used_silhouettes

if __name__ == '__main__':
    print(generate_outfit_sentence()[0])
