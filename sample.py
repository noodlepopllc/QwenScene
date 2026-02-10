
import sys
sys.path.append('qwenscene')
from character_record import CharacterRecord
from color_translators import translate_hairskin, translate_clothing
from location import LocationColorProfile, LocationLightingProfile, Location

def Bedroom(char1, char2, style):
    lighting = LocationLightingProfile("soft diffused", "a large window", "neutral")
    color = LocationColorProfile("mutedBrown (#8A6A4F) wooden floor", "lightNeutral (#E8E4DA) walls", "mutedBlue: (#4A6FB4) pillows and window curtains")
    location = Location("Bedroom", "a large master bedroom in a luxurious apartment "
     "with a large window on the left wall", lighting, color)
    location.add_detail('A king sized bed is against the left wall under the window its headboard is against the back wall')
    location.add_detail('To the right and left of the headboard are small empty nightstands with nothing on top of them')
    return (f'{style}, \n {location.describe()} \n {char1.name.capitalize()} is {char1.character_description} {char1.describe_clothing_for_shot("mid_torso_up")}.' 
        f'Chaos is laying under a mutedBrown (#8A6A4F) blanket in bed while reading a book, she looks very into the book and is smiling contently. \n'
        f'{char2.name.capitalize()} is {char2.character_description} {char2.describe_clothing_for_shot("mid_torso_up")}.'
        f'Her friend Jade is laying next to her under the same blanket looking at her cell phone with a bored expression.')


def Office(char1, char2, style):
    lighting = LocationLightingProfile("soft diffused", "a large glass exterior wall", "neutral")
    color = LocationColorProfile("desaturatedGreen (#6E7A5F) trees and grass","midNeutral (#B8B6B0) carpeted floor","mutedBrown (#8A6A4F) flat composite wooden desk")
    location = Location("office", "a large office space inside of a large corporate building on the upper floor,"
     "with a back glass wall overlooking a city park", lighting, color)
    location.add_detail("the wooden desk is 4 feet from the back glass wall with an office chair behind it,"
     "the desk faces forward, is on the left side continues out of the frame on the left side")
    location.add_detail("A laptop is on top of the desk on the left side, with the back facing forward")
    location.add_detail("To the right of the desk is a 3 foot wide aisle allowing room to get behind the desk.")

    return f'{style}, \n {location.describe()} \n {char1.name.capitalize()} is {char1.character_description} {char1.describe_clothing_for_shot("mid_torso_up")}. Chaos sits behind the desk working on the laptop, she is laughing like she just heard a very funny joke. \n {char2.name} is {char2.character_description} {char2.describe_clothing_for_shot("full_body")}. Jade stands over her looking at her screen, she is smiling with a joyous expression.'


if __name__ == '__main__':
    from json import load
    # Load Chaos
    with open('characters.json', 'r') as r:
        crec = load(r)

    record_chaos = CharacterRecord.from_json(
        [x for x in crec['characters'] if x['name'] == 'chaos'][0]
    )

    record_jade = CharacterRecord.from_json(
        [x for x in crec['characters'] if x['name'] == 'Jade'][0]
    )
    DEFAULT_STYLE = (
        "9:16 vertical composition")
    DEFAULT_STYLE = (
        "9:16 vertical composition, medium shot, 1980s American comic‑book illustration style with flat cel‑shaded lighting, "
        "bold ink outlines, minimal surface gradients, fixed garment colors with no palette harmonization, "
        "medium shot framing"
    )
    print('#'*5,'OFFICE','#'*5)
    print(Office(record_chaos, record_jade, DEFAULT_STYLE))
    print('#'*5,'BEDROOM','#'*5)
    print(Bedroom(record_chaos, record_jade, DEFAULT_STYLE))
