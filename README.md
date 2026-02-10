# Biblical Video Generation Pipeline

A comprehensive AI pipeline with HITL for transforming biblical text into cinematic video content. This project automatically generates narrated videos with AI-created visuals that bring scripture to life through a multi-stage generation process.

## Overview

This pipeline converts biblical chapters into complete videos by:
1. Generating narrated audio from scripture text
2. Creating scene-by-scene image prompts
3. Generating images using AI image generation
4. Converting images to animated videos with motion
5. Assembling everything into a final combined video

## Project Structure

```
.
├── bible_chapter.py                      # Biblical text storage (The uploaded file includes two)
├── generate_subtitle.py                  # Audio generation and subtitle creation
├── generate_meta_prompt.py               # Scene and image prompt generation
├── meta_prompt.py                        # Meta-prompt template for scene creation
├── generate_images_from_meta_prompt.py   # Image generation with quality control
├── editing_evaluation_prompt.py          # Image quality evaluation prompt
├── generate_video_meta_prompt.py         # Video motion prompt generation
├── video_meta_prompt.py                  # Video prompt template
├── trim_videos.py                        # Video trimming and concatenation
└── prompt_library_edit3.py              # Deprecated prompt library
```

## Features

### 1. Audio Generation
- Text-to-speech conversion using customizable voices
- Automatic subtitle generation with precise timing
- Support for multiple narrators/speakers

### 2. Intelligent Scene Breakdown
- AI-powered scene segmentation based on narrative beats
- Dynamic scene length calculation proportional to audio duration
- Maintains narrative coherence across scenes

### 3. Image Generation with Quality Control
- Multi-attempt generation with automatic retry
- Built-in quality evaluation system checking for:
  - Historical accuracy (clothing, settings)
  - Compositional correctness
  - Proper exposure and contrast
  - Accurate character counts and positions
  - Realistic anatomy and physics
  - Correct censorship
- Automatic prompt refinement on failures

### 4. Video Animation
- Conversion of static images to subtle motion video
- Cinematic camera movements (dolly, pan, focus shifts)
- Atmospheric effects (fog, light changes, environmental motion)
- Character micro-expressions and gestures
- Maintains reverent, sacred tone

### 5. Quality Assurance
- Multi-endpoint load balancing for generation
- Automatic detection of missing scenes
- Validation against biblical text
- Exposure and lighting consistency checks

## Prerequisites

### Required Services
- Azure OpenAI API (GPT-4 with vision)
- Gradio endpoints for:
  - Text-to-speech generation
  - Image generation (4 endpoints recommended)
  - Video generation (6 endpoints recommended)

### Python Dependencies
```bash
pip install gradio-client
pip install openai
pip install python-dotenv
pip install mutagen
pip install moviepy
pip install tqdm
```

## Setup

### 1. Environment Variables

Create a `.env` file with the following:

```env
# Azure OpenAI Configuration
OPENAI_ENDPOINT=your_azure_openai_endpoint
OPENAI_KEY=your_api_key
API_VERSION=

# Gradio Endpoints
SUBTITLE_ENDPOINT=your_tts_endpoint
IMAGE_ENDPOINT_1=your_image_endpoint_1
IMAGE_ENDPOINT_2=your_image_endpoint_2
IMAGE_ENDPOINT_3=your_image_endpoint_3
IMAGE_ENDPOINT_4=your_image_endpoint_4
VIDEO_ENDPOINT_1=your_video_endpoint_1
VIDEO_ENDPOINT_2=your_video_endpoint_2
VIDEO_ENDPOINT_3=your_video_endpoint_3
VIDEO_ENDPOINT_4=your_video_endpoint_4
VIDEO_ENDPOINT_5=your_video_endpoint_5
VIDEO_ENDPOINT_6=your_video_endpoint_6

# File Paths
INPUT_BASE_PATH=./output
```

### 2. Directory Structure

The pipeline automatically creates the following directories:
```
output/
├── chapter_X_images/          # Generated images
├── generated_videos_ch_X/     # Generated videos
├── final_vid_ch_X/           # Trimmed videos
├── scenes_ch_X.json          # Scene metadata
├── video_prompts_ch_X.json   # Video generation prompts
├── subtitle_X.json           # Subtitle timing data
└── combined_ch_X.mp4         # Final output video
```

## Usage

### Complete Pipeline (Recommended)

Run the pipeline in sequence:

```bash
# Step 1: Generate audio and subtitles
python generate_subtitle.py

# Step 2: Create scene breakdown and image prompts
python generate_meta_prompt.py

# Step 3: Generate images (with automatic quality control)
python generate_images_from_meta_prompt.py

# Step 4: Generate videos from images
python generate_video_meta_prompt.py

# Step 5: Trim and combine videos
python trim_videos.py
```

### Configuration

Edit `generate_subtitle.py` to set:
- `chapter`: The chapter number to process
- `bible_text`: The scripture text to convert

### Targeted Generation

#### Generate Specific Scenes

In `generate_images_from_meta_prompt.py`, uncomment and modify:
```python
# Generate a single scene
target_global_idx = 20
filtered_image_prompt = [(prompt, idx) for prompt, idx in all_image_prompt if idx == target_global_idx]
```

#### Regenerate Missing Content

The pipeline automatically detects and regenerates missing scenes:
```python
# Finds scenes without PASS images and regenerates them
missing_ids = target_range - existing_pass_ids
filtered_image_prompt = [(prompt, idx) for prompt, idx in all_image_prompt if idx in missing_ids]
```

## Pipeline Details

### Stage 1: Audio Generation (`generate_subtitle.py`)

**Input:** Biblical text string  
**Output:** 
- `voice_file_X.mp3` - Narrated audio
- `subtitle_short_X.json` - Timing data
- `subtitle_long_X.json` - Detailed transcription

The TTS system generates natural-sounding narration and creates precise timing data for scene synchronization.

### Stage 2: Scene Creation (`generate_meta_prompt.py`)

**Input:** Subtitle timing data  
**Output:** `scenes_ch_X.json` containing:
- `scene_id`: Unique scene identifier
- `scene_title`: Descriptive scene name
- `bible_lines`: Associated scripture text
- `core_content`: Narrative essence
- `core_action`: Primary character action
- `image_prompt`: Detailed image generation prompt
- `scene_length`: Duration in seconds

**Key Features:**
- Automatically segments chapter into 20-30 scenes
- Proportionally distributes duration based on audio timing
- Maintains narrative coherence and emotional beats

### Stage 3: Image Generation (`generate_images_from_meta_prompt.py`)

**Input:** Scene prompts from Stage 2  
**Output:** `chapter_X_images/` directory with validated images

**Quality Control System:**
The evaluation system checks each image for:

1. **Historical Accuracy**
   - Period-appropriate clothing and settings
   - Biblically accurate elements

2. **Compositional Quality**
   - Proper framing and cropping
   - No text overlays or blank space
   - Complete, realistic scenes

3. **Technical Quality**
   - Proper exposure (no over/under-exposure)
   - Maintained contrast and detail
   - Sharp focus

4. **Content Accuracy**
   - Correct number of characters
   - Accurate animal species and counts
   - Visible character features match descriptions
   - No anatomical impossibilities

5. **Interpretation Accuracy**
   - Figurative language not taken literally
   - Appropriate visual metaphors

**Retry Logic:**
- Maximum 20 attempts per scene
- Failed images saved as `X_attemptN_FAIL.png`
- GPT-4 Vision evaluates and refines prompts
- Successful images saved as `X_attemptN_PASS.png`

### Stage 4: Video Generation (`generate_video_meta_prompt.py`)

**Input:** PASS images from Stage 3  
**Output:** 
- `video_prompts_ch_X.json` - Video motion prompts
- `generated_videos_ch_X/` - Generated video clips

**Video Prompt Components:**
- `role`: Creative direction for the AI
- `scene_overview`: Visual description
- `camera_motion`: Camera movement specification
- `background_motion`: Environmental changes
- `key_motion`: Array of animated effects
- `core_action`: Primary character movement
- `video_prompt`: Complete unified prompt
- `negative_prompt`: Quality constraints

**Cinematic Guidelines:**
- Baroque/Renaissance painting aesthetics
- Subtle, reverent character movements
- Single controlled camera movement per scene
- Atmospheric environmental effects
- Consistent lighting (no intensification)
- Maximum highlight: 90 IRE
- Sharp foreground throughout

### Stage 5: Final Assembly (`trim_videos.py`)

**Input:** 
- Generated videos from Stage 4
- Scene timing data from `scenes_ch_X.json`

**Output:** 
- `final_vid_ch_X/` - Trimmed individual scenes
- `combined_ch_X.mp4` - Complete assembled video

**Process:**
1. Trims each video to exact scene duration
2. Concatenates in sequential order
3. Applies video/audio codecs (H.264/AAC)

## Advanced Features

### Multi-Endpoint Load Balancing

The system distributes generation across multiple endpoints to maximize throughput:
```python
client_idx = global_idx % len(clients)  # Round-robin assignment
client = clients[client_idx]
client_lock = client_locks[client_idx]  # Thread-safe access
```

### Parallel Processing

Uses ThreadPoolExecutor for concurrent generation:
```python
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(generate_image, prompt, idx) 
               for prompt, idx in all_image_prompt]
```

### Automatic Recovery

Missing scenes are automatically detected and regenerated:
```python
existing_pass_ids = {int(f.split("_")[0]) for f in os.listdir(output_dir) 
                     if f.endswith("_PASS.png")}
missing_ids = target_range - existing_pass_ids
```

## Output Specifications

### Image Outputs
- **Format:** PNG
- **Aspect Ratio:** Landscape (16:9 recommended)
- **Style:** Baroque/Renaissance inspired
- **Quality:** High resolution, properly exposed

### Video Outputs
- **Format:** MP4 (H.264)
- **Audio:** AAC codec
- **Duration:** Variable (2-15 seconds per scene)
- **Motion:** Subtle, cinematic
- **Frame Rate:** Standard (24-30 fps)

## Quality Control Details

### Image Evaluation Rules

**FAIL Conditions:**
1. Non-biblical clothing (modern garments)
2. Incorrect character/animal counts
3. Visual inconsistencies or hallucinations
4. Improper cropping or composition
5. Over/under-exposure
6. Literal interpretation of figurative language
7. Character positions don't match descriptions

**Example Evaluation:**
```json
{
    "evaluation": "FAIL",
    "explanation": "The image depicts Adam wearing a leather jacket and jeans, which is not appropriate for a biblical setting",
    "new_prompt": "Adam, a tall muscular man with sun-weathered skin, wearing a simple woven tunic and leather sandals appropriate for ancient times..."
}
```

### Video Quality Guards

**Enforced Constraints:**
- No over-exposure or blown highlights
- Peak luminance ≤ 90 IRE
- Gentle highlight roll-off
- No pure-white clipping
- Subtle bloom only
- No jitter, blur, or banding
- No watermarks or frame skipping
- No temporal flicker
- Maintained sharpness throughout
- Consistent exposure

## Troubleshooting

### Common Issues

**Missing Images:**
```python
# Check for PASS images
existing = [f for f in os.listdir(output_dir) if "PASS" in f]
print(f"Found {len(existing)} successful images")
```

**Failed Generations:**
Check the attempt files to see failure reasons:
```bash
ls output/chapter_X_images/*_FAIL.png
```

**Video Generation Errors:**
- Verify all endpoints are accessible
- Check client locks aren't deadlocked
- Ensure sufficient disk space

### Debug Mode

Enable verbose logging:
```python
print(f"[DEBUG] Processing scene {global_idx}")
print(f"[DEBUG] Current prompt: {current_prompt}")
```

## Performance Optimization

### Recommended Settings

- **Image Generation:** 8 parallel workers across 4 endpoints
- **Video Generation:** 6 parallel workers across 6 endpoints
- **Retry Attempts:** 20 max per scene
- **Scene Count:** 20-30 per chapter

## Limitations

1. **Quality Control:** Despite 20 attempts, some scenes may still fail validation
2. **Consistency:** Visual consistency across scenes relies on prompt engineering
3. **Motion:** Video generation limited to subtle movements only
4. **API Costs:** Significant API usage for GPT-4 Vision and generation endpoints
5. **Biblical Accuracy:** Automated evaluation may miss subtle theological nuances

## Future Enhancements

- [ ] Support for additional biblical books
- [ ] Multi-language narration
- [ ] Interactive scene editing
- [ ] Real-time generation monitoring dashboard
- [ ] Advanced visual consistency checking
- [ ] Custom voice training
- [ ] Scene transition effects
- [ ] Background music integration

## Note

This project is a showcase using biblical text, but can work with other stories if the meta prompts are sufficiently adjusted to reflect the desired atmostphere and change of setting.

This pipeline requires substantial computational resources and API access. Test with a small chapter section before processing full chapters.
