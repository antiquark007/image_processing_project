import cv2
import numpy as np
import matplotlib.pyplot as plt

def contrast_stretching(image_path):
    """
    Perform contrast stretching on an image
    """
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Get min and max pixel values
    r_min = np.min(img)
    r_max = np.max(img)
    
    # Apply contrast stretching formula: s = (r - r_min) * (255 / (r_max - r_min))
    stretched = ((img - r_min) * (255.0 / (r_max - r_min))).astype(np.uint8)
    
    # Display results
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(stretched, cmap='gray')
    plt.title('Contrast Stretched')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.hist(img.ravel(), bins=256, alpha=0.5, label='Original')
    plt.hist(stretched.ravel(), bins=256, alpha=0.5, label='Stretched')
    plt.title('Histogram Comparison')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return stretched

# Usage
if __name__ == "__main__":
    # Replace with your image path
    enhanced_img = contrast_stretching('profile.jpg')
    cv2.imwrite('contrast_stretched.jpg', enhanced_img)