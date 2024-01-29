import os
import argparse
import cv2
from PIL import Image

dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Video Generation App")
parser.add_argument("--input", type=str, default=os.path.join(dir, "input/"), help="Path for input folder with images")
parser.add_argument("--output", type=str, default=os.path.join(dir, "output/"), help="Path for output video")
args = parser.parse_args()

scale_factor = 8

output_directory = os.path.dirname(args.output)

print("Start images upscaling at {}...".format(args.input))
for filename in os.listdir(args.input):
    if filename.endswith(('.png', '.jpg', '.jpeg')): # Add/check other formats if needed
        input_path = os.path.join(args.input, filename)
        output_path = os.path.join(output_directory, filename)

        try:
            with Image.open(input_path) as img:
                new_size = (img.width * scale_factor, img.height * scale_factor)
                resized_img = img.resize(new_size, Image.NEAREST)
                resized_img.save(output_path)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

print("Upscaling for {} completed".format(args.input))

# Assuming all images are of the same size, get dimensions from the first image
first_image_path = os.path.join(output_directory, os.listdir(output_directory)[0])
first_image = cv2.imread(first_image_path)
height, width, layers = first_image.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Adjust codec if needed
out = cv2.VideoWriter(args.output, fourcc, 60, (width, height))

for filename in sorted(os.listdir(output_directory)):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image formats
        image_path = os.path.join(output_directory, filename)
        img = cv2.imread(image_path)
        out.write(img)  # Write the frame to the video

out.release() # Release everything when done
print("Video creation {} done".format(args.output))