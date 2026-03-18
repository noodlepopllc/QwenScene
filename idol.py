import random

class IdolPOVScene:
    def __init__(self):
        # -------------------------
        #   CHARACTER POOLS
        # -------------------------
        self.age = [
            "early 20s", "mid 20s", "late 20s",
            "early 30s"
        ]

        self.race = [
            "East Asian", "Southeast Asian", "South Asian",
            "White", "Black", "Latina", "Mixed"
        ]

        self.jawline = [
            "soft jawline", "rounded jawline",
            "defined jawline", "sharp jawline"
        ]

        self.eyes = [
            "round eyes", "almond eyes",
            "narrow eyes", "wide-set eyes"
        ]

        self.hair = [
            "short bob silhouette",
            "medium wavy silhouette",
            "long straight silhouette",
            "long wavy silhouette",
            "shoulder-length silhouette",
            "tied-back silhouette",
            "short layered silhouette"
        ]

        self.haircolor = ["brown", "blonde", "amber", "auburn", "black", "brunette" ,"red", "platinum"]


        # -------------------------
        #   IDOL OUTFITS
        # -------------------------
        self.outfits = [
            "soft knit sweater and skirt",
            "simple pastel blouse and jeans",
            "light cardigan over a fitted top",
            "flowy sundress",
            "casual t-shirt with soft fabric drape",
            "off-shoulder top and skirt",
            "light jacket over a simple dress",
            "camisole with loose cardigan",
            "sleek monochrome outfit",
            "minimalist top and trousers"
        ]

        self.textures = [
            "soft knit texture",
            "light chiffon texture",
            "smooth satin texture",
            "matte cotton texture",
            "silky fabric texture",
            "delicate lace texture",
            "light wool texture",
            "fine ribbed texture",
            "soft fleece texture",
            "subtle shimmer fabric texture",
            "light linen texture",
            "velvety soft texture"
        ]


        # -------------------------
        #   INTIMATE POV LOCATIONS
        # -------------------------
        self.locations = [
            "quiet studio room",
            "softly lit hallway",
            "sunlit window corner",
            "cozy indoor space",
            "minimalist room with soft textures",
            "rooftop at golden hour",
            "empty rehearsal room",
            "quiet café interior",
            "dimly lit backstage area",
            "open field at sunset"
        ]

        # -------------------------
        #   EXTREME POV TYPES
        # -------------------------
        self.pov = [
            "close POV as if the viewer is standing right in front of her",
            "slightly low POV looking up at her face",
            "over-the-shoulder POV from the viewer’s perspective",
            "intimate eye-level POV directly facing her",
            "very close POV capturing subtle facial details",
            "soft forward POV as she approaches the viewer"
        ]

        # -------------------------
        #   EMOTIONAL LIGHTING
        # -------------------------
        self.lighting = [
            "warm soft lighting that highlights her expression",
            "gentle diffused window light",
            "soft golden-hour glow",
            "cool ambient lighting with subtle highlights",
            "warm interior lighting with soft shadows",
            "dim emotional lighting with a soft rim light"
        ]

        # -------------------------
        #   MICRO-MOVEMENTS
        # -------------------------
        self.micro = [
            "a subtle shift of her eyes",
            "a gentle tilt of her head",
            "a soft inhale visible in her shoulders",
            "a tiny smile forming at the corner of her lips",
            "a slow blink with emotional weight",
            "a delicate adjustment of her posture",
            "a small hand movement near her chest",
            "a soft sway of her hair as she moves",
            "a faint tremble of anticipation in her breath",
            "a gentle lean closer toward the viewer"
        ]

        # -------------------------
        #   ACTIONS (unlimited movement)
        # -------------------------
        self.actions = [
            "she slowly approaches the viewer",
            "she steps closer with soft confidence",
            "she moves gently as if engaging directly with the viewer",
            "she walks forward with emotional intent",
            "she shifts her weight and leans in slightly",
            "she moves gracefully with fluid idol-like motion",
            "she steps into the light revealing her expression",
            "she circles subtly before facing the viewer again"
        ]

        self.colors = [
            "soft rose pink", "warm peach", "deep crimson", "sunset orange", "blush pink",
            "icy blue", "soft lavender", "deep violet", "cool mint", "midnight blue",
            "pure white", "cream beige", "charcoal black", "matte gray",
            "neon pink", "electric blue", "vibrant yellow", "bright teal"
        ]

    def to_prompt(self, data):
        return (
            f"A {data['age']} {data['race']} female idol with a {data['jawline']} and "
            f"{data['eyes']}, wearing {data['outfit']}, her {data['haircolor']} hair in a {data['hair_silhouette']}. "
            f"Scene takes place in a {data['location']}. "
            f"Camera POV: {data['pov']}. "
            f"Lighting: {data['lighting']}. "
            f"Action: {data['action']}. "
            f"Micro-movement: {data['micro_movement']}."
        )

    



    # -------------------------
    #   SINGLE SCENE GENERATOR
    # -------------------------
    def generate(self, seed=None):
        if seed is not None:
            random.seed(seed)

        data = {
            "age": random.choice(self.age),
            "race": random.choice(self.race),
            "sex": "female",
            "jawline": random.choice(self.jawline),
            "eyes": random.choice(self.eyes),
            "hair_silhouette": random.choice(self.hair),
            "haircolor": random.choice(self.haircolor),

            "outfit": f'{random.choice(self.colors)} {random.choice(self.textures)} {random.choice(self.outfits)}',
            "location": random.choice(self.locations),

            "pov": random.choice(self.pov),
            "lighting": random.choice(self.lighting),

            "action": random.choice(self.actions),
            "micro_movement": random.choice(self.micro)
        }
        return self.to_prompt(data)


# -------------------------
#   MAIN METHOD
# -------------------------
def main(count=50, seed=None):
    generator = IdolPOVScene()

    if seed is not None:
        random.seed(seed)

    scenes = []
    for _ in range(count):
        scenes.append(generator.generate())

    return scenes


# Example usage:
if __name__ == "__main__":
    results = main()
    for i, scene in enumerate(results, 1):
        #print(f"Scene {i}: {scene}\n")
        print(scene)

