import cv2
import numpy as np
import matplotlib.pyplot as plt  # For alternative display method

# Load the images
img_rgb = cv2.imread(r'DCMY_INTERNS\farees\Photos\original_spectacle.jpg')
# img_rgb = cv2.imread(r'DCMY_INTERNS\farees\Photos\rotated.jpg')
# img_rgb = cv2.imread(r'C:DCMY_INTERNS\farees\Photos\translation.jpg')
# img_rgb = cv2.imread(r'DCMY_INTERNS\farees\Photos\none.jpg')

if img_rgb is None:
    print("Error: Original image not found.")
    exit()

template = cv2.imread(r'DCMY_INTERNS\farees\Photos\spectacle.jpeg', 0)
if template is None:
    print("Error: Template image not found.")
    exit()

# Convert original image to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# Template matching
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
print(f"Threshold value: {threshold}")
loc = np.where(res >= threshold)

# Draw rectangles around matches and calculate centers
centers = []  # List to store centers
for pt in zip(*loc[::-1]):
    # Draw rectangle
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    
    # Calculate center
    center_x = pt[0] + w // 2
    center_y = pt[1] + h // 2
    centers.append((center_x, center_y))

# Print the last center coordinates (latest detected object)
if centers:
    center_x, center_y = centers[-1]  # Get the last center
    print(f"Detected object center: (X: {center_x}, Y: {center_y})")

# Add a message to the image if no objects are detected
if not centers:
    print("No objects detected.")
    cv2.putText(img_rgb, "No objects detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 0, 255), 2, cv2.LINE_AA)

# If centers are detected, display the last center coordinates in the image
if centers:
    center_x, center_y = centers[-1]  # Get the last center
    # Display the center at a fixed location (e.g., top-left corner)
    cv2.putText(img_rgb, f"({center_x}, {center_y})", (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)

# Save the result image
output_path = r'DCMY_INTERNS\farees\Results\detected.jpg'
cv2.imwrite(output_path, img_rgb)
print(f"Image saved successfully at: {output_path}")

# Display the image
try:
    # Option 1: Using OpenCV (if GUI support is available)
    cv2.imshow('Template Matching', img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except cv2.error as e:
    print("cv2.imshow is not supported in your environment. Using matplotlib instead.")

    # Option 2: Using matplotlib (works in all environments)
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)  # Convert color for matplotlib
    plt.imshow(img_rgb)
    plt.title("Template Matching")
    
    # Display center coordinates of the last match (if detected)
    if centers:
        # Display the last center only
        center_x, center_y = centers[-1]
        plt.text(center_x, center_y, f"({center_x}, {center_y})", color='yellow', fontsize=10, 
                 bbox=dict(facecolor='blue', alpha=0.5))
    plt.axis('off')  # Hide axes
    plt.show()
