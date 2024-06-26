import moviepy.editor as mp
from PIL import Image

def add_moving_watermark(video_path, watermark_path, output_path):
    # Load the main video
    clip = mp.VideoFileClip(video_path)
    video_width, video_height = clip.size
    
    # Load and resize the watermark image using Pillow
    watermark_image = Image.open(watermark_path)
    watermark_image = watermark_image.resize((int(watermark_image.width * 50 / watermark_image.height), 50), Image.LANCZOS)
    
    # Save the resized watermark to a temporary file
    temp_watermark_path = "resized_watermark.png"
    watermark_image.save(temp_watermark_path)

    # Load the resized watermark image into moviepy
    watermark = mp.ImageClip(temp_watermark_path).set_duration(clip.duration)
    watermark_width, watermark_height = watermark.size

    # Function to calculate the new position
    def position_func(t):
        speed = 100  # pixels per second
        x = speed * t
        y = speed * t
        
        # Handle collisions with the boundaries
        if x + watermark_width > video_width:
            x = video_width - watermark_width
        if y + watermark_height > video_height:
            y = video_height - watermark_height

        return (x, y)
    
    # Set the dynamic position for the watermark
    watermark = watermark.set_pos(position_func)

    # Composite the video with the watermark
    final = mp.CompositeVideoClip([clip, watermark])

    # Write result to a file
    final.write_videofile(output_path, codec='libx264')
    

# Example usage
add_moving_watermark('1389.mp4', 'watermark.png', 'output_video.mp4')
