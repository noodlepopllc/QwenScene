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
DEFAULT_STYLE_3D = (
    "stylized 3D animation render, NPR toon shading, flat color regions, "
    "bold black ink outlines, solid flat color fills, zero gradients, "
    "clean volumetric silhouette hair, matte material surfaces, "
    "uniform ambient lighting, neutral color temperature, "
    "stylized anatomical proportions, clean topology, "
    "9:16 vertical composition, full shot, centered vertical alignment, "
    "limited palette, no palette harmonization, fixed garment colors, "
    "porcelain-flat skin tone, clean inked facial contours, "
    "minimal anatomical shading, stylized young adult features, "
    "Blender Eevee toon shader, Unity URP cel-shading, "
    "edge-detection outline pass, flat shading ramp"
)

DEFAULT_STYLE = DEFAULT_STYLE_REAL + "full shot, "

def describe_char_toon(char, action, shot, view='front'):
    description = char.character_description_cartoon
    if view != 'front':
        description = char.remove_face_block(description)

    return (
        f'{char.name.capitalize()} is {description} {char.describe_clothing_for_shot(shot, view)}. '
        f'{action}'
    )

def describe_char_real(char, action, shot, view='front' ):
    description = char.character_description
    if view != 'front':
        description = char.remove_face_block(description)
    return (
        f'{char.name.capitalize()} is {description} {char.describe_clothing_for_shot(shot,view)}. '
        f'{action}'
    )

#renderers = [(DEFAULT_STYLE_TOON, describe_char_toon), (DEFAULT_STYLE_REAL, describe_char_real), (DEFAULT_STYLE_3D, describe_char_real)]
renderers = [(DEFAULT_STYLE_TOON, describe_char_toon), (DEFAULT_STYLE_REAL, describe_char_real)]

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

simple_poses = [
    "She shifts her weight onto one hip, lifts her chin slightly.",
    "She turns her shoulders at a soft angle.",
    "She relaxes her posture, tilts her head gently.",
    "She folds her hands lightly at her waist.",
    "She leans forward.",
    "She softens her shoulders.",
    "She tucks a strand of hair behind her ear.",
]

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

views = [
    'back-view full-back-visible ',
    '3/4-back-view-left', 
    'side-profile-full-left',
    '3/4-front-view-right',
    'front-view-direct, arms behind-the-back pose'
]  

emotion_expressions_toon = [
    "furrowed brows, narrowed almond eyes, tight straight mouth, sharp jaw tension, bold inked frown lines",
    "flared nostrils, clenched jaw, intense glare with lowered brows, angular mouth line, dynamic tension in neck",
    "scowling expression, eyes sharply narrowed, mouth set in hard downward line, bold contour shading on forehead",
    "wide almond eyes with small pupils, raised eyebrows, slightly parted lips, subtle tremble lines at mouth corners",
    "eyes enlarged with highlight dots, eyebrows arched high, mouth open in soft gasp, minimal shading under eyes",
    "startled expression, eyes wide with visible whites, eyebrows lifted, lips parted, flat cel-shaded tension on cheeks",
    "softly furrowed brows, downcast almond eyes, gentle downturn of mouth corners, subtle line between brows",
    "pensieve gaze, eyebrows slightly drawn together, lips pressed lightly, minimal nasolabial emphasis",
    "concerned expression, eyes slightly lowered, brows softly angled inward, mouth neutral with subtle downturn",
    "darting eyes, lightly bitten lower lip, eyebrows uneven, subtle sweat drop icon (comic style), tense shoulder line",
    "glancing sideways, mouth slightly twisted, brows raised on one side, flat-shaded blush marks, minimal gradient",
    "anxious expression, eyes avoiding direct focus, lips pressed thin, faint stress lines at temples, bold ink outlines"
]
realistic_emotion_expressions = [
    # Angry
    " deeply furrowed brows, narrowed eyes with tightened lower lids, compressed lips with slight downward pull, visible tension in jaw and neck muscles, subtle forehead creases. ",
    " flared nostrils, clenched jawline creating sharp masseter definition, intense direct gaze with lowered brow ridge, tight straight mouth with faint vertical lip lines. ",
    " scowling expression with pronounced glabellar lines, eyes narrowed and focused, mouth set in firm downward curve, subtle shadowing under cheekbones from facial tension. ",
    # Scared
    " wide eyes with visible sclera above and below iris, eyebrows raised and drawn together, lips slightly parted with relaxed jaw, subtle tension lines at outer eye corners. ",
    " enlarged pupil size, eyebrows arched high with forehead tension, mouth open in soft gasp showing minimal teeth, slight pallor with subtle under-eye shadowing. ",
    " startled expression with widened eyes and raised upper lids, eyebrows lifted creating horizontal forehead lines, lips parted with relaxed lower face, subtle neck muscle tension. ",
    # Worried
    " softly furrowed brows with gentle medial convergence, downcast eyes with relaxed lower lids, mouth corners slightly downturned with subtle nasolabial emphasis. ",
    " pensieve gaze with eyebrows slightly drawn together creating faint glabellar shadow, lips pressed lightly together showing minimal vermilion, soft tension at temples. ",
    " concerned expression with eyes slightly lowered and inner brows elevated, mouth neutral with subtle downward pull at corners, faint vertical lines between brows. ",
    # Nervous
    " eyes shifting laterally with subtle lid tension, lower lip lightly pressed by upper teeth, eyebrows slightly asymmetrical with gentle raise on one side, faint perspiration at hairline. ",
    " glancing sideways with tightened outer eye muscles, mouth slightly twisted with one corner elevated, brows uneven creating asymmetric forehead lines, subtle flush on cheeks. ",
    " anxious expression with eyes avoiding direct focus showing increased blink rate, lips pressed thin creating faint radial lines, subtle tension in platysma neck muscles. "
]

def EmptyRoom(char, style):
    return f"{style} {char} , background:plain-solid-#FFFFFF flat-fill zero-gradients no-texture no-details no-props no-environment infinite-seamless-backdrop"

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
    characters = [x for x in output['characters']]
    random.shuffle(characters)
    for character in characters:
        for renderer in renderers:
            for view in views:
                record = CharacterRecord.from_json(character)
                pose = random.choice(simple_poses)
                emotion = random.choice(realistic_emotion_expressions)
                facing = 'back' if 'full-back-visible' in view else 'front'
                action = f"{pose} {emotion} {view}" if facing == 'front' else f"She stands idly. {view}"
                x += 1
                print(EmptyRoom(renderer[1](record, action, "full_body", facing), renderer[0]))

