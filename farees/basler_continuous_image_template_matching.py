from pypylon import pylon
import cv2
import numpy as np

# Load the template
template = cv2.imread(r'C:\Users\Predator\Desktop\Bosch_Rexroth\DCMY_INTERNS\farees\Photos\metal_block.png', 0)
if template is None:
    print("Error: Template image not found.")
    exit()

# Template dimensions
w, h = template.shape[::-1]

# Connecting to the first available Basler camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Start grabbing video frames
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

# Configure the converter to output OpenCV-compatible BGR format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Threshold for template matching
threshold = 0.80
print(f"Threshold value: {threshold}")

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Convert the image to an OpenCV-compatible format
        image = converter.Convert(grabResult)
        frame = image.GetArray()

        # Convert the frame to grayscale
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
        cv2.namedWindow('Template Matching with Basler Camera', cv2.WINDOW_NORMAL)
        cv2.imshow('Template Matching with Basler Camera', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        grabResult.Release()
    else:
        print("Error: Failed to grab frame.")

# Release camera resources
camera.StopGrabbing()
cv2.destroyAllWindows()
