
def translate_hairskin(description):
    mapping = {
        # skin tone
        "fair-neutral": "fair",
        "fair-pink": "fair",
        "light-olive": "light",
        "light-neutral": "light",
        "light-yellow": "light",
        "medium-olive": "medium",
        "medium-yellow": "medium",
        "medium-brown": "medium",
        "golden-brown": "tan",
        "tan-golden": "tan",
        "tan-olive": "tan",
        "brown": "tan",
        "light-brown": "tan",
        "dark-brown": "brown",
        "deep-brown": "deep",
        "rich-brown": "deep",
        "dark-umber": "deep",
        "dark": "deep",

        # hair color
        "dark-blonde": "blonde",
        "platinum": "blonde",
        "auburn": "red",
    }

    tokens = description.split()
    normalized = [mapping.get(t, t) for t in tokens]
    return " ".join(normalized)


def translate_clothing(clothing):
    a = clothing
    a = a.replace("#4A4A4A", "darkNeutral (#4A4A4A)")
    a = a.replace("#B8B6B0", "midNeutral (#B8B6B0)")
    a = a.replace("#8A6A4F", "mutedBrown (#8A6A4F)")
    a = a.replace("#8E3F3A", "brickRed (#8E3F3A)")
    a = a.replace("#5A6B7A", "slateBlue (#5A6B7A)")
    a = a.replace("#4F7A76", "mutedTeal (#4F7A76)")
    a = a.replace("#6E7A5F", "desaturatedGreen (#6E7A5F)")
    a = a.replace("#4A6FB4", "mutedBlue (#4A6FB4)")
    clothing = a
    return clothing

