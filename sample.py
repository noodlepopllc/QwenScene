import sys
sys.path.append('qwenscene')
from character_record import CharacterRecord
from color_translators import translate_hairskin, translate_clothing
from location import LocationColorProfile, LocationLightingProfile, Location

'''
def describe_char(char, action, shot, facing='front'):
    description = char.character_description_cartoon
    if facing == 'back':
        description = char.remove_face_block(description)
    return (
        f'{char.name.capitalize()} is {description} {char.describe_clothing_for_shot(shot, facing)}. ' 
        f'{action}'
    )
'''
def describe_char(char, action, shot, facing='front'):
    description = char.character_description
    if facing == 'back':
        description = char.remove_face_block(description)
    return (
        f'{char.name.capitalize()} is {description} {char.describe_clothing_for_shot(shot, facing)}. ' 
        f'{action}'
    )


def BedLeft(char1, char2, style, detail=''):
    #lighting = LocationLightingProfile("sunny lighting", "left", "neutral")
    lighting = LocationLightingProfile("diffuse soft lighting", "left side", "warm")
    color = LocationColorProfile("mutedBrown (#8A6A4F) headboard and blanket",  "mutedBlue: (#4A6FB4) pillows)", "lightNeutral (#E8E4DA) empty back wall")
    location = Location("A king size bed", "A king size bed on the left side of the room, the right edge continues out of the frame on the right side with mutedBrown blanket lightNeutral under side, 4 mutedBlue pillows",lighting,color)
    return (f'{style} {detail} {char1} {"BOTH CHARACTERS AT IDENTICAL SCALE, SAME EYE LEVEL, NO SIZE DIFFERENTIAL. " if char2 else ""} {char2} {location.describe()} ')

def BedRight(char1, char2, style, detail=''):
    #lighting = LocationLightingProfile("sunny lighting", "left", "neutral")
    lighting = LocationLightingProfile("diffuse soft lighting", "left side", "warm")
    color = LocationColorProfile("mutedBlue: (#4A6FB4) pillows)", "mutedBrown (#8A6A4F) headboard and blanket", "lightNeutral (#E8E4DA) empty back wall")
    location = Location("A king size bed", "A king size bed on the left side of the room, the left edge continues out of the frame on the left side with mutedBrown blanket lightNeutral under side, 4 mutedBlue pillows",lighting,color)
    return (f'{style} {detail} {char1} {"BOTH CHARACTERS AT IDENTICAL SCALE, SAME EYE LEVEL, NO SIZE DIFFERENTIAL. " if char2 else ""} {char2} {location.describe()} ')

def Bed(char1, char2, style, detail=''):
    #lighting = LocationLightingProfile("sunny lighting", "left", "neutral")
    lighting = LocationLightingProfile("diffuse soft lighting", "left side", "warm")
    color = LocationColorProfile("mutedBrown (#8A6A4F) headboard and blanket", "mutedBlue (#4A6FB4) pillows", "lightNeutral (#E8E4DA) empty back wall")
    location = Location("A king size bed", "A king size bed on left side of the room, with mutedBrown blanket lightNeutral under side, 4 mutedBlue pillows",lighting,color)
    return (f'{style} {detail} {char1} {char2} {location.describe()} ')

def Bedroom(char1, char2, style, detail=''):
    #lighting = LocationLightingProfile("sunny lighting", "a large sliding glass door on the left side", "neutral")
    lighting = LocationLightingProfile("diffuse soft lighting", "lamps", "warm")
    color = LocationColorProfile("floor in mutedBrown (#8A6A4F)", "lightNeutral (#E8E4DA) empty back wall", "mutedBlue (#4A6FB4) pillows and curtains")
    lighting = LocationLightingProfile("diffuse soft lighting", "lamps", "warm")
    location = Location("Bedroom", "a large master bedroom in a luxurious apartment "
     "with a large sliding glass door on the left wall", lighting, color)
    location.add_detail(("a wide private balcony directly accessed through the sliding glass door, " 
        "spanning most of the left wall and extending several feet outward, "
        "featuring a minimalist horizontal‑line metal railing with evenly spaced bars, overlooking a park area with a lake. "))
    location.add_detail('A king sized near the sliding glass door its headboard is against the back wall with 4 mutedBlue pillows and a mutedBrown (#8A6A4F) bed covering, lightNeutral (#E8E4DA) underside')
    location.add_detail('Either side of the headboard are small nightstands with simple matching minimalist slender‑stem bedside lamps with lightNeutral (#E8E4DA) lamp shades')
    return (f'{style} {detail} {char1} {char2} {location.describe()} ')


def Kitchen(char1, char2, style, detail=''):
    lighting = LocationLightingProfile("diffuse soft lighting", "overhead lights", "warm")
    color = LocationColorProfile("floor in mutedBrown (#8A6A4F)", "lightNeutral (#E8E4DA)", "mutedBlue (#4A6FB4)")
    location = Location("Kitchen", "a modern kitchen ", lighting, color)
    location.add_detail("a large lightNeutral (#E8E4DA) counter with two mutedBlue: (#4A6FB4) stools")
    location.add_detail("in the center of the counter is a large sink")
    location.add_detail("to the right is a sliding glass door leading to a small driveway")
    return (f'{style} {detail} {char1} {char2} {location.describe()} ')

def Office(char1, char2, style):
    #lighting = LocationLightingProfile("soft diffused", "a large glass exterior wall", "neutral")
    lighting = LocationLightingProfile("soft diffused", "overhead lights", "neutral")
    color = LocationColorProfile("desaturatedGreen (#6E7A5F) trees and grass","floor in midNeutral (#B8B6B0)","desk in mutedBrown (#8A6A4F)")
    location = Location("office", "a large office space inside of a large corporate building on the upper floor,"
     "with a back glass wall overlooking a city park", lighting, color)
    location.add_detail("the desk is 4 feet from the back glass wall with an office chair behind it,"
     "the desk faces forward, the left side continues out of the frame on the left")
    location.add_detail("A laptop is on top of the desk on the left side, with the back facing forward")
    location.add_detail("To the right of the desk is a 3 foot wide aisle allowing room to get behind the desk.")
    return (f'{style} {char1} {char2} {location.describe()} ')

def portrait(char, action):
    description = describe_char(char, action, "shoulders_up")
    return (
        f'an extreme close up shot of {char.name.capitalize()}. {description}'
    )


if __name__ == '__main__':
    from character_builder import CharacterIdentity, CharacterRegistry
    from identity_arbitratorV2 import IdentityArbitrator
    from fuzzer_minimal import generate_outfit_sentence

    shawn = CharacterIdentity(
        height="tall",
        ethnicity="south_asian",
        gender="masculine",
        age="adult",
        body_type="fit",
        skin_tone="",
        hair_color="black",
        contrast="LOW",
        mode='random',
        seed=127
    )

    chaos = CharacterIdentity(
        height="average",
        ethnicity="east_asian",
        gender="feminine",
        age="adult",
        body_type="thin",
        skin_tone="",
        hair_color="blonde",
        contrast="LOW",
        mode='random',
        seed=42
    )

    jade = CharacterIdentity(
        height="average",
        ethnicity="east_asian",
        gender="feminine",
        age="young_adult",
        body_type="fit",
        skin_tone="",
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
    registry.add(
        name="Shawn",
        character_identity=shawn,
        clothing_description=generate_outfit_sentence(body_type=shawn.body_type, gender=shawn.gender, theme="professional", seed=shawn.seed)[0]
        )

    # 🔹 Apply arbitration before export
    arbitrator = IdentityArbitrator()
    registry = arbitrator.apply(registry)

    output = registry.export()

    record_chaos = CharacterRecord.from_json(
        [x for x in output['characters'] if x['name'] == 'chaos'][0]
    )

    record_jade = CharacterRecord.from_json(
        [x for x in output['characters'] if x['name'] == 'Jade'][0]
    )

    record_shawn = CharacterRecord.from_json(
        [x for x in output['characters'] if x['name'] == 'Shawn'][0]
    )

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
    DEFAULT_STYLE = DEFAULT_STYLE_REAL + "night time, medium shot, "
    print('#'*5,'OFFICE 1','#'*5)
    record_chaos.change_clothing("she is wearing a red scoop sleeveless mini dress with black flats")
    char1_action = "Chaos sits behind the desk working on the laptop, she is laughing like she just heard a very funny joke." 
    char1 = describe_char(record_chaos, char1_action, "torso_and_feet")
    char2_action = 'Jade stands over Chaos watching her screen, she is smiling with a joyous expression.'
    char2 = describe_char(record_jade, char2_action, "full_body")
    print(Office(char1, char2, DEFAULT_STYLE))

    print('#'*5,'OFFICE 2','#'*5)
    record_shawn.change_clothing("he is wearing a red longsleeve dress_shirt, black pants and boots")
    char1_action = "Chaos sits behind the desk working on the laptop, she looks very uncomfortable, frowning and trying to avoid eye contact." 
    char1 = describe_char(record_chaos, char1_action, "torso_and_feet")
    char2_action = 'Shawn stands over Chaos, he appears to be flirting, laughing at some joke he made.'
    char2 = describe_char(record_shawn, char2_action, "full_body")
    print(Office(char1, char2, DEFAULT_STYLE))
    
    print('#'*5,'BEDROOM 1','#'*5)
    print(Bedroom('', '', DEFAULT_STYLE))

    print('#'*5,'BEDROOM 2','#'*5)
    record_chaos.change_clothing('she is wearing a red tshirt')
    char1_action = "Chaos is reclining against pillows in front of the headboard under the mutedBrown blanket, absorbed in her book, smiling softly."
    char1 = describe_char(record_chaos, char1_action, 'shoulders_up')
    print(BedLeft(char1, '', DEFAULT_STYLE))
    
    print('#'*5,'BEDROOM 3','#'*5)
    record_jade.change_clothing('she is wearing a pink camisole')
    char1_action = 'Chaos is laying on the left side of the bed while reading a book, reclined against some pillows under the blanket.'
    char1 = describe_char(record_chaos, char1_action, 'mid_torso_up')
    char2_action = 'Jade walks to the right side of the bed with her back to the camera facing the other woman.'
    char2 = describe_char(record_jade, char2_action, 'full_body', 'back')
    print(Bedroom(char2, char1, DEFAULT_STYLE)) 
    
    print('#'*5,'BEDROOM 4','#'*5)
    char2_action = 'Jade is standing to the right of the bed, she looks over to chaos as she prepares to get into bed'
    char2 = describe_char(record_jade, char2_action, 'full_body')
    print(Bedroom(char2, char1, DEFAULT_STYLE, detail='wall surface rendered as single uninterrupted flat polygon extending floor-to-ceiling above headboard area, ZERO SURFACE DETAIL, NO ARTWORK, NO SHADOWS, NO TEXTURE VARIATION.'))
    
    print('#'*5,'BEDROOM 5','#'*5)
    char2_action = 'Her friend Jade is laying next to her under the same blanket looking at her cell phone with a bored expression.'
    char2 = describe_char(record_jade, char2_action, 'mid_torso_up')
    print(Bedroom(char1, char2, DEFAULT_STYLE,detail='wall surface rendered as single uninterrupted flat polygon extending floor-to-ceiling above headboard area.'))

    print('#'*5,'BEDROOM 6','#'*5)
    char2_action = "Jade is reclining under the mutedBrown blanket, she is looking at her phone, focused expression on her face"
    char2 = describe_char(record_jade, char2_action,'shoulders_up')
    print(BedRight(char2,'',DEFAULT_STYLE))

    print('#'*5,'BEDROOM 7','#'*5)
    char1_action = "Chaos is reclining against pillows in front of the headboard under the mutedBrown blanket, absorbed in her book, smiling softly."
    char1 = describe_char(record_chaos, char1_action, 'shoulders_up')
    print(Bed(char1, char2, DEFAULT_STYLE))

    print('#'*5,'BEDROOM 8','#'*5)
    print(BedRight(char1,char2,DEFAULT_STYLE,detail='Both women are laying under the blanket side-by-side.'))

    print('#'*5,'BEDROOM 9','#'*5)
    print(BedLeft(char1,char2,DEFAULT_STYLE,detail='Both women are laying under the blanket side-by-side.'))

    print('#'*5,'Kitchen 1','#'*5)
    record_jade.change_clothing('she is wearing an unzipped pink catsuit')
    record_chaos.change_clothing('she is wearing a halfzipped red v_cut leotard')
    char1_action = 'Chaos is pouring a cup of coffee at the counter'
    char1 = describe_char(record_chaos, char1_action, 'mid_torso_up')

    char2_action = 'Jade is sitting at the counter happily enjoying her coffee.'
    char2 = describe_char(record_jade, char2_action, 'full_body')
    print(Kitchen(char1, char2, DEFAULT_STYLE))
