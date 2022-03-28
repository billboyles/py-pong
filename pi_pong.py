import pygame, sys, random

def ball_move(ball_speed_x, ball_speed_y):	
	#update location 
	ball.x += ball_speed_x
	ball.y += ball_speed_y 

	#check for collisions with x walls, bounce
	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1
	
	#check for collisions with y walls, reset
	if ball.left <= 0 or ball.right >= screen_width:
		#left side
		if ball.left <= 0:
			inc_score_opponent()
		#right side
		if ball.right >= screen_width:
			inc_score_player()
		
		#move to center, get new direction
		new_ball_speed = tipoff(ball_speed_x, ball_speed_y)
		ball_speed_x = new_ball_speed[0]
		ball_speed_y = new_ball_speed[1]
		
		#pause .5 secs
		pygame.time.wait(500)

	#check for collisions with paddles
	if ball.colliderect(player) and ball_speed_x < 0:		
		if abs(ball.left - player.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
			
	if ball.colliderect(opponent) and ball_speed_x > 0:
		if abs(ball.right - opponent.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10  and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	return (ball_speed_x, ball_speed_y)

def player_move(player_speed):
	#update location
	player.y += player_speed

	#check for collisions
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_move(opponent_speed):	
	#update location by moving towards ball
	if opponent.top < ball.y:
		opponent.top += opponent_speed
	if opponent.bottom > ball.y:
		opponent.bottom -= opponent_speed

	#check for collisions
	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

def tipoff(ball_speed_x, ball_speed_y):
	global main_font

	#move to center
	ball.center = ((screen_width / 2), (screen_height / 2))

	wait()

	#get new random direction
	ball_speed_x *= random.choice((1, -1)) 
	ball_speed_y *= random.choice((1, -1))		

	return (ball_speed_x, ball_speed_y)

def wait():
	#loop for space bar
	while True:

		#handle input
		for event in pygame.event.get():
			#quit
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			#key down
			if event.type == pygame.KEYDOWN:
				#q key or esc key to quit
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

				#space key to start/resume
				if event.key == pygame.K_SPACE:
					return
					
		#background
		screen.fill(black)

		#center line
		pygame.draw.aaline(screen, gray, ((screen_width / 2), 0), ((screen_width / 2), screen_height))

		#center circle
		pygame.draw.circle(screen, gray, (screen_width / 2, screen_height / 2), 200, width=1)

		#goal lines
		pygame.draw.aaline(screen, gray, (20, 0), (20, screen_height))
		pygame.draw.aaline(screen, gray, ((screen_width - 20), 0), ((screen_width - 20), screen_height))
		
		#score
		draw_score_text(player_score, opponent_score)

		#paddles
		pygame.draw.rect(screen, blue, player)
		pygame.draw.rect(screen, red, opponent)
		
		#ball
		pygame.draw.ellipse(screen, green, ball)

		#draw tipoff text
		tipoff_text = main_font.render(f"PRESS SPACE TO START", True, gray)
		tipoff_rect = tipoff_text.get_rect(center=((screen.get_width() / 2), ((screen.get_height() / 2) - 60)))
		screen.blit(tipoff_text, tipoff_rect)

		#paddles
		pygame.draw.rect(screen, blue, player)
		pygame.draw.rect(screen, red, opponent)
	
		#ball
		pygame.draw.ellipse(screen, green, ball)

		#update window
		pygame.display.flip()
		clock.tick(60)

def draw_score_text(player_score, opponent_score):
	score_text = main_font.render(f"{player_score} {opponent_score}", True, gray)
	score_rect = score_text.get_rect(center=((screen.get_width() / 2), (screen.get_height() - 100)))
	screen.blit(score_text, score_rect)

def inc_score_player():
	global player_score
	player_score += 1

def inc_score_opponent():
	global opponent_score
	opponent_score += 1

def title_text():
	#background
	screen.fill(black)

	#center line
	pygame.draw.aaline(screen, gray, ((screen_width / 2), 0), ((screen_width / 2), screen_height))

	#center circle
	pygame.draw.circle(screen, gray, (screen_width / 2, screen_height / 2), 200, width=1)

	#goal lines
	pygame.draw.aaline(screen, gray, (20, 0), (20, screen_height))
	pygame.draw.aaline(screen, gray, ((screen_width - 20), 0), ((screen_width - 20), screen_height))

	#paddles
	pygame.draw.rect(screen, blue, player)
	pygame.draw.rect(screen, red, opponent)

	#draw title text
	title_text = title_font.render(f"PI PONG", True, gray)
	title_rect = title_text.get_rect(center=((screen.get_width() / 2), ((screen.get_height() / 2) - 120)))
	screen.blit(title_text, title_rect)

	#draw small text
	small_text = small_font.render(f"by Bill Boyles", True, gray)
	small_rect = small_text.get_rect(center=((screen.get_width() / 2), ((screen.get_height() / 2) + 50)))
	screen.blit(small_text, small_rect)

	#paddles
	pygame.draw.rect(screen, blue, player)
	pygame.draw.rect(screen, red, opponent)

	#ball
	pygame.draw.ellipse(screen, green, ball)

	#update window
	pygame.display.flip()
	clock.tick(60)

	pygame.time.wait(3000)


#inital setup
pygame.init()
clock = pygame.time.Clock()

#get screen size
display_size = pygame.display.Info()

#set screen to match display
screen_width = display_size.current_w
screen_height = display_size.current_h - 60

#create pygame display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pi Pong')

#game items
ball = pygame.Rect(((screen_width / 2) - 15), ((screen_height / 2) - 15), 30, 30)
player = pygame.Rect(15, ((screen_height / 2) - 75), 20, 200)
opponent = pygame.Rect((screen_width - 30), ((screen_height / 2) - 75), 20, 200)

#colors
green = (50, 255, 50)
blue = (50, 50, 255)
red = (255, 50, 50)
gray = (50, 50, 50)
black = (0, 0, 0)

#velocities
ball_speed_x = 8
ball_speed_y = 8
player_speed = 0
opponent_speed = 10

#scores
player_score = 0
opponent_score = 0

#text
try:
	title_font = pygame.font.Font('Alien-Encounters-Regular.ttf', 300)
except:
	print("title font 'Alien-Encounters-Regular.ttf' not found, using default text")
	title_font = pygame.font.Font(None, 300)

try:
	main_font = pygame.font.SysFont('couriernew', 100)
except:
	print("main font 'Courier New' not found, using default text")
	main_font = pygame.font.SysFont(None, 100)

try:
	small_font = pygame.font.SysFont('couriernew', 50)
except:
	print("small font 'Courier New' not found, using default text")
	small_font = pygame.font.SysFont(None, 100)

#title text
title_text()

#tipoff
ball_speed_x, ball_speed_y = tipoff(ball_speed_x, ball_speed_y)

while True:
	#handle input
	for event in pygame.event.get():
		
		#quit
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#key down 
		if event.type == pygame.KEYDOWN:
			#down key to move down
			if event.key == pygame.K_DOWN:
				player_speed += 5

			#up key to move up
			if event.key == pygame.K_UP:
				player_speed -= 5

			#q key or esc key to quit
			if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

			#space key to pause
			if event.key == pygame.K_SPACE:
				wait()

		#key up
		if event.type == pygame.KEYUP:
			#down key to stop moving down
			if event.key == pygame.K_DOWN:
				player_speed = 0
			
			#up key to stop moving up
			if event.key == pygame.K_UP:
				player_speed = 0

	#move ball, update speed
	ball_speed_x, ball_speed_y = ball_move(ball_speed_x, ball_speed_y)

	#move player
	player_move(player_speed)

	#move opponent
	opponent_move(opponent_speed)

	#drawing
	#background
	screen.fill(black)

	#center line
	pygame.draw.aaline(screen, gray, ((screen_width / 2), 0), ((screen_width / 2), screen_height))

	#center circle
	pygame.draw.circle(screen, gray, (screen_width / 2, screen_height / 2), 200, width=1)

	#goal lines
	pygame.draw.aaline(screen, gray, (20, 0), (20, screen_height))
	pygame.draw.aaline(screen, gray, ((screen_width - 20), 0), ((screen_width - 20), screen_height))
	
	#score
	draw_score_text(player_score, opponent_score)

	#paddles
	pygame.draw.rect(screen, blue, player)
	pygame.draw.rect(screen, red, opponent)
	
	#ball
	pygame.draw.ellipse(screen, green, ball)
	
	#update window
	pygame.display.flip()
	clock.tick(60)



