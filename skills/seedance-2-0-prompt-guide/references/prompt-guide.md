# Seedance 2.0 Prompt Guide Reference

Source: BytePlus ModelArk document `2222480`, "Dreamina Seedance 2.0 series prompt guide", last updated 2026-04-23.

## Contents

- Core prompt formula
- Multimodal reference control
- Text rendering
- Image references
- Video references
- Video editing
- Compact prompt patterns

## Core Prompt Formula

Seedance 2.0 follows natural-language logic. Build prompts from:

- Required: subject plus motion/action. Define who performs what action.
- Optional: environment and aesthetics. Describe spatial background, lighting, tone, or visual style.
- Optional advanced controls: camera movement, cuts, audio, scene sound effects, ambient sound, dialogue, music, and timing.

Best default order:

```text
[Subject] + [motion/action] + [environment] + [aesthetic/style] + [camera/cuts/timing] + [audio/text instructions]
```

## Multimodal Reference Control

Seedance 2.0 can use image, audio, and video references. Always identify references explicitly.

- Use `Image 1`, `Image 2`, ... and `Video 1`, `Video 2`, ...
- If order matters, upload assets in the desired order and say the output should follow that order.
- Tell the model what to transfer: composition, identity, outfit, product shape, logo, scene layout, motion, camera movement, VFX, audio rhythm, or dialogue.

Strong phrasing:

```text
Use the composition of Image 1.
Maintain the character design from Image 2.
Match the motion of Video 1.
Refer to the camera movement in Video 1.
Keep the VFX formation trajectory from Video 1.
```

## Text Rendering

Seedance 2.0 supports text in T2V, I2V, R2V, and V2V. It can adapt font style and color to the scene, and can follow explicit style, timing, entrance, and layout instructions.

Text reliability rules:

- Use common vocabulary and familiar phrases.
- Avoid rare words when exact text rendering matters.
- Minimize special symbols and non-standard punctuation.
- Quote exact text, dialogue, and captions.

### Slogans

Template:

```text
[Text content] + [timing] + [positioning] + [entrance/appearance style], [visual attributes such as color or font style].
```

Use logo or brand-image references when the text must match a strict brand standard.

Example pattern:

```text
The frame gradually blurs, and the text "Bite", "Laugh", and "Seedance" appears in order at the center of the screen in a hand-drawn comic style.
```

### Subtitles

Template:

```text
Display subtitles at the bottom-center with the text. The subtitles must be perfectly synchronized with the audio rhythm and pacing.
```

For dialogue, ask for subtitles to appear sequentially as each character speaks.

Example pattern:

```text
Voiceover: A calm male voice says: "..." Text integration: render the narration as bottom-center subtitles, perfectly synchronized with audio timing.
```

### Speech Bubbles

Template:

```text
[Character] says, "[Dialogue]." Speech bubbles appear around the character containing the spoken text.
```

For multiple speakers, bind each speech bubble to the currently speaking character.

## Image References

### Multi-Perspective Subject Reference

Use for products or characters shown from several angles.

Template:

```text
Refer to/Extract/Combine/Use the [subject] from [Image N] to generate [scene description], maintaining consistent [subject] features.
```

Product pattern:

```text
Use the cameras featured in Image 1, Image 2, and Image 3. Replace the original background with a white one, place the cameras on a white table, then rotate 360 degrees around the cameras to clearly show the front, sides, and back.
```

Character pattern:

```text
Refer to the woman in Image 1, Image 2, and Image 3, and generate a scene of her eating cake in a coffee shop while maintaining her facial features and outfit consistency.
```

### Multi-Image Reference

Use when different images control different elements.

Template:

```text
Refer to / Extract / Combine / Follow the [referenced elements] from [Image N] to generate [scene description], while maintaining the consistency of [referenced elements].
```

Common bindings:

- Logo reference: define where the logo appears, forms, or remains.
- Multi-subject reference: use each image as a prototype for a subject.
- Multi-element reference: bind character, clothing, location, object, and logo separately.
- Multi-panel sequence reference: follow frame compositions in strict predefined order.
- Sequence reference: combine specific compositions, cuts, character references, and dialogue in order.

Sequence phrasing:

```text
Refer to the sequence in Image 1. Present all frame compositions from Image 1 in strict predefined order, then continue with [new action].
```

## Video References

Upload videos in order when sequence matters. Define the generated content's relationship to the source.

### Motion Reference

Template:

```text
Refer to the [motion description] from [Video N] to generate [scene description], keeping the motion details consistent.
```

Use for body movement, object motion, choreography, product transformation motion, or animal motion.

### Camera Motion Reference

Template:

```text
Refer to the [camera movement description] from [Video N] to generate [scene description], keeping the scene consistent.
```

Use for first-person movement, push-ins, pullbacks, pans, dives, rotations, or shot language.

### VFX Reference

Template:

```text
Refer to the [VFX effects description] from [Video N] to generate [scene description], keeping the special effects consistent.
```

When trajectory matters, say the effect follows the exact same motion path and sequence.

## Video Editing

Seedance 2.0 supports adding, removing, modifying elements, extending video forward/backward, and completing tracks.

If a specific sequence matters, upload clips in order and refer to `Video 1`, `Video 2`, ... precisely.

### Add, Remove, Modify

Templates:

```text
Adding: At [timestamp/timing] and [spatial location] of [Video N], add [description of intended element].
Removing: Remove [element to be deleted] from [Video N], keeping the rest of the video content unchanged.
Modifying: Replace [description of element to be changed] in [Video N] with [description of intended element].
```

Useful preservation phrase:

```text
Preserve all original motions and camera work.
```

### Extend Videos

Templates:

```text
Extend [Video N] forward/backward + [description of extended content].
Generate content before/after [Video N] + [description of extended content].
```

Official behavior to remember: the model extracts transition frames for seamless blending, and the original segments of the input video are not regenerated.

### Complete Tracks

Template:

```text
[Video 1] + [transition description] + followed by [Video 2] + [transition description] + followed by [Video 3].
```

Limits and behavior:

- Maximum 3 input video clips.
- Total combined duration must not exceed 15 seconds.
- The model may automatically trim connecting segments of start/end clips to keep synthesis seamless and logical.

## Compact Prompt Patterns

T2V:

```text
T2V: [subject] [action] in [environment], [visual style]. [Camera/cuts]. [Audio/text if needed].
```

I2V with image identity:

```text
I2V: Use [subject/object] from Image 1 to create [scene/action], maintaining consistent [features]. [Camera/aesthetic/audio].
```

R2V with multiple images:

```text
R2V: Use [element A] from Image 1, [element B] from Image 2, and [layout/logo/style] from Image 3 to generate [scene], maintaining consistency of each referenced element.
```

V2V motion transfer:

```text
V2V: Refer to the [motion/camera/VFX] in Video 1 to generate [new scene], keeping [motion/camera/VFX] consistent while changing [subject/environment/style].
```

Video edit:

```text
Edit Video 1: [add/remove/replace] [element] [at timing/location], keeping the rest of the video unchanged and preserving original motion and camera work.
```
