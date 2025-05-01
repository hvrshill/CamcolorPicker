import cv2
import numpy as np
import pyperclip

# Store color info
clicked_color = (0, 0, 0)
color_text = "Click to pick color"

# Mouse callback to pick color
def pick_color(event, x, y, flags, param):
    global clicked_color, color_text
    if event == cv2.EVENT_LBUTTONDOWN:
        r, g, b = frame[y, x]
        clicked_color = (int(r), int(g), int(b))
        color_text = f"RGB({clicked_color[0]}, {clicked_color[1]}, {clicked_color[2]})"
        pyperclip.copy(color_text)
        print("Color picked:", color_text)

# Open camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("Color Picker")
cv2.setMouseCallback("Color Picker", pick_color)

while True:
    ret, raw_frame = cap.read()
    if not ret:
        break

    # Convert frame once, use everywhere
    frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

    # Check if window is still open
    if cv2.getWindowProperty("Color Picker", cv2.WND_PROP_VISIBLE) < 1:
        break

    # Draw color bar
    display_frame = frame.copy()
    cv2.rectangle(display_frame, (0, 0), (display_frame.shape[1], 50), clicked_color, -1)
    
    # Adjust text color for visibility
    text_color = (0, 0, 0) if sum(clicked_color) > 400 else (255, 255, 255)
    cv2.putText(display_frame, color_text, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    # Convert back to BGR for display
    display_frame = cv2.cvtColor(display_frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("Color Picker", display_frame)

    # Exit on 'q' or close window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
