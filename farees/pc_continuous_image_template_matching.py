import cv2
import numpy as np

# Load the template
template = cv2.imread(r'C:\Users\Predator\Desktop\Bosch_Rexroth\DCMY_INTERNS\farees\Photos\black_temp.png', 0)
if template is None:
    print("Error: Template image not found.")
    exit()

# Template dimensions
w, h = template.shape[::-1]

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for the default camera
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Threshold for template matching
threshold = 0.8
print(f"Threshold value: {threshold}")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from the camera.")
        break

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # Draw rectangles around matches and calculate centers
    centers = []
    for pt in zip(*loc[::-1]):
        # Draw rectangle
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        # Calculate center
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        centers.append((center_x, center_y))

    # Display the last detected center (if any)
    if centers:
        center_x, center_y = centers[-1]
        cv2.putText(frame, f"({center_x}, {center_y})", (center_x, center_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    # Display a message if no objects are detected
    if not centers:
        cv2.putText(frame, "No objects detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the frame with detected matches
    cv2.imshow('Template Matching', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
