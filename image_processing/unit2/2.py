import cv2
import numpy as np
import matplotlib.pyplot as plt

def histogram_equalization(image_path):
    """
    Perform histogram equalization on an image
    """
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply histogram equalization
    equalized = cv2.equalizeHist(img)
    
    # Manual implementation for better understanding
    def manual_hist_eq(image):
        # Calculate histogram
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        
        # Calculate CDF
        cdf = hist.cumsum()
        cdf_normalized = cdf * 255 / cdf[-1]
        
        # Apply transformation
        equalized_manual = np.interp(image.flatten(), bins[:-1], cdf_normalized)
        return equalized_manual.reshape(image.shape).astype(np.uint8)
    
    manual_eq = manual_hist_eq(img)
    
    # Display results
    plt.figure(figsize=(15, 5))
    
    plt.subplot(2, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(equalized, cmap='gray')
    plt.title('OpenCV Histogram Equalization')
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(manual_eq, cmap='gray')
    plt.title('Manual Histogram Equalization')
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.hist(img.ravel(), bins=256, alpha=0.7, label='Original')
    plt.title('Original Histogram')
    plt.legend()
    
    plt.subplot(2, 3, 5)
    plt.hist(equalized.ravel(), bins=256, alpha=0.7, label='Equalized')
    plt.title('Equalized Histogram')
    plt.legend()
    
    plt.subplot(2, 3, 6)
    plt.hist(manual_eq.ravel(), bins=256, alpha=0.7, label='Manual Eq')
    plt.title('Manual Eq Histogram')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return equalized, manual_eq

# Usage
if __name__ == "__main__":
    opencv_eq, manual_eq = histogram_equalization('profile.jpg')
    cv2.imwrite('histogram_equalized.jpg', opencv_eq)