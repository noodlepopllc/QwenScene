PROMPT_FORMULA = '''
    Stylized illustration of [character].  
    Anatomically accurate proportions (7.5 heads tall), realistic joint alignment.  
    Facial structure: [jaw], [cheekbones], [eyes], [nose], [lips].  
    Soft cel-shaded lighting—gentle gradients for form, no harsh shadows.  
    Matte skin with light under-eye/nasolabial definition, no texture.  
    Hair as cohesive shape with soft highlights, no strand detail.  
    Limited color palette, no airbrushing, no photorealism.  
    9:16 vertical, medium shot.'''


Horizontal:  left third | centered horizontally | right third
Vertical:    floor-level | centered vertically | ceiling-height
Depth:       against front wall | mid-depth | against rear wall
Adjacency:   abutting | touching | flanking horizontally/vertically
Grouping:    aligned horizontally | stacked vertically | symmetrically placed


Goal,Effective Prompt Phrase,Why It Works
Bed continues out of frame left,"bed anchored to the left edge of the frame, continuing beyond the left boundary",Explicitly ties object to frame edge + continuation
Bed continues out of frame right,"bed extending out of frame to the right, only left portion visible",Forces asymmetric crop
"Headboard runs horizontally, cropped",horizontal headboard with left edge cropped by frame boundary,Describes the cropping event itself
Avoid centered truncation,avoid symmetrical cropping — bed flush against left frame edge,Negative instruction to override default priors

Weak (default behavior):

    "queen-size bed positioned on the left side"

→ Model renders bed centered within its own bounding box, often cropping both sides equally in vertical frame.
Strong (frame-aware):

    "queen-size bed anchored flush against the left edge of the frame, horizontal headboard extending beyond the left boundary with only the right two-thirds visible within the 9:16 composition"

→ Forces asymmetric crop where bed originates outside frame left and continues rightward into view.


Wide horizontal scene (what you imagine):
┌──────────────────────────────────────────────┐
│  [BED HEADBOARD running left→right]          │
│  ┌──────┐                                     │
│  │Night-│                                     │
│  │stand │                                     │
└──────────────────────────────────────────────┘

9:16 vertical crop (what model generates):
         ┌──────────────┐
         │  [BED]       │ ← Only right portion visible
         │  ┌──────┐    │    Left edge cropped
         │  │Night-│    │
         │  │stand │    │
         └──────────────┘
