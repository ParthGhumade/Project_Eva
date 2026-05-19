import cv2
import time

# Initialize the camera. '0' is usually the built-in or default USB camera port.
# If you are using a Raspberry Pi Camera Module, ensure legacy camera support is enabled.
cap = cv2.VideoCapture(0)

# Check if the camera opened correctly
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

print("Camera initialized successfully! Press Ctrl+C in the terminal to stop.")

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Can't receive frame. Exiting...")
            break

        # Save the current frame as a static image file
        cv2.imwrite('live_feed.jpg', frame)
        
        # Print a small heartbeat to the terminal so you know it's working
        print(".", end="", flush=True)

        # Wait 0.1 seconds (captures roughly 10 frames per second)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping camera feed...")

# Always release the camera resource when done
cap.release()
print("Camera released cleanly.")