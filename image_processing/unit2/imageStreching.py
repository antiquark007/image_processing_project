import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load grayscale image
img = cv2.imread('profile.jpg', 0)

# Contrast stretching
r_min, r_max = np.min(img), np.max(img)
stretched = ((img - r_min) / (r_max - r_min) * 255).astype(np.uint8)

# Display
# plt.subplot(1,2,1); plt.title('Original'); plt.imshow(img, cmap='gray')
# plt.subplot(1,2,2); plt.title('Contrast Stretched'); plt.imshow(stretched, cmap='gray')
# plt.show()

# histogramEquilizer
# equalized = cv2.equalizeHist(img)

# plt.subplot(1,2,1); plt.title('Original'); plt.imshow(img, cmap='gray')
# plt.subplot(1,2,2); plt.title('Histogram Equalized'); plt.imshow(equalized, cmap='gray')
# plt.show()


# Spatial filters modify a pixel based on its neighbors using a kernel (mask).

# 🔹 a. Smoothing Filters (Noise Reduction)
blur = cv2.blur(img, (5,5))  # 5x5 mean filter
plt.imshow(blur, cmap='gray')

gaussian = cv2.GaussianBlur(img, (5,5), 1)
plt.imshow(gaussian, cmap='gray')

