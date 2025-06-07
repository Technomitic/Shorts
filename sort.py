import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image
import numpy as np


def create_short_clip(
    clip,
    part_number,
    output_folder,
    background_image_path,
    screen_resolution,
):
    screen_w, screen_h = screen_resolution

    # Load and resize background image
    bg_pil = Image.open(background_image_path).convert("RGB")
    bg_pil = bg_pil.resize((screen_w, screen_h))
    bg_np = np.array(bg_pil)
    bg_clip = ImageClip(bg_np).set_duration(clip.duration)

    # Center the video on background
    video_clip = clip.set_position("center")

    # Final composite
    final = CompositeVideoClip([bg_clip, video_clip])

    output_path = os.path.join(output_folder, f"short_part{part_number:03}.mp4")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"✅ Saved: {output_path}")


def parse_parts_input(user_input, total_parts):
    parts = set()
    if not user_input.strip():
        return set(range(1, total_parts + 1))

    for part in user_input.split(','):
        if '-' in part:
            start, end = part.split('-')
            parts.update(range(int(start), int(end) + 1))
        else:
            parts.add(int(part.strip()))
    return parts


def split_movie_into_shorts(
    input_path,
    output_folder="shorts_output",
    duration=60,
    background_image_path="background.jpg",
    screen_resolution=(1080, 1920),
):
    os.makedirs(output_folder, exist_ok=True)
    print("📥 Loading video...")
    video = VideoFileClip(input_path)
    total_duration = int(video.duration)
    total_parts = (total_duration + duration - 1) // duration

    print(f"🎞️ Total video duration: {total_duration} seconds")
    print(f"🔀 Will be split into {total_parts} parts (each {duration}s)")

    user_input = input("📌 Enter part numbers to generate (e.g. 1,3,5 or 2-4). Press Enter to generate all: ")
    selected_parts = parse_parts_input(user_input, total_parts)

    part_number = 1
    for start in range(0, total_duration, duration):
        end = min(start + duration, total_duration)
        if part_number in selected_parts:
            clip = video.subclip(start, end)
            create_short_clip(
                clip,
                part_number,
                output_folder,
                background_image_path,
                screen_resolution,
            )
        else:
            print(f"⏩ Skipping Part {part_number}")
        part_number += 1

    print("🎉 All done!")


# Run the generator
if __name__ == "__main__":
    split_movie_into_shorts(
        input_path="Lucifer_2016_S01_E01_07_720p_HEVC_HDRip_Dual_Audio_Hindi_+_English.mkv",  # Replace with your actual video
        output_folder="output_shorts",
        duration=60,
        background_image_path="bg_1.jpg",  # Replace with your background image
        screen_resolution=(1080, 1920),
    )

        # input_path="Lucifer_2016_S01_E01_07_720p_HEVC_HDRip_Dual_Audio_Hindi_+_English.mkv",  # Replace with your actual video
        # background_image_path="bg_1.jpg",  # Replace with your background image
        # screen_resolution=(1080, 1920),

