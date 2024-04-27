import pygame
import random
from math import sin, cos, radians

pygame.init()

window_size = [1200, 800]

screen = pygame.display.set_mode(window_size)
f = 360

cam_x = 0
cam_y = 0
cam_z = 0

cx_rot = 0
cy_rot = 0


def z_rot(x, y, ox, oy, angle):
	angle = radians(angle)
	qx = ox + cos(angle) * (x - ox) - sin(angle) * (y - oy)
	qy = oy + sin(angle) * (x - ox) + cos(angle) * (y - oy)

	return [qx, qy]

def x_rot(y, z, oy, oz, angle):
	angle = radians(angle)
	qy = oy + cos(angle) * (y - oy) - sin(angle) * (z - oz)
	qz = oz + sin(angle) * (y - oy) + cos(angle) * (z - oz)

	return [qy, qz]

def y_rot(z, x, oz, ox, angle):
	angle = radians(angle)
	qz = oz + cos(angle) * (z - oz) - sin(angle) * (x - ox)
	qx = ox + sin(angle) * (z - oz) + cos(angle) * (x - ox)

	return [qz, qx]


class Point:
	def __init__(self, pos):
		self.pos = pos

	def render(self):
		rx = self.pos[0]
		ry = self.pos[1]
		rz = self.pos[2]

		rz, rx = y_rot(rz, rx, cam_z, cam_x, cy_rot)
		ry, rz = x_rot(ry, rz, cam_y, cam_z, cx_rot)
		rx, ry = z_rot(rx, ry, cam_x, cam_y, 0)

		if rz-cam_z > 0:
			screen_x = (rx-cam_x)/(rz-cam_z)*f +window_size[0]/2
			screen_y = (ry-cam_y)/(rz-cam_z)*f +window_size[1]/2
			size = 1/(rz-cam_z)*f
			pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), size)


points = [Point([x, y, z]) for x in range(0, 100, 10) for y in range(0, 100, 10) for z in range(0, 100, 10)]

while 1:
	screen.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			pass

	keys = pygame.key.get_pressed()
	if keys[pygame.K_x]:
		cam_y -= 1
	if keys[pygame.K_z]:
		cam_y += 1


	if keys[pygame.K_w]:
		cam_x -= sin(radians(cy_rot))
		cam_z += cos(radians(cy_rot))
	if keys[pygame.K_s]:
		cam_x += sin(radians(cy_rot))
		cam_z -= cos(radians(cy_rot))
	if keys[pygame.K_a]:
		cam_x -= cos(radians(cy_rot))
		cam_z -= sin(radians(cy_rot))
	if keys[pygame.K_d]:
		cam_x += cos(radians(cy_rot))
		cam_z += sin(radians(cy_rot))


	if keys[pygame.K_j]:
		cy_rot += 1
	if keys[pygame.K_l]:
		cy_rot -= 1
	if keys[pygame.K_i]:
		cx_rot -= 1
	if keys[pygame.K_k]:
		cx_rot += 1


	for point in points:
		point.render()

	pygame.display.update()