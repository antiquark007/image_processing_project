import cv2
import numpy as np
import matplotlib.pyplot as plt

def frequency_domain_filtering(image_path):
    """
    Perform frequency domain filtering using Fourier Transform
    """
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    rows, cols = img.shape
    
    # Apply Fourier Transform
    f_transform = np.fft.fft2(img)
    f_shift = np.fft.fftshift(f_transform)
    
    # Create coordinate arrays
    crow, ccol = rows // 2, cols // 2
    
    # LOW-PASS FILTERS
    
    # 1. Ideal Low-Pass Filter
    def ideal_lowpass_filter(shape, cutoff):
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        y, x = np.ogrid[:rows, :cols]
        mask_area = (x - ccol) ** 2 + (y - crow) ** 2 <= cutoff ** 2
        mask[mask_area] = 1
        return mask
    
    # 2. Butterworth Low-Pass Filter
    def butterworth_lowpass_filter(shape, cutoff, order):
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2
        y, x = np.ogrid[:rows, :cols]
        d = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
        mask = 1 / (1 + (d / cutoff) ** (2 * order))
        return mask
    
    # 3. Gaussian Low-Pass Filter
    def gaussian_lowpass_filter(shape, cutoff):
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2
        y, x = np.ogrid[:rows, :cols]
        d = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
        mask = np.exp(-(d ** 2) / (2 * (cutoff ** 2)))
        return mask
    
    # HIGH-PASS FILTERS (complement of low-pass)
    
    def ideal_highpass_filter(shape, cutoff):
        return 1 - ideal_lowpass_filter(shape, cutoff)
    
    def butterworth_highpass_filter(shape, cutoff, order):
        return 1 - butterworth_lowpass_filter(shape, cutoff, order)
    
    def gaussian_highpass_filter(shape, cutoff):
        return 1 - gaussian_lowpass_filter(shape, cutoff)
    
    # Apply filters
    cutoff = 50
    order = 2
    
    # Low-pass filtering
    ideal_lp = ideal_lowpass_filter(img.shape, cutoff)
    butterworth_lp = butterworth_lowpass_filter(img.shape, cutoff, order)
    gaussian_lp = gaussian_lowpass_filter(img.shape, cutoff)
    
    # High-pass filtering
    ideal_hp = ideal_highpass_filter(img.shape, cutoff)
    butterworth_hp = butterworth_highpass_filter(img.shape, cutoff, order)
    gaussian_hp = gaussian_highpass_filter(img.shape, cutoff)
    
    # Apply filters to frequency domain
    filtered_ideal_lp = f_shift * ideal_lp
    filtered_butterworth_lp = f_shift * butterworth_lp
    filtered_gaussian_lp = f_shift * gaussian_lp
    
    filtered_ideal_hp = f_shift * ideal_hp
    filtered_butterworth_hp = f_shift * butterworth_hp
    filtered_gaussian_hp = f_shift * gaussian_hp
    
    # Convert back to spatial domain
    def ifft_and_real(f_filtered):
        f_ishift = np.fft.ifftshift(f_filtered)
        img_back = np.fft.ifft2(f_ishift)
        return np.real(img_back).astype(np.uint8)
    
    # Low-pass results
    result_ideal_lp = ifft_and_real(filtered_ideal_lp)
    result_butterworth_lp = ifft_and_real(filtered_butterworth_lp)
    result_gaussian_lp = ifft_and_real(filtered_gaussian_lp)
    
    # High-pass results
    result_ideal_hp = ifft_and_real(filtered_ideal_hp)
    result_butterworth_hp = ifft_and_real(filtered_butterworth_hp)
    result_gaussian_hp = ifft_and_real(filtered_gaussian_hp)
    
    # Display results
    plt.figure(figsize=(20, 15))
    
    # Original and FFT
    plt.subplot(4, 4, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(4, 4, 2)
    plt.imshow(np.log(np.abs(f_shift) + 1), cmap='gray')
    plt.title('FFT Magnitude Spectrum')
    plt.axis('off')
    
    # Low-pass filters and results
    filters_lp = [ideal_lp, butterworth_lp, gaussian_lp]
    results_lp = [result_ideal_lp, result_butterworth_lp, result_gaussian_lp]
    titles_lp = ['Ideal LP', 'Butterworth LP', 'Gaussian LP']
    
    for i in range(3):
        plt.subplot(4, 4, 5 + i)
        plt.imshow(filters_lp[i], cmap='gray')
        plt.title(f'{titles_lp[i]} Filter')
        plt.axis('off')
        
        plt.subplot(4, 4, 9 + i)
        plt.imshow(results_lp[i], cmap='gray')
        plt.title(f'{titles_lp[i]} Result')
        plt.axis('off')
    
    # High-pass filters and results
    filters_hp = [ideal_hp, butterworth_hp, gaussian_hp]
    results_hp = [result_ideal_hp, result_butterworth_hp, result_gaussian_hp]
    titles_hp = ['Ideal HP', 'Butterworth HP', 'Gaussian HP']
    
    for i in range(3):
        plt.subplot(4, 4, 6 + i)
        plt.imshow(filters_hp[i], cmap='gray')
        plt.title(f'{titles_hp[i]} Filter')
        plt.axis('off')
        
        plt.subplot(4, 4, 10 + i)
        plt.imshow(results_hp[i], cmap='gray')
        plt.title(f'{titles_hp[i]} Result')
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return {
        'lowpass': {
            'ideal': result_ideal_lp,
            'butterworth': result_butterworth_lp,
            'gaussian': result_gaussian_lp
        },
        'highpass': {
            'ideal': result_ideal_hp,
            'butterworth': result_butterworth_hp,
            'gaussian': result_gaussian_hp
        }
    }

# Usage
if __name__ == "__main__":
    filtered_images = frequency_domain_filtering('profile.jpg')
    
    # Save filtered images
    for filter_type, images in filtered_images.items():
        for name, img in images.items():
            cv2.imwrite(f'{filter_type}_{name}.jpg', img)