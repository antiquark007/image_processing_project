import cv2
import numpy as np
import matplotlib.pyplot as plt

def spatial_filtering(image_path):
    """
    Perform various spatial filtering operations
    """
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # SMOOTHING FILTERS
    
    # 1. Mean Filter (Box Filter)
    mean_filtered = cv2.blur(img, (5, 5))
    
    # 2. Gaussian Filter
    gaussian_filtered = cv2.GaussianBlur(img, (5, 5), 1.0)
    
    # 3. Median Filter (for salt and pepper noise)
    median_filtered = cv2.medianBlur(img, 5)
    
    # SHARPENING FILTERS
    
    # 4. Laplacian Filter
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    laplacian = np.absolute(laplacian).astype(np.uint8)
    
    # 5. Unsharp Masking
    gaussian_blur = cv2.GaussianBlur(img, (9, 9), 10.0)
    unsharp_mask = cv2.addWeighted(img, 1.5, gaussian_blur, -0.5, 0)
    
    # 6. Custom Sharpening Kernel
    sharpening_kernel = np.array([[-1, -1, -1],
                                  [-1,  9, -1],
                                  [-1, -1, -1]])
    sharpened = cv2.filter2D(img, -1, sharpening_kernel)
    
    # Display results
    plt.figure(figsize=(15, 10))
    
    images = [img, mean_filtered, gaussian_filtered, median_filtered,
              laplacian, unsharp_mask, sharpened]
    titles = ['Original', 'Mean Filter', 'Gaussian Filter', 'Median Filter',
              'Laplacian', 'Unsharp Masking', 'Sharpening Kernel']
    
    for i in range(len(images)):
        plt.subplot(3, 3, i+1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return {
        'mean': mean_filtered,
        'gaussian': gaussian_filtered,
        'median': median_filtered,
        'laplacian': laplacian,
        'unsharp': unsharp_mask,
        'sharpened': sharpened
    }

# Usage
if __name__ == "__main__":
    filtered_images = spatial_filtering('profile.jpg')
    
    # Save filtered images
    for name, img in filtered_images.items():
        cv2.imwrite(f'{name}_filtered.jpg', img)