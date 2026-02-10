import sys
sys.path.append('qwenscene')
from character_record import CharacterRecord
from color_translators import translate_hairskin, translate_clothing
from location import LocationColorProfile, LocationLightingProfile, Location

def describe_char(char, action, shot):
    return (
        f'{char.name.capitalize()} is {char.character_description} {char.describe_clothing_for_shot(shot)}. ' 
        f'{action}'
    )
def BedLeft(char1, char2, style):
    lighting = LocationLightingProfile("sunny lighting", "left", "neutral")
    color = LocationColorProfile("mutedBrown (#8A6A4F) headboard and blanket", "lightNeutral (#E8E4DA) empty back wall", "mutedBlue: (#4A6FB4) pillows)")
    location = Location("A king size bed", "A king size bed on the left side of the room, the right edge continues out of the frame on the right side with mutedBrown blanket lightNeutral under side, 4 mutedBlue pillows",lighting,color)
    return (f'{style} {char1} {char2} {location.describe()} ')

def BedRight(char1, char2, style):
    lighting = LocationLightingProfile("sunny lighting", "left", "neutral")
    color = LocationColorProfile("mutedBrown (#8A6A4F) headboard and blanket", "lightNeutral (#E8E4DA) empty back wall", "mutedBlue: (#4A6FB4) pillows)")
    location = Location("A king size bed", "A king size bed on the left side of the room, the left edge continues out of the frame on the left side with mutedBrown blanket lightNeutral under side, 4 mutedBlue pillows",lighting,color)
    return (f'{style} {char1} {char2} {location.describe()} ')

def Bed(char1, char2, style):
    lighting = LocationLightingProfile("sunny lighting", "left", "neutral")
    color = LocationColorProfile("mutedBrown (#8A6A4F) headboard and blanket", "lightNeutral (#E8E4DA) empty back wall", "mutedBlue: (#4A6FB4) pillows)")
    location = Location("A king size bed", "A king size bed with mutedBrown blanket lightNeutral under side, 4 mutedBlue pillows",lighting,color)
    return (f'{style} {char1} {char2} {location.describe()} ')

def Bedroom(char1, char2, style):
    lighting = LocationLightingProfile("sunny lighting", "a large sliding glass door on the left side", "neutral")
    color = LocationColorProfile("mutedBrown (#8A6A4F) wooden floor", "lightNeutral (#E8E4DA) walls", "mutedBlue: (#4A6FB4) pillows and curtains")
    location = Location("Bedroom", "a large master bedroom in a luxurious apartment "
     "with a large sliding glass door on the left wall", lighting, color)
    location.add_detail(("a wide private balcony directly accessed through the sliding glass door, " 
        "spanning most of the left wall and extending several feet outward, "
        "featuring a minimalist horizontal‑line metal railing with evenly spaced bars, overlooking a park area with a lake. "))
    location.add_detail('A king sized near the sliding glass door its headboard is against the back wall with 4 mutedBlue pillows and a mutedBrown (#8A6A4F) bed covering, lightNeutral (#E8E4DA) underside')
    location.add_detail('Either side of the headboard are small nightstands with simple matching minimalist slender‑stem bedside lamps with lightNeutral (#E8E4DA) lamp shades')
    return (f'{style} {char1} {char2} {location.describe()} ')

def Office(char1, char2, style):
    lighting = LocationLightingProfile("soft diffused", "a large glass exterior wall", "neutral")
    color = LocationColorProfile("desaturatedGreen (#6E7A5F) trees and grass","midNeutral (#B8B6B0) carpeted floor","mutedBrown (#8A6A4F) flat composite wooden desk")
    location = Location("office", "a large office space inside of a large corporate building on the upper floor,"
     "with a back glass wall overlooking a city park", lighting, color)
    location.add_detail("the wooden desk is 4 feet from the back glass wall with an office chair behind it,"
     "the desk faces forward, is on the left side continues out of the frame on the left side")
    location.add_detail("A laptop is on top of the desk on the left side, with the back facing forward")
    location.add_detail("To the right of the desk is a 3 foot wide aisle allowing room to get behind the desk.")
    return (f'{style} {location.describe()} '
        f'{char1}{char2}')

def portrait(char, action):
    description = describe_char(char, action, "shoulders_up")
    return (
        f'an extreme close up shot of {char.name.capitalize()}. {description}'
    )


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
        "9:16 vertical composition, professional interior photography")
    DEFAULT_STYLE = (
        "9:16 vertical composition, 1980s American comic‑book illustration style with flat cel‑shaded lighting, "
        "bold ink outlines, minimal surface gradients, fixed garment colors with no palette harmonization, daytime "
        #"close up shot framing"
        "medium shot framing "
    )
    #DEFAULT_STYLE = ''
    print('#'*5,'OFFICE','#'*5)
    char1_action = "Chaos sits behind the desk working on the laptop, she is laughing like she just heard a very funny joke." 
    char1 = describe_char(record_chaos, char1_action, "mid_torso_up")
    char2_action = 'Jade stands over her looking at her screen, she is smiling with a joyous expression.'
    char2 = describe_char(record_jade, char2_action, "full_body")
    print(Office(char1, char2, DEFAULT_STYLE))
    
    print('#'*5,'BEDROOM 1','#'*5)
    print(Bedroom('', '', DEFAULT_STYLE))

    print('#'*5,'BEDROOM 2','#'*5)
    record_chaos.change_clothing('she is wearing a nightshirt')
    char1_action = "Chaos is reclining under the mutedBrown blanket, absorbed in her book, smiling softly."
    char1 = describe_char(record_chaos, char1_action, 'shoulders_up')
    print(BedLeft(char1, '', DEFAULT_STYLE))
    
    print('#'*5,'BEDROOM 3','#'*5)
    record_jade.change_clothing('she is wearing a camisole with pink bootyshorts')
    char1_action = 'Chaos is laying under a mutedBrown (#8A6A4F) blanket in bed while reading a book, she looks very into the book and is smiling contently.'
    char1 = describe_char(record_chaos, char1_action, 'mid_torso_up')
    char2_action = 'Her friend Jade is walking towards the bed her back to the camera with a cell phone in her left hand.'
    char2 = describe_char(record_jade, char2_action, 'full_body')
    print(Bedroom(char1, char2, DEFAULT_STYLE))
    
    print('#'*5,'BEDROOM 4','#'*5)
    char2_action = 'Her friend Jade is standing next to the bed facing chaos with her hand grabbing the blanket as she prepares to get into bed'
    char2 = describe_char(record_jade, char2_action, 'full_body')
    print(Bedroom(char1, char2, DEFAULT_STYLE))
    
    print('#'*5,'BEDROOM 5','#'*5)
    char2_action = 'Her friend Jade is laying next to her under the same blanket looking at her cell phone with a bored expression.'
    char2 = describe_char(record_jade, char2_action, 'mid_torso_up')
    print(Bedroom(char1, char2, DEFAULT_STYLE))

    print('#'*5,'BEDROOM 6','#'*5)
    char2_action = "Jade is reclining under the mutedBrown blanket, she is looking at her phone, focused expression on her face"
    char2 = describe_char(record_jade, char2_action,'shoulders_up')
    print(BedRight(char1,'',DEFAULT_STYLE))

    print('#'*5,'BEDROOM 7','#'*5)
    char1_action = "Chaos is reclining under the mutedBrown blanket, absorbed in her book, smiling softly."
    char1 = describe_char(record_chaos, char1_action, 'shoulders_up')
    print(Bed(char1, char2, DEFAULT_STYLE))



