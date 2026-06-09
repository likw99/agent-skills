---
name: seedance-2-0-prompt-guide
description: BytePlus Dreamina Seedance 2.0 prompt guide distilled into practical prompt-writing workflows. Use when an agent needs to draft, improve, debug, or review Seedance 2.0 / Seedance 2.0 series video-generation prompts, including text-to-video, image-to-video, reference-to-video, video-to-video, audio/video generation, text rendering, subtitles, speech bubbles, image references, video motion/camera/VFX references, video editing, video extension, and track completion.
---

# Seedance 2.0 Prompt Guide

## Overview

Create Seedance 2.0 prompts using the official BytePlus Dreamina guidance. Optimize for natural-language logic, explicit reference mapping, audiovisual synchronization, and predictable edits.

For exact templates, limits, and task-specific phrasing, read `references/prompt-guide.md`.

## Workflow

1. Classify the request:
   - New generation: T2V, I2V, R2V, or V2V.
   - Text rendering: slogan, subtitle, or speech bubble.
   - Reference transfer: image subject, multi-image elements, video motion, camera motion, or VFX.
   - Video editing: add, remove, modify, extend forward/backward, or complete tracks.
2. Map all provided materials before writing:
   - Use explicit identifiers: `Image 1`, `Image 2`, `Video 1`, `Audio 1`.
   - If sequence matters, tell the user or assume assets are uploaded in the intended order.
   - State what each reference controls: subject identity, composition, outfit, logo, motion, camera movement, effects, audio, or scene layout.
3. Start the prompt with the logical core:
   - Required: subject plus action, i.e. who does what.
   - Add environment and aesthetics only after the core action is clear.
   - Add camera movement, cuts, timing, and audio when they affect the output.
4. Make reference instructions explicit:
   - Prefer "Use the composition of Image 1", "Maintain the character design from Image 2", "Match the motion of Video 1", or "Keep the VFX trajectory from Video 1".
   - For multiple references, bind each reference to one job when possible.
5. Make text and speech renderable:
   - Use common words and short phrases.
   - Quote exact on-screen text or dialogue.
   - Specify timing, position, entrance/appearance behavior, and visual style only when needed.
   - For subtitles, require bottom-center placement and synchronization with audio rhythm/pacing.
6. Preserve continuity for edits:
   - For removals, say to keep the rest of the video unchanged.
   - For replacements, say to preserve original motion and camera work.
   - For extensions, describe content before/after the input clip without regenerating the original segment.
7. Return the result in the form the user needs:
   - If the user asks for a prompt, provide one polished prompt.
   - If the user asks for variants, provide distinct prompt options with short labels.
   - If reviewing, list issues first, then provide an improved prompt.

## Prompt Shape

Use this structure unless the user's format requires otherwise:

```text
[Mode/task]: [subject + action]. [Reference bindings]. [Environment and aesthetic]. [Camera movement/cuts/timing]. [Text, dialogue, subtitle, or speech-bubble instructions]. [Audio or sound design]. [Continuity/edit constraints].
```

Keep prompts concise but concrete. Seedance 2.0 follows natural language well; do not turn the prompt into a dense parameter list unless the target API requires parameters separately.

## Quality Checklist

Before finalizing a prompt, verify:

- The subject and action are unambiguous.
- Every referenced image/video/audio has an identifier and a specific purpose.
- Sequence-dependent references say "in strict order" or equivalent.
- Text rendering uses simple vocabulary and avoids unusual symbols unless required.
- Dialogue, subtitles, speech bubbles, music, and sound effects are synchronized when relevant.
- Editing prompts include timestamp/spatial location when available and preservation constraints.
- Track-completion prompts use no more than 3 input video clips and no more than 15 seconds total when the user mentions clip counts or durations.

## Reference

- Source distilled from BytePlus ModelArk document `2222480`, ["Dreamina Seedance 2.0 series prompt guide"](https://docs.byteplus.com/en/docs/ModelArk/2222480), last updated 2026-04-23.
- Load `references/prompt-guide.md` for task-specific templates and official constraints.
