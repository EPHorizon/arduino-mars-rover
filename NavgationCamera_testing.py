import pygame
import pygame.camera
import pygame.image

pygame.camera.init()

cam = pygame.camera.Camera(pygame.camera.list_cameras()[1])
cam.start()

img = cam.get_image()
pygame.image.save(img, "test.png")
pygame.camera.quit()
