import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Ant Colony')

# Define colors
background_color = (210, 180, 140)  # Tan color in RGB format
WHITE = (255, 255, 255)  # Define WHITE color

# Load the sprite images
player_image = pygame.image.load('C:\\Users\\katie\\OneDrive\\Documents\\ant3.png').convert_alpha()
draggable_image = pygame.image.load('C:\\Users\\katie\\OneDrive\\Documents\\blueberry.png').convert_alpha()  # Change this path to your draggable object image
anthill_image = pygame.image.load('C:\\Users\\katie\\OneDrive\\Documents\\ant_hill.png').convert_alpha()  # Change this path to your anthill image

# Create a Player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dragging = None

    def update(self, keys_pressed, draggable_sprites):
        speed = 0.6
        # Handle key presses
        if pygame.K_LEFT in keys_pressed and keys_pressed[pygame.K_LEFT]:
            self.rect.x -= speed
        if pygame.K_RIGHT in keys_pressed and keys_pressed[pygame.K_RIGHT]:
            self.rect.x += speed
        if pygame.K_UP in keys_pressed and keys_pressed[pygame.K_UP]:
            self.rect.y -= speed
        if pygame.K_DOWN in keys_pressed and keys_pressed[pygame.K_DOWN]:
            self.rect.y += speed

        # Ensure the player stays within screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen.get_width(), self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(screen.get_height(), self.rect.bottom)

        # Handle dragging
        if self.dragging:
            self.dragging.rect.center = self.rect.center
            # Ensure the dragged object stays within screen bounds
            self.dragging.rect.left = max(0, self.dragging.rect.left)
            self.dragging.rect.right = min(screen.get_width(), self.dragging.rect.right)
            self.dragging.rect.top = max(0, self.dragging.rect.top)
            self.dragging.rect.bottom = min(screen.get_height(), self.dragging.rect.bottom)


# Create a DraggableObject sprite class
class DraggableObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = draggable_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create an AntHill sprite class
class AntHill(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = anthill_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Function to check proximity
def is_near(player, obj, distance):
    return player.rect.colliderect(pygame.Rect(obj.rect.left - distance, obj.rect.top - distance, obj.rect.width + 2 * distance, obj.rect.height + 2 * distance))

# Create sprite instances
player = Player(100, 100)
draggable1 = DraggableObject(300, 300)  # First blueberry object
draggable2 = DraggableObject(400, 400)  # Second blueberry object
draggable3 = DraggableObject(500, 300)
draggable4 = DraggableObject(600, 200)  # First blueberry object
draggable5 = DraggableObject(700, 100)  # Second blueberry object
draggable6 = DraggableObject(750,450)
anthill = AntHill(500, 500)

# Create sprite groups
all_sprites = pygame.sprite.Group(player, draggable1, draggable2, draggable3, draggable4, draggable5, draggable6, anthill)  # Include draggable2
draggable_sprites = pygame.sprite.Group(draggable1, draggable2, draggable3, draggable4, draggable5, draggable6)  # Include draggable2 in draggable_sprites
anthill_sprites = pygame.sprite.Group(anthill)


# Score variables
score = 0
font = pygame.font.Font(None, 36)  # Font for displaying the score
keys_pressed = {}
# Main game loop
# Main game loop
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Toggle picking up or dropping the object
                if player.dragging:
                    player.dragging = None
                else:
                    for sprite in draggable_sprites:
                        if is_near(player, sprite, 50):  # 50 is the proximity threshold
                            player.dragging = sprite
                            break
            elif event.key == pygame.K_w:
                keys_pressed[pygame.K_UP] = True
            elif event.key == pygame.K_a:
                keys_pressed[pygame.K_LEFT] = True
            elif event.key == pygame.K_s:
                keys_pressed[pygame.K_DOWN] = True
            elif event.key == pygame.K_d:
                keys_pressed[pygame.K_RIGHT] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys_pressed[pygame.K_UP] = False
            elif event.key == pygame.K_a:
                keys_pressed[pygame.K_LEFT] = False
            elif event.key == pygame.K_s:
                keys_pressed[pygame.K_DOWN] = False
            elif event.key == pygame.K_d:
                keys_pressed[pygame.K_RIGHT] = False


    # Update all sprites
    all_sprites.update(keys_pressed, draggable_sprites)

    # Check for collision between the draggable object and the ant hill
    if player.dragging and pygame.sprite.spritecollide(player.dragging, anthill_sprites, False):
        draggable_sprites.remove(player.dragging)
        all_sprites.remove(player.dragging)
        player.dragging = None
        score += 1

    # Draw everything
    screen.fill(background_color)
    all_sprites.draw(screen)

    # Display the score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
