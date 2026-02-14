import sys, random
sys.path.append('qwenscene')
from character_record import CharacterRecord
from color_translators import translate_hairskin, translate_clothing
from location import LocationColorProfile, LocationLightingProfile, Location

DEFAULT_STYLE_TOON = (
    "9:16 vertical, flat-color anime illustration: "
    "bold black ink outlines, solid flat color fills only, zero gradients, zero airbrushing. "
    "No eye sparkles, no blush, no glowing skin, no soft shadows. "
    "Hair as solid silhouette—no texture, no luminance variation. "
    "Limited palette, no palette harmonization. "
    "illustration "
)
DEFAULT_STYLE_REAL = (
    "9:16 vertical composition, professional portrait photography, "
    "sharp focus, natural lighting, neutral color balance. "
    "High-fidelity skin texture with accurate subsurface scattering, "
    "realistic fabric detail, natural eye moisture and reflection. "
    "Correct anatomical proportions, symmetrical facial features, "
    "no distortions, no AI artifacts, no plastic or waxy appearance. "
    "Shot on full-frame sensor, 85mm lens, f/2.8 aperture, "
    "soft background separation, no vignetting, no chromatic aberration."
)
DEFAULT_STYLE = DEFAULT_STYLE_REAL + "medium shot, "
'''
def describe_char(char, action, shot):
    return (
        f'{char.name.capitalize()} is {char.character_description_cartoon} {char.describe_clothing_for_shot(shot, "front")}. ' 
        f'{action}'
    )
'''

def describe_char(char, action, shot):
    return (
        f'{char.name.capitalize()} is {char.character_description} {char.describe_clothing_for_shot(shot,"front")}. ' 
        f'{action}'
    )

def PhotoStudio(char):
    lighting = LocationLightingProfile(
        lighting_type="flat cel-shaded lighting",
        lighting_source="ambient non-directional light",
        lighting_temperature="neutral"
    )

    color = LocationColorProfile(
        dominant_60="slateBlue  (#5A6B7A) illustrated water",
        supporting_30="desaturatedTan (#C9B08A) illustrated sand",
        accent_10="mutedGreen (#5A9A6A) illustrated palm trees"
    )

    location = Location(
        "A mostly empty room",
        "the background is a mural of a beach colored in a limited palette illustrated art style",
        lighting,
        color
    )

    return (
        f"{DEFAULT_STYLE} {char} {location.describe()}"
    )

female_names = [
    "Aria", "Lila", "Naomi", "Selene", "Mira",
    "Jade", "Rhea", "Elara", "Talia", "Sienna",
    "Amara", "Nyla", "Keira", "Hana", "Yuna",
    "Mei", "Aiko", "Kaia", "Zara", "Liora",
    "Freya", "Astrid", "Elin", "Sofia", "Lucia",
    "Maren", "Isla", "Clara", "Elise", "Noelle",
    "Brielle", "Camille", "Daphne", "Iris", "Hazel",
    "Rowan", "Quinn", "Mirae", "Jisoo", "Minji",
    "Samira", "Layla", "Farah", "Leila", "Ines",
    "Amaya", "Renata", "Paloma", "Solana", "Nadia"
]

camera_poses = {"feminine": [
    "She shifts her weight onto one hip, lifts her chin slightly, and gives the camera a bright, confident smile.",
    "She turns her shoulders at a soft angle and flashes a warm, inviting grin toward the lens.",
    "She relaxes her posture, tilts her head gently, and offers the camera a poised, graceful smile.",
    "She folds her hands lightly at her waist and meets the lens with a calm, steady expression.",
    "She leans forward a touch, eyes sparkling, and beams at the camera as if sharing an inside joke.",
    "She lifts one hand in a playful gesture and gives the lens a lively, animated smile.",
    "She softens her shoulders, lets a gentle smile bloom, and looks into the camera with warm, open eyes.",
    "She tucks a strand of hair behind her ear and offers the lens a shy, sweet smile.",
    "She angles her body slightly toward the lens, lifts her chin with quiet confidence, and gives the camera a warm, expressive smile."
    ],
    "masculine": [
        "He stands with squared shoulders, weight evenly distributed, and gives the camera a calm, confident look.",
        "He angles his torso slightly, keeps his chin level, and offers a subtle, relaxed smile.",
        "He rests his hands loosely at his sides and meets the lens with steady, self-assured eye contact.",
        "He places one hand in his pocket, shifts his stance naturally, and gives the camera a composed expression.",
        "He crosses his arms comfortably and looks toward the lens with a quiet, confident presence.",
        "He adjusts the cuff of his sleeve, posture straight, and gives the camera a focused, relaxed look.",
        "He leans back slightly on one leg, shoulders relaxed, and offers a small, understated smile.",
        "He clasps his hands loosely in front of him and looks into the camera with a grounded, steady expression.",
        "He stands tall with a neutral stance, chin slightly lowered, and gives the lens a confident, composed look."
    ]
}

ethnicities = ["east_asian", "south_asian", "sub_saharan_african", "middle_eastern", "northern_european", "southern_european","latinx_mestizo"]

DECORATORS = [
    "WORN",
    "DISTRESSED",
    "FRAYED",
    "TORN",
    "TATTERED",
    "SHREDDED",
    "BURNT",
    "SCORCHED",
    "WEATHERED",
    "DIRTY",
    "MUDDY",
    "WET",
    "PATCHED",
    "FADED"
]

outfits = [
    "she is wearing {first} cropped tshirt, {second} bootyshorts, {third} sneakers",
    "she is wearing {first} scoop sleeveless mini dress, {second} flats",
    "she is wearing {first} cropped camisole, {second} mini skirt, tall black boots",
    "she is wearing {first} {decorator} halter mini dress, tall black boots",
    "she is wearing {first} {decorator} cropped tshirt, {second} {decorator} pants, {third} sneakers"
]

COLOR_HARMONY_SETS = [
    ["navy", "blue", "lightblue"],
    ["black", "gray", "white"],
    ["red", "orange", "yellow"],
    ["blue", "green", "teal"],
    ["red", "green", "white"],
    ["blue", "orange", "white"],
    ["red", "blue", "yellow"],
    ["orange", "green", "purple"]
]

def outfit(decorators=True):
    colors = random.choice(COLOR_HARMONY_SETS)
    random.shuffle(colors)
    decor = random.choice(DECORATORS) if decorators else ''
    outfit = random.choice(outfits)
    return outfit.format(first=colors[0],second=colors[1],third=[colors[2]],decorator=decor)

if __name__ == '__main__':
    from character_builder import CharacterIdentity, CharacterRegistry
    from identity_arbitrator import IdentityArbitrator
    from fuzzer_minimal import generate_outfit_sentence

    seed = 666
    professional = generate_outfit_sentence(body_type="soft", gender="masculine", theme="professional",seed=seed)[0]
    athletic = generate_outfit_sentence(body_type="fit", gender="masculine", theme="athletic",seed=seed)[0]
    casual = generate_outfit_sentence(body_type="fit", gender="masculine", theme="casual",seed=seed)[0]

    hair_color = ["black","blonde","brown","red"]

    registry = CharacterRegistry()
    x = 0
    for name in female_names:
        age = ('young_adult','thin', generate_outfit_sentence(body_type="thin", gender="feminine", theme="sexy")[0])
        registry.add(
            name=name,
            character_identity=CharacterIdentity(
                height='average',
                ethnicity=ethnicities[x%len(ethnicities)],
                gender='feminine',
                skin_tone="",
                age=age[0],
                body_type=age[1],
                hair_color=random.choice(hair_color),
                contrast='low',
                mode='random'
            ),
            clothing_description=outfit()
        )
        x += 1

    # 🔹 Apply arbitration before export
    arbitrator = IdentityArbitrator()
    registry = arbitrator.apply(registry)

    output = registry.export()
    x = 0
    for character in output['characters']:
        record = CharacterRecord.from_json(character)
        action = camera_poses[record.gender][x % len(camera_poses[record.gender])]
        x += 1
        print(PhotoStudio(describe_char(record, action, "full_body")))

