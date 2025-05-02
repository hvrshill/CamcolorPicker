import cv2  # OpenCV library for computer vision tasks
import numpy as np  # NumPy library for numerical operations (not directly used here)
import pyperclip  # Library to copy text to the clipboard

# Store color info
clicked_color = (0, 0, 0)  # Default color (black)
color_text = "Click to pick color"  # Default text to display

# Mouse callback to pick color
def pick_color(event, x, y, flags, param):
    """
    This function is triggered when a mouse event occurs in the "Color Picker" window.
    If the left mouse button is clicked, it captures the color of the pixel at (x, y)
    and updates the global variables `clicked_color` and `color_text`.
    """
    global clicked_color, color_text  # Access global variables
    if event == cv2.EVENT_LBUTTONDOWN:  # Check if the left mouse button was clicked
        r, g, b = frame[y, x]  # Get the RGB values of the pixel at (x, y)
        clicked_color = (int(r), int(g), int(b))  # Update the clicked color
        color_text = f"RGB({clicked_color[0]}, {clicked_color[1]}, {clicked_color[2]})"  # Format the color as text
        pyperclip.copy(color_text)  # Copy the color text to the clipboard
        print("Color picked:", color_text)  # Print the picked color to the console

# Open camera
cap = cv2.VideoCapture(0)  # Initialize the camera (default camera index 0)
cv2.namedWindow("Color Picker")  # Create a window named "Color Picker"
cv2.setMouseCallback("Color Picker", pick_color)  # Set the mouse callback for the window

# Main loop to capture and process frames from the camera
while True:
    ret, raw_frame = cap.read()  # Capture a frame from the camera
    if not ret:  # If no frame is captured, exit the loop
        break

    # Convert frame once, use everywhere
    frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)  # Convert the frame from BGR to RGB format

    # Check if window is still open
    if cv2.getWindowProperty("Color Picker", cv2.WND_PROP_VISIBLE) < 1:  # Check if the window is still open
        break

    # Draw color bar
    display_frame = frame.copy()  # Create a copy of the frame to modify for display
    cv2.rectangle(display_frame, (0, 0), (display_frame.shape[1], 50), clicked_color, -1)  
    # Draw a rectangle (color bar) at the top of the frame, filled with the clicked color

    # Adjust text color for visibility
    text_color = (0, 0, 0) if sum(clicked_color) > 400 else (255, 255, 255)  
    # Use black text for bright colors and white text for dark colors
    cv2.putText(display_frame, color_text, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)  
    # Display the RGB color text on the color bar

    # Convert back to BGR for display
    display_frame = cv2.cvtColor(display_frame, cv2.COLOR_RGB2BGR)  # Convert the frame back to BGR for OpenCV display
    cv2.imshow("Color Picker", display_frame)  # Show the frame in the "Color Picker" window

    # Exit on 'q' or close window
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Check if the 'q' key is pressed
        break

# Cleanup
cap.release()  # Release the camera resource
cv2.destroyAllWindows()  # Close all OpenCV windows