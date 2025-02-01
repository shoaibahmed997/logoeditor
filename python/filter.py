import os
import cv2
import numpy as np

def adjust_image(image):
    # Convert to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize brightness
    norm = cv2.normalize(grayscale, None, alpha=100, beta=255, norm_type=cv2.NORM_MINMAX)

    # Convert all non-black pixels to white
    _, white_mask = cv2.threshold(norm, 1, 255, cv2.THRESH_BINARY)  

    # Convert to 3-channel white image
    white_image = np.full_like(image, 255)  

    # Apply the mask (keep white where the original image had content)
    final = cv2.bitwise_and(white_image, white_image, mask=white_mask)

    return final

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            if image is None:
                print(f"Could not read {filename}, skipping...")
                continue

            # Handle transparent PNGs
            if image.shape[-1] == 4:  # If image has an alpha channel
                alpha_channel = image[:, :, 3]  # Extract transparency
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)  # Convert to 3-channel
                edited_image = adjust_image(image)

                # Merge transparency back
                edited_image = cv2.merge([edited_image, alpha_channel])  
            else:
                edited_image = adjust_image(image)

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, edited_image)
            print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    input_folder = "./input_images"
    output_folder = "./edited_images"
    process_images(input_folder, output_folder)
