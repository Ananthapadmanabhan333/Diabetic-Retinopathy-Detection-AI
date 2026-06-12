import cv2
import numpy as np
from pathlib import Path

def resize_and_pad(image, target_size=(512, 512)):
    """Resize image and pad to keep aspect ratio."""
    h, w = image.shape[:2]
    sh, sw = target_size
    aspect = w / h

    if aspect > 1:
        new_w = sw
        new_h = np.round(new_w / aspect).astype(int)
        pad_vert = (sh - new_h) / 2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1:
        new_h = sh
        new_w = np.round(new_h * aspect).astype(int)
        pad_horz = (sw - new_w) / 2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else:
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    scaled_img = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    padded_img = cv2.copyMakeBorder(
        scaled_img, pad_top, pad_bot, pad_left, pad_right, 
        borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )
    return padded_img

def preprocess_retina_image(image_path, target_size=(512, 512)):
    """Standardize lighting and contrast using CLAHE and apply circular crop."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
        
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize & pad
    img = resize_and_pad(img, target_size)
    
    # Convert to LAB for CLAHE
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge and convert back
    limg = cv2.merge((cl, a, b))
    img_clahe = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    
    # Basic circular crop mask (assuming centered retina after padding)
    h, w = img_clahe.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w//2, h//2), int(min(h, w)*0.48), 1, thickness=-1)
    
    img_final = cv2.bitwise_and(img_clahe, img_clahe, mask=mask)
    return img_final

if __name__ == "__main__":
    print("Preprocessing utils loaded.")
