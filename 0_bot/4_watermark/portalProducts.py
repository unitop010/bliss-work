from PIL import Image
import os

def add_watermark(input_image_path, output_image_path, watermark_image_path, position):
    # Open the original image
    original = Image.open(input_image_path).convert("RGBA")
    
    # Open the watermark image
    watermark = Image.open(watermark_image_path).convert("RGBA")
    
    # Calculate the position for the watermark
    if position == 'center':
        x = (original.width - watermark.width) // 2
        y = (original.height - watermark.height) // 2
    elif position == 'bottom-right':
        x = original.width - watermark.width
        y = original.height - watermark.height

    # Create an RGBA canvas with the same size as the image
    transparent = Image.new('RGBA', original.size, (0, 0, 0, 0))
    
    # Paste the image and watermark onto the canvas
    transparent.paste(original, (0, 0))
    transparent.paste(watermark, (x, y), mask=watermark)
    
    # Convert back to RGB to save in common formats (like JPEG)
    final_image = transparent.convert("RGB")
    
    # Save the image
    final_image.save(output_image_path)

# Define paths
input_directory = 'lcd/portalData/product_image/'
output_directory = 'lcd/portalData/product_images/'
product_image_path = 'test.jpeg'
watermark_image_path = 'watermark.png'
output_image_path = 'image.jpg'
# product_image_path = 'path/to/product/image.jpg'
# watermark_image_path = 'path/to/watermark/image.png'
# output_image_path = 'path/to/output/image.jpg'

for filename in os.listdir(input_directory):
    if filename.endswith('.jpg'):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)
        print(f'\n{input_file_path}\n')
        # Add watermark
        add_watermark(input_file_path, output_file_path, watermark_image_path, position='bottom-right')
