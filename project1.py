from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Window dimensions
window_width = 800
window_height = 600

# Game variables
ball_x = window_width // 2
ball_y = window_height // 2
ball_radius = 20
ball_speed = 10
health = 50
score = 0
snakes = []  # List of snakes
projectiles = []  # Projectiles shot by the ball
upgrade = False  # Ball upgrade status
game_over = False
is_paused = False
game_started = False  # To check if the game has started
diff = False
curvy_threshold = 5  # Snakes start moving curvy after reaching this score

shield = {"x": -1, "y": -1, "size": 30, "active": False, "timer": 0}

# Start button dimensions
start_button_x = window_width // 2 - 45
start_button_y = window_height // 2 +10
start_button_width = 100
start_button_height = 50
# Exit button dimensions
exit_button_x = window_width // 2 - 45
exit_button_y = window_height // 2 - 70  # Positioned below the start button
exit_button_width = 100
exit_button_height = 50

#Restart Button

restart_button_x = window_width // 2 - 45
restart_button_y = window_height // 2 +20
restart_button_width = 100
restart_button_height = 50

#Main Menu Button 
mm_button_x = window_width // 2 - 45
mm_button_y = window_height // 2 - 60  # Positioned below the start button
mm_button_width = 100
mm_button_height = 50
#exit from restart menu
exitr_button_x = window_width // 2 - 45
exitr_button_y = window_height // 2 - 70 -70 # Positioned below the start button
exitr_button_width = 100
exitr_button_height = 50

# Drawing a pixel
def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Midpoint Circle Algorithm
def draw_circle(xc, yc, r):
    x, y = 0, r
    d = 1 - r
    circle_points(xc, yc, x, y)
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        circle_points(xc, yc, x, y)

def circle_points(xc, yc, x, y):
    points = [
        (xc + x, yc + y), (xc - x, yc + y),
        (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x),
        (xc + y, yc - x), (xc - y, yc - x)
    ]
    for point in points:
        draw_pixel(*point)
def draw_half_circle(xc, yc, r, direction):
    # Draw a half-circle based on the direction
    if direction == 'right':
        angle_start, angle_end = 0, 180
    elif direction == 'left':
        angle_start, angle_end = 180, 360
    elif direction == 'up':
        angle_start, angle_end = 90, 270
    elif direction == 'down':
        angle_start, angle_end = 270, 450

    for angle in range(angle_start, angle_end):
        rad = math.radians(angle)
        x = xc + r * math.cos(rad)
        y = yc + r * math.sin(rad)
        draw_pixel(int(x), int(y))
# Drawing a snake
def draw_snake(snake):
    # Define fixed dimensions for the snake
    body_length = 80  # Fixed length for the rectangle
    body_thickness = 20  # Fixed thickness for the rectangle

    # Determine the orientation based on movement direction
    if snake["dx"] != 0:  # Horizontal movement
        direction = 'horizontal'
        x1 = snake["x"] - body_length // 2
        x2 = snake["x"] + body_length // 2
        y1 = snake["y"] - body_thickness // 2
        y2 = snake["y"] + body_thickness // 2
    else:  # Vertical movement
        direction = 'vertical'

        x1 = snake["x"] - body_thickness // 2
        x2 = snake["x"] + body_thickness // 2
        y1 = snake["y"] - body_length // 2
        y2 = snake["y"] + body_length // 2

     # Set color to red for the snake body
    glColor3f(1.0, 0.0, 0.0)  # Red color
    
    if direction == 'horizontal':
       
        # Draw four half-circles for horizontal snake
        draw_half_circle(x1, (y1 + y2) // 2, body_thickness // 2, 'right')
        draw_half_circle((x1 + body_thickness), (y1 + y2) // 2, body_thickness // 2, 'left')
        draw_half_circle((x1 + body_thickness*2), (y1 + y2) // 2, body_thickness // 2, 'right')
        draw_half_circle((x1 + body_thickness*3), (y1 + y2) // 2, body_thickness // 2, 'left')
        draw_half_circle((x1 + body_thickness*4), (y1 + y2) // 2, body_thickness // 2, 'right')
    else:
        # Draw four half-circles for vertical snake
        draw_half_circle((x1 + x2) // 2, y1, body_thickness // 2, 'down')
        draw_half_circle((x1 + x2) // 2, (y1+body_thickness), body_thickness // 2, 'up')
        draw_half_circle((x1 + x2) // 2, (y1+body_thickness*2), body_thickness // 2, 'down')
        draw_half_circle((x1 + x2) // 2, (y1+body_thickness*3), body_thickness // 2, 'up')
        draw_half_circle((x1 + x2) // 2, (y1+body_thickness*4), body_thickness // 2, 'down')

    # Draw the circle head
    if snake["dx"] > 0:  # Moving right
        head_x = x2 + body_thickness 
        head_y = (y1 + y2) // 2
    elif snake["dx"] < 0:  # Moving left
        head_x = x1 - body_thickness 
        head_y = (y1 + y2) // 2
    elif snake["dy"] > 0:  # Moving up
        head_x = (x1 + x2) // 2
        head_y = y2 + body_thickness 
    else:  # Moving down
        head_x = (x1 + x2) // 2
        head_y = y1 - body_thickness

    glColor3f(1.0, 0.0, 0.0)  # Red color
    draw_circle(head_x, head_y, body_thickness // 2)

def spawn_snake(value=0):
    global game_started  # Ensure we spawn only after the game has started
    if game_started and not is_paused and not game_over:
        side = random.choice(['top', 'bottom', 'left', 'right'])
        size = random.randint(10, 30)
        speed = random.randint(2, 5)
        oscillation_speed = random.uniform(0.05, 0.2)

        if side == 'top':
            x = random.randint(0, window_width)
            y = window_height
            dx, dy = 0, -speed
        elif side == 'bottom':
            x = random.randint(0, window_width)
            y = 0
            dx, dy = 0, speed
        elif side == 'left':
            x = 0
            y = random.randint(0, window_height)
            dx, dy = speed, 0
        elif side == 'right':
            x = window_width
            y = random.randint(0, window_height)
            dx, dy = -speed, 0
        
        snake = {
            "x": x, 
            "y": y, 
            "size": size, 
            "dx": dx, 
            "dy": dy, 
            "time": 0,
            "oscillation_speed": oscillation_speed
        }
        snakes.append(snake)
    #     print(f"Snake added: {snake}")  # Log the snake added to the list
    # else:
    #     print("Not spawning snake, game state might be incorrect.")  # Log to verify the game state

    # Ensure we spawn snakes continuously
    glutTimerFunc(1000, spawn_snake, 0)

# Start button click detection
def start_button_click(x, y):
    global game_started, health, ball_radius, score
    if start_button_x <= x <= start_button_x + start_button_width and start_button_y <= y <= start_button_y + start_button_height:
        game_started = True
        
        ball_radius =20
        health = 50
        score = 0
        
        print("Game started!")  # Debugging line to check if start button works
        glutPostRedisplay()  # Refresh the screen to start the game
  # Refresh the screen to start the game
# Exit button click detection

def exit_button_click(x, y):
    global game_started
    # Check if the mouse click is within the bounds of the exit button
    if exit_button_x <= x <= exit_button_x + exit_button_width and exit_button_y <= y <= exit_button_y + exit_button_height:
        print(f"Exit button clicked at ({x}, {y})")  # Debugging line to verify click position
        print("Exiting game...")  # Debugging line
        glutLeaveMainLoop()  # This will exit the main GLUT loop and close the game
def exit_r_button_click(x, y):
    global game_started
    # Check if the mouse click is within the bounds of the exit button
    if exitr_button_x <= x <= exitr_button_x + exitr_button_width and exitr_button_y <= y <= exitr_button_y + exitr_button_height:
        print(f"Exit button clicked at ({x}, {y})")  # Debugging line to verify click position
        print("Exiting game...")  # Debugging line
        glutLeaveMainLoop()  # This will exit the main GLUT loop and close the game
def mm_button_click(x, y):
    global game_started, game_over, is_paused
    # Check if the mouse click is within the bounds of the exit button
    if mm_button_x <= x <= mm_button_x + mm_button_width and mm_button_y <= y <= mm_button_y + mm_button_height:
        print(f"Main Menu button clicked at ({x}, {y})")  # Debugging line to verify click position
        print("Going to Main Menu...")  # Debugging line
        game_started = False
        game_over = True
        is_paused = False
        glutPostRedisplay()  # This will exit the main GLUT loop and close the game
def restart_button_click(x, y):
    global game_started, game_over, is_paused, ball_radius, health, score, snakes
    # Check if the mouse click is within the bounds of the exit button
    if restart_button_x <= x <= restart_button_x + restart_button_width and restart_button_y <= y <= restart_button_y + restart_button_height:
        print(f"Restart button clicked at ({x}, {y})")  # Debugging line to verify click position
        print("Started...")  # Debugging line
        ball_radius =20
        health = 50
        score = 0
        if not is_paused:
            snakes.clear()
        game_started = True
        game_over = False
        is_paused = False
        glutPostRedisplay()  # This will exit the main GLUT loop and close the game
def resume_button_click(x, y):
    global game_started, game_over, is_paused
    # Check if the mouse click is within the bounds of the exit button
    if restart_button_x <= x <= restart_button_x + restart_button_width and restart_button_y <= y <= restart_button_y + restart_button_height:
        print(f"Resume button clicked at ({x}, {y})")  # Debugging line to verify click position
        print("Started...")  # Debugging line
        
        is_paused = False
        glutPostRedisplay()  # This will exit the main GLUT loop and close the game
  # This will exit the main GLUT loop and close the game
def restart():
    global game_started


def resume():
    global game_started


def game_pause():
    glColor3f(0.0, 1.0, 0)  # Blue for start button
    glBegin(GL_QUADS)
    glVertex2f(restart_button_x, restart_button_y)
    glVertex2f(restart_button_x + restart_button_width, restart_button_y)
    glVertex2f(restart_button_x + restart_button_width, restart_button_y + restart_button_height)
    glVertex2f(restart_button_x, restart_button_y + restart_button_height)
    glEnd()

    # Draw text "Start"
    glColor3f(1.0, 1.0, 1.0)  # White for the start text
    draw_text(window_width // 2 - 25, window_height // 2 + 40, "Resume")

    # Draw the exit button
    glColor3f(0.0, 0.0, 1.0)  # Red for exit button
    glBegin(GL_QUADS)
    glVertex2f(mm_button_x, mm_button_y)
    glVertex2f(mm_button_x + mm_button_width, mm_button_y)
    glVertex2f(mm_button_x + mm_button_width, mm_button_y + mm_button_height)
    glVertex2f(mm_button_x, mm_button_y + mm_button_height)
    glEnd()

    # Draw text "Exit"
    glColor3f(1.0, 1.0, 1.0)  # White text color for exit
    draw_text(window_width // 2 - 40, window_height // 2 - 40, "Main Menu")

    glColor3f(1.0, 0.0, 0.0)  # Red for exit button
    glBegin(GL_QUADS)
    glVertex2f(exitr_button_x, exitr_button_y)
    glVertex2f(exitr_button_x + exitr_button_width, exitr_button_y)
    glVertex2f(exitr_button_x + exitr_button_width, exitr_button_y + exitr_button_height)
    glVertex2f(exitr_button_x, exitr_button_y + exitr_button_height)
    glEnd()

    # Draw text "Exit"
    glColor3f(1.0, 1.0, 1.0)  # White text color for exit
    draw_text(window_width // 2 - 10, window_height // 2 - 120, "Exit")

def game_over_restart():
    glColor3f(0.0, 1.0, 0)  # Blue for start button
    glBegin(GL_QUADS)
    glVertex2f(restart_button_x, restart_button_y)
    glVertex2f(restart_button_x + restart_button_width, restart_button_y)
    glVertex2f(restart_button_x + restart_button_width, restart_button_y + restart_button_height)
    glVertex2f(restart_button_x, restart_button_y + restart_button_height)
    glEnd()

    # Draw text "Start"
    glColor3f(1.0, 1.0, 1.0)  # White for the start text
    draw_text(window_width // 2 - 25, window_height // 2 + 40, "Restart")

    # Draw the exit button
    glColor3f(0.0, 0.0, 1.0)  # Red for exit button
    glBegin(GL_QUADS)
    glVertex2f(mm_button_x, mm_button_y)
    glVertex2f(mm_button_x + mm_button_width, mm_button_y)
    glVertex2f(mm_button_x + mm_button_width, mm_button_y + mm_button_height)
    glVertex2f(mm_button_x, mm_button_y + mm_button_height)
    glEnd()

    # Draw text "Exit"
    glColor3f(1.0, 1.0, 1.0)  # White text color for exit
    draw_text(window_width // 2 - 40, window_height // 2 - 40, "Main Menu")

    glColor3f(1.0, 0.0, 0.0)  # Red for exit button
    glBegin(GL_QUADS)
    glVertex2f(exitr_button_x, exitr_button_y)
    glVertex2f(exitr_button_x + exitr_button_width, exitr_button_y)
    glVertex2f(exitr_button_x + exitr_button_width, exitr_button_y + exitr_button_height)
    glVertex2f(exitr_button_x, exitr_button_y + exitr_button_height)
    glEnd()

    # Draw text "Exit"
    glColor3f(1.0, 1.0, 1.0)  # White text color for exit
    draw_text(window_width // 2 - 10, window_height // 2 - 120, "Exit")




def draw_start_screen():

    glColor3f(1.0, 1.0, 1.0)  # White for the title text
    draw_text(window_width // 2 - 60, window_height // 2 + 150, "Serpent Strike", font=GLUT_BITMAP_TIMES_ROMAN_24)



    # Draw the start button
    glColor3f(0.0, 1.0, 0)  # Blue for start button
    glBegin(GL_QUADS)
    glVertex2f(start_button_x, start_button_y)
    glVertex2f(start_button_x + start_button_width, start_button_y)
    glVertex2f(start_button_x + start_button_width, start_button_y + start_button_height)
    glVertex2f(start_button_x, start_button_y + start_button_height)
    glEnd()

    # Draw text "Start"
    glColor3f(1.0, 1.0, 1.0)  # White for the start text
    draw_text(window_width // 2 - 25, window_height // 2 + 25, "START")

    # Draw the exit button
    glColor3f(1.0, 0.0, 0.0)  # Red for exit button
    glBegin(GL_QUADS)
    glVertex2f(exit_button_x, exit_button_y)
    glVertex2f(exit_button_x + exit_button_width, exit_button_y)
    glVertex2f(exit_button_x + exit_button_width, exit_button_y + exit_button_height)
    glVertex2f(exit_button_x, exit_button_y + exit_button_height)
    glEnd()

    # Draw text "Exit"
    glColor3f(1.0, 1.0, 1.0)  # White text color for exit
    draw_text(window_width // 2 - 17, window_height // 2 - 50, "EXIT")


# Game update logic
def update(value):
    global ball_x, ball_y, ball_radius, health, score, upgrade, game_over, shield

    if game_over or is_paused or not game_started:
        glutTimerFunc(30, update, 0)
        return
    
    # Check if shield should appear
    if score >= 5 and (score == 5 or (score - 5) % 15 == 0) and not shield["active"]:
        shield["x"] = random.randint(0, window_width - shield["size"])
        shield["y"] = random.randint(0, window_height - shield["size"])
        shield["active"] = True

    # Handle shield timer
    if shield["timer"] > 0:
        shield["timer"] -= 1
        if shield["timer"] <= 0:
            shield["active"] = False

    # Update snakes
    for snake in snakes[:]:
        # Increment time for sine wave (only used for curvy movement)
        snake["time"] += snake["oscillation_speed"]

        if score >= curvy_threshold:
            # Gradual amplitude: Increases every 5 points after curvy_threshold
            amplitude = min(((score - curvy_threshold) // 5) * 1.5, 25)  # Cap at 25
            if snake["dx"] != 0:  # Moving horizontally
                snake["x"] += snake["dx"]
                snake["y"] = max(0, min(window_height, snake["y"] + math.sin(snake["time"]) * amplitude))
            else:  # Moving vertically
                snake["y"] += snake["dy"]
                snake["x"] = max(0, min(window_width, snake["x"] + math.sin(snake["time"]) * amplitude))
        else:
 
            snake["x"] += snake["dx"]
            snake["y"] += snake["dy"]

        # Check if snake crosses the screen
        if snake["x"] < 0 or snake["x"] > window_width or snake["y"] < 0 or snake["y"] > window_height:
            snakes.remove(snake)
            score += 1
            if score >= 10:  # Upgrade threshold
                upgrade = True
        
        # Check collision with the ball
        if not shield["timer"]:  # Only check collision if shield is inactive
            if math.hypot(snake["x"] - ball_x, snake["y"] - ball_y) < ball_radius + snake["size"] // 2:
                health -= 10
                ball_radius += 2  # Ball grows larger
                snakes.remove(snake)
                if health <= 0:
                    game_over = True

    # Update projectiles
    for projectile in projectiles[:]:
        projectile["x"] += projectile["dx"] * 5
        projectile["y"] += projectile["dy"] * 5

        # Remove projectiles that leave the screen
        if projectile["x"] < 0 or projectile["x"] > window_width or projectile["y"] < 0 or projectile["y"] > window_height:
            projectiles.remove(projectile)
            continue

        # Check collision with snakes
        for snake in snakes[:]:
            if math.hypot(projectile["x"] - snake["x"], projectile["y"] - snake["y"]) < snake["size"]:
                snakes.remove(snake)
                projectiles.remove(projectile)
                score += 1
                break
    
    # Check collision with shield
    if shield["active"] and shield["x"] <= ball_x <= shield["x"] + shield["size"] and \
            shield["y"] <= ball_y <= shield["y"] + shield["size"]:
        shield["timer"] = 300  # Shield active for 10 seconds (300 frames at 30 FPS)
        shield["active"] = False

    glutPostRedisplay()  # Make sure this is called to redraw the screen
    glutTimerFunc(30, update, 0)


# Drawing the display
# Game update logic to display game over screen
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    if not game_started:
        draw_start_screen()
    else:
        # Draw the ball
        if shield["timer"] > 0:
            # Outer blue circle for shield
            glColor3f(0.0, 0.5, 1.0)  # Blue for the shield
            draw_circle(ball_x, ball_y, ball_radius + 5)  # Slightly larger than the ball
            
        glColor3f(0.0, 1.0, 0.0)  # Green for ball
        draw_circle(ball_x, ball_y, ball_radius)

        # Draw snakes
        glColor3f(1.0, 0.0, 0.0)  # Red for snakes
        for snake in snakes:
            draw_snake(snake)

        # Draw projectiles
        glColor3f(1.0, 1.0, 1.0)  # White for projectiles
        for projectile in projectiles:
            draw_circle(projectile["x"], projectile["y"], 5)

        # Draw the shield power-up
        if shield["active"]:
            glColor3f(0.0, 0.5, 1.0)  # Blue for the shield power-up
            glBegin(GL_QUADS)
            glVertex2f(shield["x"], shield["y"])
            glVertex2f(shield["x"] + shield["size"], shield["y"])
            glVertex2f(shield["x"] + shield["size"], shield["y"] + shield["size"])
            glVertex2f(shield["x"], shield["y"] + shield["size"])
            glEnd()

        # Display health and score
        glColor3f(1.0, 1.0, 0.0)  # Yellow
        draw_text(10, window_height - 30, f"Score: {score}")
        draw_text(10, window_height - 50, f"Health: {health}")

        if game_over:
            # Draw the Game Over text
            draw_text(window_width // 2 - 70, window_height // 2 + 180, "GAME OVER", font=GLUT_BITMAP_TIMES_ROMAN_24)
            
            # Show the last score
            draw_text(window_width // 2 - 60, window_height // 2+130, f"Last Score: {score}", font=GLUT_BITMAP_TIMES_ROMAN_24)
            
            # Display "Returning to Menu" message
            # draw_text(window_width // 2 - 120, window_height // 2 - 50, "Click to Return to Main Menu", font=GLUT_BITMAP_TIMES_ROMAN_24)
            game_over_restart()
        if is_paused:
            game_pause()
    glutSwapBuffers()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

# Mouse input for throwing projectiles or clicking buttons
def mouse_input(button, state, x, y):
    global projectiles, game_started, game_over, score, health, ball_radius
    # Convert y-coordinate to OpenGL coordinates (inverted)
    mouse_y = window_height - y  # Convert to OpenGL y-axis orientation
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:  # Only respond to button press
        click_y = window_height - y
        print(f"Mouse click detected at ({x}, {click_y})")  # Debugging line
        
        if not game_started:
            start_button_click(x, click_y)
            exit_button_click(x, click_y)
        else:
            if game_over:

                exit_r_button_click(x, click_y)
                mm_button_click(x, click_y)
                
                restart_button_click(x, click_y)
            elif is_paused:
                exit_r_button_click(x, click_y)
                mm_button_click(x, click_y)
                
                resume_button_click(x, click_y)
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if game_over:
            # Check "Exit" button on the Game Over screen
            if exitr_button_x <= x <= exitr_button_x + exitr_button_width and \
                    exitr_button_y <= y <= exitr_button_y + exitr_button_height:
                print(f"Game Over Exit button clicked at ({x}, {y})")
                print("Exiting game from Game Over screen...")
                glutLeaveMainLoop()  # Exit the game
            # If the game is over and a click occurs, restart the game and go back to the menu
            game_over = False
            score = 0
            health = 50
            ball_radius = 20
            snakes.clear()  # Clear the snakes
            projectiles.clear()  # Clear the projectiles
            game_started = False  # Reset the game start state
            glutPostRedisplay()  # Refresh the screen to display the start menu
        elif game_started:
            if upgrade:
                # Calculate direction vector from ball to mouse click position
                mouse_x = x
                dx = mouse_x - ball_x
                dy = mouse_y - ball_y
                magnitude = math.sqrt(dx**2 + dy**2)
                if magnitude > 0:
                    dx /= magnitude  # Normalize direction vector
                    dy /= magnitude
                # Add projectile
                projectiles.append({"x": ball_x, "y": ball_y, "dx": dx, "dy": dy})
        # else:
        #     # Check if the start button is clicked
        #     start_button_click(x, mouse_y)
        #     # Check if the exit button is clicked
        #     exit_button_click(x, mouse_y)  # Corrected to use mouse_y
        #     exit_r_button_click(x, mouse_y)


# Keyboard input
def keyboard_input(key, x, y):
    global ball_x, ball_y, is_paused, diff
    if key == b'w':  # Move up
        ball_y = min(window_height, ball_y + ball_speed)
    elif key == b's':  # Move down
        ball_y = max(0, ball_y - ball_speed)
    elif key == b'a':  # Move left
        ball_x = max(0, ball_x - ball_speed)
    elif key == b'd':  # Move right
        ball_x = min(window_width, ball_x + ball_speed)
    elif key == b'p':  # Toggle pause
        is_paused = not is_paused
        diff = False
        if is_paused:
            game_pause()
    glutPostRedisplay()

# Initialization
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(2)
    glutTimerFunc(30, update, 0)  # Start the update loop
    glutTimerFunc(1000, spawn_snake, 0)  # Make sure this is here to start snake spawning

# Main program
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Serpent Strike")
glOrtho(0, window_width, 0, window_height, -1, 1)
init()
glutDisplayFunc(display)
glutMouseFunc(mouse_input)
glutKeyboardFunc(keyboard_input)
glutMainLoop()