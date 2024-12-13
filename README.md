# Serpent Strike 

Introduction:<br>
This project involves the design and implementation of a 2D interactive game using OpenGL, focusing on gameplay mechanics, graphical representation, and real-time user interaction. The game offers a unique twist on traditional snake games, challenging the player to avoid obstacles and earn upgrades to survive for as long as possible.

Gameplay Elements:<br>
Player-Controlled Ball: Drawn using the Midpoint Circle Algorithm, moves via keyboard input to avoid obstacles.<br>
Snakes: Represented as lines drawn using the Midpoint Line Algorithm, spawning randomly from screen edges and moving in straight lines.<br>
Increasing Difficulty: As the player crosses certain point thresholds, the snakes' speed increases to make the game more challenging.

Collision Effects:<br>
The ball grows in size and loses health upon collision with snakes.<br>
Points are awarded for each snake successfully avoided (crossing the screen).

Upgrades and Projectiles:<br>
Points unlock upgrades, enabling the ball to shoot projectiles (small circles) to eliminate snakes for additional points.

Scoring System:<br>
Points are earned by avoiding snakes or hitting them with projectiles.<br>
Score thresholds unlock new abilities for the player and increase the game's difficulty.
