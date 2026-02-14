from color_translators import translate_hairskin, translate_clothing
from character_outfit import describe_character_outfit
class CharacterRecord:
    def __init__(
        self,
        name,
        gender,
        character_description,
        clothing_description,
        character_description_cartoon
    ):
        self.name = name
        self.gender = gender
        self.character_description = translate_hairskin(character_description)
        self.clothing_description = translate_clothing(clothing_description)
        self.character_description_cartoon = translate_hairskin(character_description_cartoon)

    def remove_face_block(self, desc: str) -> str:
        """Remove full facial description block (structure + contrast) for back views"""
        start = "Facial structure"
        start_idx = desc.find(start)
        if start_idx == -1:
            return desc  # no face block → return as-is
        
        # Find NEXT semantic marker after start (works for both styles)
        # Toon ends before "Hair: ", realistic ends before "Skin tone is "
        end_markers = ["Hair: ", "Skin tone is "]
        end_idx = -1
        for marker in end_markers:
            idx = desc.find(marker, start_idx)
            if idx != -1:
                end_idx = idx
                break
        
        if end_idx == -1:
            return desc  # no end marker found → defensive fallback
        
        return desc[:start_idx] + desc[end_idx:]

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data["name"],
            gender=data["gender"],
            character_description=translate_hairskin(data["characterDescription"]),
            clothing_description=translate_clothing(data["clothingDescription"]),
            character_description_cartoon=translate_hairskin(data["characterDescriptionCartoon"])
        )

    def describe_clothing_for_shot(self, shot_type, facing):
        pronouns = {"feminine": "she", "masculine": "he", "androgynous": "they"}
        pronoun = pronouns[self.gender]
        return translate_clothing(describe_character_outfit(
            pronoun,
            self.clothing_description,
            shot_type,
            facing
        ))

    def change_clothing(self, clothing):
        self.clothing_description = translate_clothing(clothing)
