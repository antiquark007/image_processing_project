import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

class ImageEnhancementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Enhancement Toolkit")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.original_image = None
        self.current_image = None
        self.image_path = None
        
        # Create main interface
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Enhancement Toolkit", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Controls
        self.create_control_panel(main_frame)
        
        # Right panel - Image display
        self.create_image_panel(main_frame)
        
    def create_control_panel(self, parent):
        # Control panel frame
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # File operations
        file_frame = ttk.LabelFrame(control_frame, text="File Operations", padding="5")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(file_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Reset", command=self.reset_image).grid(row=0, column=2, padx=5, pady=5)
        
        # Point Processing
        point_frame = ttk.LabelFrame(control_frame, text="Point Processing", padding="5")
        point_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(point_frame, text="Contrast Stretching", 
                  command=self.apply_contrast_stretching).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(point_frame, text="Histogram Equalization", 
                  command=self.apply_histogram_equalization).grid(row=0, column=1, padx=5, pady=5)
        
        # Spatial Filtering
        spatial_frame = ttk.LabelFrame(control_frame, text="Spatial Filtering", padding="5")
        spatial_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Smoothing filters
        smooth_subframe = ttk.Frame(spatial_frame)
        smooth_subframe.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(smooth_subframe, text="Smoothing:").grid(row=0, column=0, padx=5)
        ttk.Button(smooth_subframe, text="Mean Filter", 
                  command=lambda: self.apply_spatial_filter('mean')).grid(row=0, column=1, padx=2)
        ttk.Button(smooth_subframe, text="Gaussian Filter", 
                  command=lambda: self.apply_spatial_filter('gaussian')).grid(row=0, column=2, padx=2)
        ttk.Button(smooth_subframe, text="Median Filter", 
                  command=lambda: self.apply_spatial_filter('median')).grid(row=0, column=3, padx=2)
        
        # Kernel size control
        kernel_frame = ttk.Frame(spatial_frame)
        kernel_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(kernel_frame, text="Kernel Size:").grid(row=0, column=0, padx=5)
        self.kernel_size = tk.IntVar(value=5)
        kernel_scale = ttk.Scale(kernel_frame, from_=3, to=15, orient=tk.HORIZONTAL, 
                                variable=self.kernel_size, length=200)
        kernel_scale.grid(row=0, column=1, padx=5)
        ttk.Label(kernel_frame, textvariable=self.kernel_size).grid(row=0, column=2, padx=5)
        
        # Sharpening filters
        sharp_subframe = ttk.Frame(spatial_frame)
        sharp_subframe.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(sharp_subframe, text="Sharpening:").grid(row=0, column=0, padx=5)
        ttk.Button(sharp_subframe, text="Laplacian", 
                  command=lambda: self.apply_sharpening('laplacian')).grid(row=0, column=1, padx=2)
        ttk.Button(sharp_subframe, text="Unsharp Masking", 
                  command=lambda: self.apply_sharpening('unsharp')).grid(row=0, column=2, padx=2)
        ttk.Button(sharp_subframe, text="Custom Kernel", 
                  command=lambda: self.apply_sharpening('custom')).grid(row=0, column=3, padx=2)
        
        # Frequency Domain Filtering
        freq_frame = ttk.LabelFrame(control_frame, text="Frequency Domain Filtering", padding="5")
        freq_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Filter type selection
        filter_type_frame = ttk.Frame(freq_frame)
        filter_type_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(filter_type_frame, text="Filter Type:").grid(row=0, column=0, padx=5)
        self.filter_type = tk.StringVar(value="lowpass")
        ttk.Radiobutton(filter_type_frame, text="Low-Pass", variable=self.filter_type, 
                       value="lowpass").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(filter_type_frame, text="High-Pass", variable=self.filter_type, 
                       value="highpass").grid(row=0, column=2, padx=5)
        
        # Filter design
        filter_design_frame = ttk.Frame(freq_frame)
        filter_design_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(filter_design_frame, text="Design:").grid(row=0, column=0, padx=5)
        self.filter_design = tk.StringVar(value="gaussian")
        ttk.Radiobutton(filter_design_frame, text="Ideal", variable=self.filter_design, 
                       value="ideal").grid(row=0, column=1, padx=2)
        ttk.Radiobutton(filter_design_frame, text="Butterworth", variable=self.filter_design, 
                       value="butterworth").grid(row=0, column=2, padx=2)
        ttk.Radiobutton(filter_design_frame, text="Gaussian", variable=self.filter_design, 
                       value="gaussian").grid(row=0, column=3, padx=2)
        
        # Cutoff frequency control
        cutoff_frame = ttk.Frame(freq_frame)
        cutoff_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(cutoff_frame, text="Cutoff Frequency:").grid(row=0, column=0, padx=5)
        self.cutoff_freq = tk.IntVar(value=50)
        cutoff_scale = ttk.Scale(cutoff_frame, from_=10, to=200, orient=tk.HORIZONTAL, 
                                variable=self.cutoff_freq, length=200)
        cutoff_scale.grid(row=0, column=1, padx=5)
        ttk.Label(cutoff_frame, textvariable=self.cutoff_freq).grid(row=0, column=2, padx=5)
        
        ttk.Button(freq_frame, text="Apply Frequency Filter", 
                  command=self.apply_frequency_filter).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Analysis tools
        analysis_frame = ttk.LabelFrame(control_frame, text="Analysis", padding="5")
        analysis_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(analysis_frame, text="Show Histogram", 
                  command=self.show_histogram).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(analysis_frame, text="Show FFT Spectrum", 
                  command=self.show_fft_spectrum).grid(row=0, column=1, padx=5, pady=5)
        
    def create_image_panel(self, parent):
        # Image display frame
        image_frame = ttk.LabelFrame(parent, text="Image Display", padding="10")
        image_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 8), facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, image_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for image frame
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)
        
        # Initially show empty plot
        self.update_display()
        
    def load_image(self):
        """Load an image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif")]
        )
        
        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.original_image is not None:
                self.current_image = self.original_image.copy()
                self.update_display()
                messagebox.showinfo("Success", "Image loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load image!")
                
    def save_image(self):
        """Save the current image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            cv2.imwrite(file_path, self.current_image)
            messagebox.showinfo("Success", "Image saved successfully!")
            
    def reset_image(self):
        """Reset to original image"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.update_display()
            
    def apply_contrast_stretching(self):
        """Apply contrast stretching"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        r_min = np.min(self.current_image)
        r_max = np.max(self.current_image)
        stretched = ((self.current_image - r_min) * (255.0 / (r_max - r_min))).astype(np.uint8)
        self.current_image = stretched
        self.update_display()
        
    def apply_histogram_equalization(self):
        """Apply histogram equalization"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        equalized = cv2.equalizeHist(self.current_image)
        self.current_image = equalized
        self.update_display()
        
    def apply_spatial_filter(self, filter_type):
        """Apply spatial filtering"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        kernel_size = int(self.kernel_size.get())
        if kernel_size % 2 == 0:  # Ensure odd kernel size
            kernel_size += 1
            
        if filter_type == 'mean':
            result = cv2.blur(self.current_image, (kernel_size, kernel_size))
        elif filter_type == 'gaussian':
            result = cv2.GaussianBlur(self.current_image, (kernel_size, kernel_size), 1.0)
        elif filter_type == 'median':
            result = cv2.medianBlur(self.current_image, kernel_size)
            
        self.current_image = result
        self.update_display()
        
    def apply_sharpening(self, method):
        """Apply sharpening filters"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        if method == 'laplacian':
            laplacian = cv2.Laplacian(self.current_image, cv2.CV_64F)
            result = np.absolute(laplacian).astype(np.uint8)
        elif method == 'unsharp':
            gaussian_blur = cv2.GaussianBlur(self.current_image, (9, 9), 10.0)
            result = cv2.addWeighted(self.current_image, 1.5, gaussian_blur, -0.5, 0)
        elif method == 'custom':
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            result = cv2.filter2D(self.current_image, -1, kernel)
            
        self.current_image = result
        self.update_display()
        
    def apply_frequency_filter(self):
        """Apply frequency domain filtering"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        rows, cols = self.current_image.shape
        
        # FFT
        f_transform = np.fft.fft2(self.current_image)
        f_shift = np.fft.fftshift(f_transform)
        
        # Create filter
        crow, ccol = rows // 2, cols // 2
        y, x = np.ogrid[:rows, :cols]
        d = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
        
        cutoff = self.cutoff_freq.get()
        filter_type = self.filter_type.get()
        filter_design = self.filter_design.get()
        
        if filter_design == 'ideal':
            if filter_type == 'lowpass':
                mask = (d <= cutoff).astype(float)
            else:
                mask = (d > cutoff).astype(float)
        elif filter_design == 'gaussian':
            if filter_type == 'lowpass':
                mask = np.exp(-(d ** 2) / (2 * (cutoff ** 2)))
            else:
                mask = 1 - np.exp(-(d ** 2) / (2 * (cutoff ** 2)))
        elif filter_design == 'butterworth':
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
        
        self.current_image = result
        self.update_display()
        
    def show_histogram(self):
        """Show histogram in a new window"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Create new window for histogram
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Histogram")
        hist_window.geometry("600x400")
        
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.hist(self.current_image.ravel(), bins=256, range=[0, 256], alpha=0.7)
        ax.set_xlabel('Pixel Intensity')
        ax.set_ylabel('Frequency')
        ax.set_title('Image Histogram')
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, hist_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def show_fft_spectrum(self):
        """Show FFT spectrum in a new window"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Create new window for FFT spectrum
        fft_window = tk.Toplevel(self.root)
        fft_window.title("FFT Magnitude Spectrum")
        fft_window.geometry("600x400")
        
        # Compute FFT
        f_transform = np.fft.fft2(self.current_image)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.log(np.abs(f_shift) + 1)
        
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        im = ax.imshow(magnitude_spectrum, cmap='gray')
        ax.set_title('FFT Magnitude Spectrum (Log Scale)')
        ax.axis('off')
        fig.colorbar(im, ax=ax)
        
        canvas = FigureCanvasTkAgg(fig, fft_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_display(self):
        """Update the image display"""
        self.fig.clear()
        
        if self.current_image is not None:
            ax1 = self.fig.add_subplot(121)
            ax1.imshow(self.original_image, cmap='gray')
            ax1.set_title('Original Image')
            ax1.axis('off')
            
            ax2 = self.fig.add_subplot(122)
            ax2.imshow(self.current_image, cmap='gray')
            ax2.set_title('Enhanced Image')
            ax2.axis('off')
        else:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Load an image to start', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=16)
            ax.axis('off')
            
        self.fig.tight_layout()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = ImageEnhancementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()