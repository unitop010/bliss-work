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

    # Initial movement direction (45 degrees)
    speed = 50  # pixels per second
    velocity_x, velocity_y = speed, speed

    # Function to calculate the new position
    def position_func(t):
        nonlocal velocity_x, velocity_y
        
        # Calculate new positions based on time and speed
        new_x = (velocity_x * t) % (2 * (video_width - watermark_width))
        new_y = (velocity_y * t) % (2 * (video_height - watermark_height))

        # Reverse direction if needed
        if new_x > (video_width - watermark_width):
            new_x = 2 * (video_width - watermark_width) - new_x
            velocity_x = -speed
        else:
            velocity_x = speed

        if new_y > (video_height - watermark_height):
            new_y = 2 * (video_height - watermark_height) - new_y
            velocity_y = -speed
        else:
            velocity_y = speed

        return (new_x, new_y)
    
    # Set the dynamic position for the watermark
    watermark = watermark.set_pos(position_func)

    # Composite the video with the watermark
    final = mp.CompositeVideoClip([clip, watermark])

    # Write result to a file
    final.write_videofile(output_path, codec='libx264')
    

# Example usage
if __name__ == "__main__":
    input_video = input("Select video that need watermark: ")
    watermark_image = "watermark.png"
    output_video = f"{input_video}_watermark.mp4"

    add_moving_watermark(f'{input_video}.mp4', watermark_image, output_video)
