
image_video_prompt_generation = """
# Prompt for Image & Video Generation – Biblical & Christian Themed

## Task Overview
You are a world‑class visual storyteller. Given a Biblically rich passage, create:
Image prompts — single‑frame, minimalist compositions that evoke beauty, stillness, and gentle Christian symbolism.
Video prompts — descriptions of how each image unfolds in a slow, sacred motion suitable for sleep‑aid shorts on TikTok / YouTube.

## Goal
Generate {number} tranquil image prompts.
For every image prompt, produce a matching video prompt. Both must:
1. Draw unmistakable inspiration from Scripture or Christian tradition (setting, symbol, character, or tone).
2. Convey the emotional and spiritual atmosphere of the passage
3. Emphasize simplicity, sacred stillness, and subtle symbolism.

## Requirement
### Image prompt
##### Role
Give instructions for the image generation moodel to take on the role of an artist transported to a serene Biblical scene, capturing a single, evocative moment
##### Subject (Who/What):
A single, biblically relevant moment, such as: a serpent tempting Eve, God's covenent with Abraham
Avoid abstractions: “peace,” “grace,” “salvation.”

##### Style:
    Emulate the style of a Rennaisance or Baroque painting, with a focus on chiaroscuro lighting and rich textures. Use Baroque biblical paintings as inspiration.
    Should evoke strong emotion using rich texture, tones, and color
    Lighting: Use different lighting for different emotions - Soft golden light (warmth/hope), harsh shadows (tension), candlelight (intimacy), fog (uncertainty)
    Color: Use different colors for different emotions - Blue-gray (sorrow), golden (joy), crimson (passion or danger), white (purity)

##### Relevance:
    The scene must be relevant to the corresponding text:
    {cur_text}

##### Image prompt Examples:
1) Abraham and the Stars
You are an artist transported to a serene Biblical scene, capturing the moment when Abraham contemplates God’s covenant. In a Baroque style, Paint an aged Abraham standing alone on a quiet desert hill under a vast starlit sky. His face is uplifted in wonder, bathed in soft silver moonlight and cool blue-gray tones that evoke quiet reverence and longing. The cloak he wears stirs gently in the night wind, while deep chiaroscuro shadows emphasize the spiritual weight of the promise.

2) Peter Weeping After the Rooster Crows
You are an artist transported to a serene Biblical scene, capturing the instant after Peter denies Jesus. In a Baroque style, depict Peter alone in an empty courtyard at dawn, his back slumped against a stone wall, face buried in his hands. A rooster perches in shadow nearby. Use dim, blue-gray light with soft, golden highlights from the breaking sun to contrast sorrow with the first glimmer of forgiveness. The rough textures of stone and cloth should enhance the emotional stillness.

### Video prompt
Structure each video prompt as Subject + Scene + Visual Change.
    Camera: The frame remains completely fixed, no pan, zoom, or tilt.
    Composition: The scene is visually simple, containing only a few key elements. Avoid clutter.
    Subject Motion: If any, movement should be minimal and extremely slow (e.g., a flickering flame or slight hand motion).
    Environmental Change: Use slow and subtle effects only (e.g., mist drifting, light deepening).
    Tone: Peaceful, sacred, timeless. Avoid modern references or sudden action.

##### Video prompt Example:
1. Fixed camera on a candle placed on a plain wooden table. The flame flickers gently. In the background, a linen curtain moves slightly as the sky slowly darkens.
2. Still frame of a single olive tree standing in a misty field. The grass at its base shifts faintly. The sky gradually dims, and the mist thickens in the distance.
3. Unmoving shot of a boy with a candle. He sits quietly. His fingers rest near the flame, which flickers softly. The sky behind him brightens slowly.
4. Fixed view of a dove on a wooden cross. Light rain falls. Behind the dove, clouds move slowly, allowing soft morning light to emerge.
5. Still frame of a shepherd under a tree. A lamb lies beside him. Leaves drift down slowly as the sky turns from orange to deep dusk.

## Output Format:
A list of dictionaries, each containing two keys:
image_prompt: a detailed, cinematic image prompt
video_prompt: a visual description of how the scene unfolds as a short film

## IMPORTANT NOTES:
Ensure the output is formatted exactly as specified, with no additional text or commentary outside the JSON structure. Because your output will be read by python code, ensure all characters of your output are within the standard ASCII or basic Latin charset: no fancy quotes or special dashes. Avoid special unicode characters, along with em-dashes. Keep it simple.

Additionally, the prompts you are generating are for a single scene in a much larger whole. You must keep your image and video prompt directions consistent across the entire video. For example, if the sky is brightening in the first scene, the second scene must not be set at night if the two clips are related and are meant to be interpreted as in chronological order. If a wind blows a candle out in the first clip, it must remain blown out in the second unless there is a reason for it to be lit. If you are referencing the same object, then that object must look the same in your prompt. Be consistent. 
Of course, you are allowed to decide what exactly goes in a scene and can vary objects accordingly to avoid visual fatigue. For example, if you want a source of light, it can come from a clay oil lamp, or a hanging lantern, or the sun, etc. And if the scene changes, feel free to use objects, symbols, and scenery that are completely different. The main thing to remember is that if you choose to use the same object as in the previous prompt, or if the scene you are currently portraying directly builds off of the previous scene, the objects/time/place/colors used must all look the same and any changes must be logical. For example, if you first show a person exiting a car to enter a grocery store, the person who exits in the next scene must look the same, the car must be the same model, and they must exit carrying groceries or other products one would find in a grocery store. 
Below are the previous prompts you have generated for the video:
"prev_prompt": {prev_prompt}
Note: if there are no previous prompts, then you are currently generating your first scene and don't need to worry about consistency. But if there is a previous prompt loaded, KEEP IT CONSISTENT.

## Input:
"topic_summary": {summary},
"current_text": {cur_text},
"image_prompt_number": {number}

## Output:
"""