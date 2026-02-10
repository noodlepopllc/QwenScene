from garment_parser import ClothingParser

# -------------------------
# Zone definitions
# -------------------------

ZONE_NAMES = [
    "upper arms",    # 0
    "mid arms",      # 1
    "forearms",      # 2
    "upper torso",   # 3
    "mid torso",     # 4
    "lower torso",   # 5
    "upper thighs",  # 6
    "mid thighs",    # 7
    "lower legs"     # 8
]

# Zone filters for different shot types or caller preferences
ZONE_FILTERS = {
    "shoulders_up":    [0, 3],
    "full_body":       [0,1,2,3,4,5,6,7,8],
    "mid_torso_up":     [0,1,2,3,4],
    "torso_to_feet":   [0,1,2,3,4,5,6,7,8],
    "mid_torso_down":  [4,5,6,7,8],
    "lower_torso_down":[5,6,7,8],
    "thighs_to_feet":  [6,7,8],
    "legs_only":       [6,7,8],
    "none":            [],
    "torso_and_feet":  [0,1,2,3,4,5]
}

# -------------------------
# Coverage merging
# -------------------------

def merge_coverage(garments):
    merged = [0] * 9
    for g in garments:
        merged = [max(a, b) for a, b in zip(merged, g.coverage)]
    return merged

# -------------------------
# Garment visibility
# -------------------------

def garment_is_visible(garment, visible_zones):
    return any(
        garment.coverage[z] == 1
        for z in visible_zones
    )

# -------------------------
# Outfit phrase (filtered)
# -------------------------

def outfit_phrase(garments, visible_zones, zone_filter):
    visible = []

    for g in garments:
        # footwear rule
        if g.slot == "footwear":
            if zone_filter in ["full_body","torso_and_feet"]:
                visible.append(g.name)
            continue

        # normal garment visibility
        if any(g.coverage[z] == 1 for z in visible_zones):
            visible.append(g.name)

    return ", ".join(visible)


# -------------------------
# Exposed skin description
# -------------------------

def exposed_skin(skintone, coverage, visible_zones, garments):
    tone = skintone
    has_footwear = any(g.slot == "footwear" for g in garments)

    exposed = []

    for i in visible_zones:
        if coverage[i] == 0:
            exposed.append(ZONE_NAMES[i])

    if not exposed:
        return None

    return f"{tone} skin visible on the {', '.join(exposed)}"


# -------------------------
# Final character + outfit description
# -------------------------

def describe_character_outfit(pronoun, sentence, zone_filter="full_body"):
    parser = ClothingParser()
    output = parser.parse(sentence)
    garments = output['garments']

    visible_zones = ZONE_FILTERS.get(zone_filter, ZONE_FILTERS["full_body"])
    coverage = merge_coverage(garments)

    clothing = outfit_phrase(garments, visible_zones, zone_filter)
    skin = exposed_skin('bare', coverage, visible_zones, garments)

    if skin:
        return f"{pronoun} is wearing {clothing} with {skin}"
    return f"{pronoun} is wearing {clothing}"


if __name__ == '__main__':
    from character_builder import CharacterIdentity, CharacterRegistry

    jade = CharacterIdentity(
        height="average",
        ethnicity="east_asian",
        gender="feminine",
        age="young_adult",
        body_type="fit",
        skin_tone="light",
        hair_color="black"
    )
    registry = CharacterRegistry()
    registry.add(
        name="Jade",
        character_identity=jade,
        clothing_description="white cotton labcoat, black cotton pants, black leather flats"
    )
    jade2 = registry.get("Jade")
    pronouns = {"feminine": "she", "masculine": "he", "androgynous": "they"}
    pronoun = pronouns[jade2['gender']]
    clothing = f"{pronoun.capitalize()} is wearing a red halter dress and blue leather sneakers."
    clothing = describe_character_outfit(pronoun, clothing)
    print(f"{jade2['characterDescription']} {clothing}.")
