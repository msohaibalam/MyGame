import pygame

#import random

pygame.init()

# setup screen
size_x = 700
size_y = 500
size = (size_x,size_y)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sobi's Cool Game")

# declare colors
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
Yellow = (255,255,51)
White = (255,255,255)
Black = (0,0,0)

done = False
clock = pygame.time.Clock()

# rectangle movement
delta_x = -0.5
delta_y = 0.3
width = 55
height = 55
rect_x = 0 #random.randrange(0,size_x - width)
rect_y = 50 #random.randrange(0,size_y - height)

# make sticky figure
def sticky(x,y):
	#head
	pygame.draw.ellipse(screen,Black,[x,y,15,15])
	#body
	pygame.draw.line(screen,Black,[x+7.5,y],[x+7.5,y+28],2)
	#arms
	pygame.draw.line(screen,Black,[x+7.5,y+20],[x+22,y+18],2)
	pygame.draw.line(screen,Black,[x+7.5,y+20],[x-7.5,y+18],2)
	#legs
	pygame.draw.line(screen,Black,[x+7.5,y+28],[x+16,y+(28+12)],2)
	pygame.draw.line(screen,Black,[x+7.5,y+28],[x+7.5-(16-7.5),y+(28+12)],2)
	
# sticky location
x_coord = size_x - 40
y_coord = size_y - 60
x_change = 0
y_change = 0

# Fire!
fire_x = size_x + 50 #x_coord
fire_y = size_y + 50 #y_coord
fire_x_change = 0

# Text -- FAIL
font = pygame.font.SysFont('Calibri', 25, True, False)
text_fail = font.render("FAIL!",True,Black)

# Text -- Score
score = 0

while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x_change = -5
			if event.key == pygame.K_RIGHT:
				x_change = 5
			if event.key == pygame.K_UP:
				y_change = -5
			if event.key == pygame.K_DOWN:
				y_change = 	5
			if event.key == pygame.K_SPACE:
				fire_x = x_coord
				fire_y = y_coord
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				x_change = 0
			if event.key == pygame.K_RIGHT:
				x_change = 0
			if event.key == pygame.K_UP:
				y_change = 0
			if event.key == pygame.K_DOWN:
				y_change = 	0
			if event.key == pygame.K_SPACE:
				fire_x_change = 15	
				
	screen.fill(Red)
	
	## sticky movement
	sticky(x_coord,y_coord)
	x_coord += x_change
	y_coord += y_change
	# restrict within screen
	if x_coord<10:
		x_coord = 10
		x_change = 0
	if x_coord>size_x-25:
		x_coord = size_x - 25
		x_change = 0
	if y_coord<0:
		y_coord = 0
		y_change = 0
	if y_coord>size_y-40:
		y_coord = size_y-40
		y_change = 0
	
	# rect movement
	pygame.draw.rect(screen, Blue, [rect_x,rect_y,width,height])
	rect_x += delta_x
	rect_y += delta_y
	
	# bounce rect
	if rect_x > 700 - width or rect_x <0:
		delta_x *= -1
	if rect_y > 500 - height or rect_y <0:
		delta_y *= -1
	
	# collision -- sticky and rect
	x_collide = (x_coord >= rect_x) and (x_coord < rect_x + width)
	y_collide = (y_coord >= rect_y) and (y_coord < rect_y + height)
	collide = x_collide and y_collide
	
	if collide:
		score -= 5
		for i in range(30):
			screen.blit(text_fail, [size_x/2,size_y/2])
		
	# Fire
	fire_x += fire_x_change
	pygame.draw.rect(screen, Yellow, [fire_x,fire_y,30,5])
	
	# collision -- fire and rect
	x_kaboom = (fire_x >= rect_x) and (fire_x < rect_x + width)
	y_kaboom = (fire_y >= rect_y) and (fire_y < rect_y + height)
	kaboom = x_kaboom and y_kaboom
	
	speed_change = 0.2
	
	if kaboom:
		score += 1
		if delta_x >= 0:
			delta_x += speed_change #random.choice(speed_change)
		elif delta_x < 0:
			delta_x -= speed_change #random.choice(speed_change)
		if delta_y >= 0:
			delta_y += speed_change #random.choice(speed_change)
		elif delta_y < 0:
			delta_y -= speed_change #random.choice(speed_change)
	
	# Display score
	text_score = font.render("Score: " + str(score),True,Black)
	screen.blit(text_score, [size_x - 150, 20])
	
	## Level up --- TODO
	#if score >= 10:
	#	sticky(50,50)
	
	pygame.display.flip()
	
	clock.tick(60)

pygame.quit()