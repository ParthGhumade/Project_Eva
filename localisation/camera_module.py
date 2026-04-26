from PIL import Image
import pygame

img = Image.open('image2.png')
w, h = img.size
pixels = img.load()

pygame.init()

w = img.width
h = img.height

screen = pygame.display.set_mode((w, h))

cutoff = 100

for i in range(0, w):
	for j in range(0, h):
		r, g, b = pixels[i, j]
		if r < cutoff and g < cutoff and b < cutoff:
			screen.set_at((i, j), (r, g, b))
		else:
			screen.set_at((i, j), (255, 255, 255))

pygame.display.flip()

while True:
	pass