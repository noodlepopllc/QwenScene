from color_translators import translate_hairskin, translate_clothing
from character_outfit import describe_character_outfit
class CharacterRecord:
    def __init__(
        self,
        name,
        gender,
        character_description,
        clothing_description,
    ):
        self.name = name
        self.gender = gender
        self.character_description = translate_hairskin(character_description)
        self.clothing_description = translate_clothing(clothing_description)

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data["name"],
            gender=data["gender"],
            character_description=translate_hairskin(data["characterDescription"]),
            clothing_description=data["clothingDescription"],
        )

    def describe_clothing_for_shot(self, shot_type):
        pronouns = {"feminine": "she", "masculine": "he", "androgynous": "they"}
        pronoun = pronouns[self.gender]
        return translate_clothing(describe_character_outfit(
            pronoun,
            self.clothing_description,
            shot_type
        ))


