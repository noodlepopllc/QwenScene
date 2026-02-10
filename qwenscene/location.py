
from character_outfit import describe_character_outfit

class LocationColorProfile:
    def __init__(self, dominant_60, supporting_30, accent_10):
        self.dominant_60 = dominant_60
        self.supporting_30 = supporting_30
        self.accent_10 = accent_10

    def describe(self):
        return (
            f"60% {self.dominant_60}, "
            f"30% {self.supporting_30}, "
            f"10% {self.accent_10}"
        )

class LocationLightingProfile:
    def __init__(self, lighting_type, lighting_source, lighting_temperature):
        self.lighting_type = lighting_type
        self.lighting_source = lighting_source
        self.lighting_temperature = lighting_temperature

    def describe(self):
        return (
            f"{self.lighting_type} {self.lighting_temperature} light "
            f"from {self.lighting_source}"
        )

class Location:
    def __init__(self, name, description, lighting, color):
        self.name = name
        self.description = description
        self.lighting = lighting
        self.color = color
        self.details = []

    def add_detail(self, text):
        self.details.append(text)

    

    def describe(self):
        description = []
        description.append(self.name)
        description.append(self.description)
        description.append(self.lighting.describe())
        description.append(self.color.describe())
        description.extend(self.details)
        return ', '.join(description)

