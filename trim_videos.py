import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import json
from generate_subtitle import chapter

input_folder = "generated_videos_ch_" + chapter
video_prompt_file = "scenes_ch_" + chapter + ".json"

output_final_folder = "final_vid_ch_" + chapter
os.makedirs(output_final_folder, exist_ok=True)

final_output_path = "combined_ch_" + chapter + ".mp4"




clips_to_concatenate = []


with open(video_prompt_file, "r", encoding="utf-8") as f:
        merged_prompts = json.load(f)


# Build index of true video durations from JSON
index_to_true_length = {
    entry["scene_id"]: entry["scene_length"]
    for entry in merged_prompts
}

# trim videos to proper length
for video_file in os.listdir(input_folder):
    if video_file.endswith(".mp4"):
        video_path = os.path.join(input_folder, video_file)

        # Extract index from filename, e.g., "scene_10_output.mp4"
        index = video_file.split("_")[1]
        if index in index_to_true_length:
            target_duration = index_to_true_length[index]
            trimmed_path = os.path.join(output_final_folder, f"scene_{index}_output_trimmed.mp4")
            
            try:
                with VideoFileClip(video_path) as clip:
                    trimmed = clip.subclip(0, min(target_duration, clip.duration))
                    trimmed.write_videofile(trimmed_path, codec="libx264", audio_codec="aac", logger=None)
                # After saving to file, reload for concatenation
                final_trimmed_clip = VideoFileClip(trimmed_path)
                clips_to_concatenate.append(final_trimmed_clip)

                print(f"[TRIMMED] scene {index} to {target_duration:.2f}s")
            except Exception as e:
                print(f"[ERROR] Failed to trim scene {index}: {e}")
        else:
            print(f"[WARNING] No duration found for index {index}, skipping...")

# concatenate videos
# Get all trimmed video files and sort them
trimmed_videos = sorted([
    os.path.join(output_final_folder, f)
    for f in os.listdir(output_final_folder)
    if f.endswith("_output_trimmed.mp4")
])

# Load clips
clips = [VideoFileClip(f) for f in trimmed_videos]

# Concatenate
final_video = concatenate_videoclips(clips_to_concatenate, method="compose")
final_video.write_videofile(final_output_path, codec="libx264", audio_codec="aac")
print(f"[COMPLETED] Final combined video saved to {final_output_path}")