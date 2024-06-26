import moviepy.editor as mp
from PIL import Image

def add_moving_watermark(video_path, watermark_path, output_path):
    # Load the main video
    clip = mp.VideoFileClip(video_path)
    
    # Load and resize the watermark image using Pillow
    watermark_image = Image.open(watermark_path)
    watermark_image = watermark_image.resize((int(watermark_image.width * 50 / watermark_image.height), 50), Image.LANCZOS)
    
    # Save the resized watermark to a temporary file
    temp_watermark_path = "resized_watermark.png"
    watermark_image.save(temp_watermark_path)

    # Load the resized watermark image into moviepy
    watermark = (mp.ImageClip(temp_watermark_path)
                .set_duration(clip.duration)
                .set_pos(lambda t: ('right', int(50 * t)))  # Moving position
                )

    # Composite the video with the watermark
    final = mp.CompositeVideoClip([clip, watermark])
    
    # Write result to a file
    final.write_videofile(output_path, codec='libx264')

# Example usage
add_moving_watermark('input_video.mp4', 'watermark.png', 'output_video.mp4')
