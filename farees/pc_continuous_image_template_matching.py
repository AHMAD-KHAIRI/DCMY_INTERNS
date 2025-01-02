import cv2
import numpy as np

# Load the reference image
reference_image = cv2.imread(r'C:\Users\Predator\Desktop\Bosch_Rexroth\DCMY_INTERNS\farees\Photos\spectacle.jpeg')

# Convert reference image to grayscale
gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

# Initialize SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors for the entire reference image
keypoints_reference, descriptors_reference = sift.detectAndCompute(gray_reference, None)

# Convert descriptors to CV_32F type
descriptors_reference = descriptors_reference.astype(np.float32)

# Get the dimensions of the reference image for tracking
h, w = gray_reference.shape

# Initialize the camera or video stream
cap = cv2.VideoCapture(0)

# Initialize the BFMatcher
bf = cv2.BFMatcher()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and compute descriptors for the frame
    keypoints_frame, descriptors_frame = sift.detectAndCompute(gray_frame, None)

    # Convert descriptors to CV_32F type if not None
    if descriptors_frame is not None:
        descriptors_frame = descriptors_frame.astype(np.float32)

        # Match descriptors between the frame and the reference image
        matches = bf.knnMatch(descriptors_reference, descriptors_frame, k=2)

        # Apply ratio test to find good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Calculate homography
        if len(good_matches) > 10:
            src_pts = np.float32([keypoints_reference[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_frame[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is not None:
                # Calculate bounding box for the tracked object
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                frame = cv2.polylines(frame, [np.int32(dst)], True, (0, 255, 0), 2)

    # Display the frame with the tracked object
    cv2.imshow('Object Tracking', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
