import cv2
import numpy as np
import pygame

# Init
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("OPENCV + Pygame")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load filter image once
glasses_img = pygame.image.load("TheCyborgs.png").convert_alpha()

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = np.rot90(frame_rgb)
    surface = pygame.surfarray.make_surface(frame_rgb)

    screen.blit(surface, (0, 0))

    # Now overlay the glasses for each face
    for (x, y, w, h) in faces:
        scaled_glasses = pygame.transform.scale(glasses_img, (w, h // 3))
        screen.blit(scaled_glasses, (x, y + h // 4))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
