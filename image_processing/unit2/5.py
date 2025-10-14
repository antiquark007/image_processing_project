import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageEnhancement:
    def __init__(self, image_path):
        self.original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.results = {}
    
    def contrast_stretching(self):
        """Apply contrast stretching"""
        r_min = np.min(self.original)
        r_max = np.max(self.original)
        stretched = ((self.original - r_min) * (255.0 / (r_max - r_min))).astype(np.uint8)
        self.results['contrast_stretching'] = stretched
        return stretched
    
    def histogram_equalization(self):
        """Apply histogram equalization"""
        equalized = cv2.equalizeHist(self.original)
        self.results['histogram_equalization'] = equalized
        return equalized
    
    def spatial_smoothing(self, filter_type='gaussian', kernel_size=5):
        """Apply spatial smoothing filters"""
        if filter_type == 'mean':
            result = cv2.blur(self.original, (kernel_size, kernel_size))
        elif filter_type == 'gaussian':
            result = cv2.GaussianBlur(self.original, (kernel_size, kernel_size), 1.0)
        elif filter_type == 'median':
            result = cv2.medianBlur(self.original, kernel_size)
        
        self.results[f'{filter_type}_smoothing'] = result
        return result
    
    def spatial_sharpening(self, method='unsharp'):
        """Apply spatial sharpening"""
        if method == 'laplacian':
            laplacian = cv2.Laplacian(self.original, cv2.CV_64F)
            result = np.absolute(laplacian).astype(np.uint8)
        elif method == 'unsharp':
            gaussian_blur = cv2.GaussianBlur(self.original, (9, 9), 10.0)
            result = cv2.addWeighted(self.original, 1.5, gaussian_blur, -0.5, 0)
        
        self.results[f'{method}_sharpening'] = result
        return result
    
    def frequency_domain_filter(self, filter_type='lowpass', filter_name='gaussian', cutoff=50):
        """Apply frequency domain filtering"""
        rows, cols = self.original.shape
        
        # FFT
        f_transform = np.fft.fft2(self.original)
        f_shift = np.fft.fftshift(f_transform)
        
        # Create filter
        crow, ccol = rows // 2, cols // 2
        y, x = np.ogrid[:rows, :cols]
        d = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
        
        if filter_name == 'ideal':
            if filter_type == 'lowpass':
                mask = (d <= cutoff).astype(float)
            else:
                mask = (d > cutoff).astype(float)
        elif filter_name == 'gaussian':
            if filter_type == 'lowpass':
                mask = np.exp(-(d ** 2) / (2 * (cutoff ** 2)))
            else:
                mask = 1 - np.exp(-(d ** 2) / (2 * (cutoff ** 2)))
        elif filter_name == 'butterworth':
            order = 2
            if filter_type == 'lowpass':
                mask = 1 / (1 + (d / cutoff) ** (2 * order))
            else:
                mask = 1 - 1 / (1 + (d / cutoff) ** (2 * order))
        
        # Apply filter
        filtered = f_shift * mask
        
        # IFFT
        f_ishift = np.fft.ifftshift(filtered)
        img_back = np.fft.ifft2(f_ishift)
        result = np.real(img_back).astype(np.uint8)
        
        self.results[f'{filter_type}_{filter_name}'] = result
        return result
    
    def run_complete_pipeline(self):
        """Run all enhancement techniques"""
        print("Running complete image enhancement pipeline...")
        
        # Point processing
        self.contrast_stretching()
        self.histogram_equalization()
        
        # Spatial filtering
        self.spatial_smoothing('gaussian')
        self.spatial_smoothing('mean')
        self.spatial_sharpening('unsharp')
        self.spatial_sharpening('laplacian')
        
        # Frequency domain filtering
        self.frequency_domain_filter('lowpass', 'gaussian')
        self.frequency_domain_filter('highpass', 'gaussian')
        
        print("Pipeline complete!")
        return self.results
    
    def display_all_results(self):
        """Display all enhancement results"""
        num_results = len(self.results) + 1  # +1 for original
        cols = 4
        rows = (num_results + cols - 1) // cols
        
        plt.figure(figsize=(15, rows * 4))
        
        # Display original
        plt.subplot(rows, cols, 1)
        plt.imshow(self.original, cmap='gray')
        plt.title('Original')
        plt.axis('off')
        
        # Display results
        for i, (name, img) in enumerate(self.results.items(), 2):
            plt.subplot(rows, cols, i)
            plt.imshow(img, cmap='gray')
            plt.title(name.replace('_', ' ').title())
            plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def save_results(self, output_dir='output'):
        """Save all results"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, img in self.results.items():
            cv2.imwrite(f'{output_dir}/{name}.jpg', img)
        
        print(f"All results saved to {output_dir} directory")

# Usage example
if __name__ == "__main__":
    # Initialize enhancement pipeline
    enhancer = ImageEnhancement('profile.jpg')
    
    # Run complete pipeline
    results = enhancer.run_complete_pipeline()
    
    # Display all results
    enhancer.display_all_results()
    
    # Save results
    enhancer.save_results()
    
    # Individual technique examples
    print("\nRunning individual techniques:")
    
    # Point processing
    contrast_img = enhancer.contrast_stretching()
    hist_eq_img = enhancer.histogram_equalization()
    
    # Spatial filtering
    gaussian_smooth = enhancer.spatial_smoothing('gaussian')
    unsharp_sharp = enhancer.spatial_sharpening('unsharp')
    
    # Frequency domain
    lowpass_result = enhancer.frequency_domain_filter('lowpass', 'gaussian', 30)
    highpass_result = enhancer.frequency_domain_filter('highpass', 'gaussian', 30)