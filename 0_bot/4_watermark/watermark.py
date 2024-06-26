import moviepy.editor as mp
from moviepy.video.fx.all import vfx

def add_moving_watermark(video_path, watermark_path, output_path):
  # Load the main video
  clip = mp.VideoFileClip(video_path)
  
  # Load the watermark image
  watermark = (mp.ImageClip(watermark_path)
                .set_duration(clip.duration)
                .resize(height=50)  # Resize the watermark
                .set_pos(lambda t: ('right', int(50 * t)))  # Moving position
              )

  # Composite the video with the watermark
  final = mp.CompositeVideoClip([clip, watermark])
  
  # Write result to a file
  final.write_videofile(output_path, codec='libx264')

# Example usage
add_moving_watermark('input_video.mp4', 'watermark.png', 'output_video.mp4')
