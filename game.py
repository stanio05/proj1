"""
Catch and Avoid Game
A simple game where the player controls a footballer using hand gestures,
collecting balls and avoiding red cards.
"""

import pygame
import cv2
import mediapipe as mp
import random
import sys
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)

# Game settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
BALL_RADIUS = 20
RED_CARD_WIDTH = 30
RED_CARD_HEIGHT = 45
INITIAL_HEALTH = 3
SPAWN_INTERVAL = 60  # frames
FALL_SPEED = 3


class HandTracker:
    """Handles hand tracking using MediaPipe and OpenCV"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(0)
        self.hand_x = 0.5  # Normalized position (0 to 1)
        
    def update(self) -> bool:
        """Update hand position from camera"""
        ret, frame = self.cap.read()
        if not ret:
            return False
            
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            # Get first hand
            hand_landmarks = results.multi_hand_landmarks[0]
            # Use index finger tip (landmark 8) for position
            index_finger = hand_landmarks.landmark[8]
            self.hand_x = index_finger.x
            
        # Draw landmarks on frame for debugging
        if results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.multi_hand_landmarks[0],
                self.mp_hands.HAND_CONNECTIONS
            )
        
        # Show camera feed
        cv2.imshow('Hand Tracking', frame)
        cv2.waitKey(1)
        
        return True
    
    def get_player_x(self, screen_width: int) -> int:
        """Convert normalized hand position to screen coordinates"""
        return int(self.hand_x * screen_width)
    
    def close(self):
        """Release camera and close windows"""
        self.cap.release()
        cv2.destroyAllWindows()


class Player:
    """Player character (footballer)"""
    
    def __init__(self, x: int, y: int):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, x: int):
        """Update player position based on hand tracking"""
        self.x = x - self.width // 2
        # Keep player within screen bounds
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))
        self.rect.x = self.x
        
    def draw(self, screen):
        """Draw player as a simple footballer sprite"""
        # Body (blue shirt)
        pygame.draw.rect(screen, BLUE, self.rect)
        # Head (skin color)
        head_rect = pygame.Rect(self.x + 12, self.y - 15, 26, 20)
        pygame.draw.ellipse(screen, (255, 220, 177), head_rect)
        # Feet
        foot1 = pygame.Rect(self.x + 8, self.y + self.height, 15, 8)
        foot2 = pygame.Rect(self.x + 27, self.y + self.height, 15, 8)
        pygame.draw.rect(screen, BLACK, foot1)
        pygame.draw.rect(screen, BLACK, foot2)


class Ball:
    """Collectible ball object"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.speed = FALL_SPEED
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                                self.radius * 2, self.radius * 2)
        
    def update(self):
        """Move ball downward"""
        self.y += self.speed
        self.rect.y = self.y - self.radius
        
    def draw(self, screen):
        """Draw ball as a circle with soccer ball pattern"""
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 2)
        # Pentagon pattern
        for i in range(5):
            angle = i * 72
            x_offset = int(self.radius * 0.3 * pygame.math.Vector2(1, 0).rotate(angle).x)
            y_offset = int(self.radius * 0.3 * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.circle(screen, BLACK, (self.x + x_offset, self.y + y_offset), 
                             self.radius // 4)
        
    def is_off_screen(self) -> bool:
        """Check if ball is below screen"""
        return self.y > WINDOW_HEIGHT + self.radius


class RedCard:
    """Red card obstacle to avoid"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = RED_CARD_WIDTH
        self.height = RED_CARD_HEIGHT
        self.speed = FALL_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self):
        """Move red card downward"""
        self.y += self.speed
        self.rect.y = self.y
        
    def draw(self, screen):
        """Draw red card"""
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, (139, 0, 0), self.rect, 3)  # Dark red border
        
    def is_off_screen(self) -> bool:
        """Check if card is below screen"""
        return self.y > WINDOW_HEIGHT + self.height


class Game:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Catch and Avoid - Piłkarz")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.running = True
        self.game_over = False
        self.score = 0
        self.health = INITIAL_HEALTH
        self.frame_count = 0
        
        # Initialize hand tracker
        self.hand_tracker = HandTracker()
        
        # Initialize player
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        
        # Game objects
        self.balls: List[Ball] = []
        self.red_cards: List[RedCard] = []
        
    def spawn_objects(self):
        """Spawn balls and red cards at intervals"""
        if self.frame_count % SPAWN_INTERVAL == 0:
            # Spawn ball (70% chance) or red card (30% chance)
            x = random.randint(30, WINDOW_WIDTH - 30)
            if random.random() < 0.7:
                self.balls.append(Ball(x, -BALL_RADIUS))
            else:
                self.red_cards.append(RedCard(x, -RED_CARD_HEIGHT))
                
    def check_collisions(self):
        """Check collisions between player and objects"""
        player_rect = self.player.rect
        
        # Check ball collisions
        for ball in self.balls[:]:
            if player_rect.colliderect(ball.rect):
                self.balls.remove(ball)
                self.score += 1
                
        # Check red card collisions
        for card in self.red_cards[:]:
            if player_rect.colliderect(card.rect):
                self.red_cards.remove(card)
                self.health -= 1
                if self.health <= 0:
                    self.game_over = True
                    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
        # Update hand tracking
        if not self.hand_tracker.update():
            print("Failed to get camera frame")
            self.running = False
            return
            
        # Update player position from hand tracking
        player_x = self.hand_tracker.get_player_x(WINDOW_WIDTH)
        self.player.update(player_x)
        
        # Spawn new objects
        self.spawn_objects()
        
        # Update all balls
        for ball in self.balls[:]:
            ball.update()
            if ball.is_off_screen():
                self.balls.remove(ball)
                
        # Update all red cards
        for card in self.red_cards[:]:
            card.update()
            if card.is_off_screen():
                self.red_cards.remove(card)
                
        # Check collisions
        self.check_collisions()
        
        self.frame_count += 1
        
    def draw(self):
        """Draw all game objects"""
        # Background
        self.screen.fill(GREEN)
        
        # Draw grass pattern
        for i in range(0, WINDOW_HEIGHT, 40):
            color = (0, 200, 0) if (i // 40) % 2 == 0 else (0, 180, 0)
            pygame.draw.rect(self.screen, color, (0, i, WINDOW_WIDTH, 40))
        
        # Draw all objects
        for ball in self.balls:
            ball.draw(self.screen)
            
        for card in self.red_cards:
            card.draw(self.screen)
            
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen if needed
        if self.game_over:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def draw_ui(self):
        """Draw score and health"""
        # Score
        score_text = self.font.render(f"Wynik: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)
        # Draw black background for better readability
        pygame.draw.rect(self.screen, BLACK, score_rect.inflate(20, 10))
        self.screen.blit(score_text, score_rect)
        
        # Health
        health_text = self.font.render(f"Zdrowie: {self.health}", True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topright = (WINDOW_WIDTH - 10, 10)
        pygame.draw.rect(self.screen, BLACK, health_rect.inflate(20, 10))
        self.screen.blit(health_text, health_rect)
        
        # Instructions
        instruction_text = self.small_font.render(
            "Poruszaj dłonią aby sterować piłkarzem", True, WHITE
        )
        instruction_rect = instruction_text.get_rect()
        instruction_rect.midtop = (WINDOW_WIDTH // 2, 10)
        pygame.draw.rect(self.screen, BLACK, instruction_rect.inflate(20, 10))
        self.screen.blit(instruction_text, instruction_rect)
        
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font.render("KONIEC GRY!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Końcowy Wynik: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Naciśnij R aby zagrać ponownie lub Q aby wyjść", 
                                              True, YELLOW)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                    
    def reset_game(self):
        """Reset game to initial state"""
        self.game_over = False
        self.score = 0
        self.health = INITIAL_HEALTH
        self.frame_count = 0
        self.balls.clear()
        self.red_cards.clear()
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        self.cleanup()
        
    def cleanup(self):
        """Clean up resources"""
        self.hand_tracker.close()
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    print("Uruchamianie gry Catch and Avoid...")
    print("Upewnij się, że kamera jest podłączona i działa.")
    print("Poruszaj dłonią przed kamerą aby sterować piłkarzem.")
    print()
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
