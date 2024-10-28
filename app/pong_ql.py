import pygame
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Variables
TRAINING = True
if TRAINING:
    MAX_SCORE = 5
    FPS = 480
else:
    MAX_SCORE = 11
    FPS = 60
COLOR = (139,23,137)
WHITE = (255,255,255)
PDL_WIDTH = 10
PDL_HEIGHT = 100
WIDTH = 840
HEIGHT = 600
PDL_SPEED = 10
RADIUS = 10
SIMPLE_AI_SPEED = 7

class Ball(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, RADIUS):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.RADIUS = RADIUS
        self.width = width  
        self.height = height
        self.velocity = [np.random.randint(2, 5), np.random.randint(-4, 5)]
 
        # Draw the ball (a circle)
        pygame.draw.circle(self.image, color, (self.width // 2, self.height //2), self.RADIUS)
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]
    
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = np.random.uniform(-4, 5)

class AI:
    def __init__(self):
        # Initialize the paddle position to some default value, e.g., middle of the canvas
        self.paddle_y = 200  # Adjust this based on your canvas height and paddle size

    def decide_move(self, ball_position):
        # Example logic to move the paddle based on ball position
        if ball_position['y'] > self.paddle_y + 50:
            self.paddle_y = min(self.paddle_y + 5, 400 - 100)  # Move down within bounds
        elif ball_position['y'] < self.paddle_y:
            self.paddle_y = max(self.paddle_y - 5, 0)  # Move up within bounds
        return self.paddle_y


class Paddle(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, hight, name, alpha=0.4, gamma=0.7, epsilon_decay=0.00001,epsilon_min=0.01, epsilon=1):
        # Call the parent class (Sprite) constructor
        super().__init__()

        global TRAINING
        
        # Pass in the color of the paddle, and its x and y position, width and hight.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, hight])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.hight = hight
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.q_table = {}

        self.rewards, self.episodes, self.average = [], [], []
        self.name = name
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.hight])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
    
    def moveUp(self, pixels):
        self.rect.y -= pixels
		#Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
	    #Check that you are not going too far (off the screen)
        if self.rect.y > (HEIGHT - self.hight):
          self.rect.y = (HEIGHT - self.hight)

    def simple_ai(self, ball_pos_y, pixels):
        if ball_pos_y + RADIUS > self.rect.y + PDL_HEIGHT / 2:
            self.rect.y += pixels
        if ball_pos_y + RADIUS < self.rect.y + PDL_HEIGHT /2:
            self.rect.y -= pixels

        if self.rect.y < 0:
          self.rect.y = 0
        if self.rect.y > (HEIGHT - self.hight):
          self.rect.y = (HEIGHT - self.hight)
    
    def epsilon_greedy(self):
        self.epsilon = max(self.epsilon_min, self.epsilon*(1 - self.epsilon_decay))
    
    def get_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(3)

        if TRAINING:
            self.epsilon_greedy()

            if np.random.uniform() < self.epsilon:
                action = np.random.choice(3)
            else:
                action = np.argmax(self.q_table[state])
        else:
            action = np.argmax(self.q_table[state])
        return action
    
    def update_q_table(self, state, action, reward, next_state):
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(3)
        td_target = reward + self.gamma * np.max(self.q_table[next_state])
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error
    
    def save(self, episode):
        with open(f'player_{self.name}_{episode}_qtable.pkl', 'wb') as file:
            pickle.dump(self.q_table, file)

    def load(self, name):
        with open(name, 'rb') as file:
            self.q_table = pickle.load(file)

    def plot_model(self, reward, episode):
        self.rewards.append(reward)
        self.episodes.append(episode)
        self.average.append(sum(self.rewards) / len(self.rewards))
        plt.plot(self.episodes, self.average, 'r')
        plt.plot(self.episodes, self.rewards, 'b')
        plt.ylabel('Reward', fontsize=18)
        plt.xlabel('Games', fontsize=18)

        try:
            plt.savefig(f'player_{self.name}_evolution.png')
        except OSError as e:
            print(f"Error saving file: {e}")

class Game:
    def __init__(self, player_a, player_b):

        pygame.init()  # Initialize Pygame modules

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CameBush Pong")

        self.paddle_a = player_a
        self.paddle_a.rect.x = 0
        self.paddle_a.rect.y = (HEIGHT - PDL_HEIGHT) // 2

        self.paddle_b = player_b
        self.paddle_b.rect.x = WIDTH - PDL_WIDTH
        self.paddle_b.rect.y = (HEIGHT - PDL_HEIGHT) // 2

        self.ball = Ball(COLOR, 2 * RADIUS, 2 * RADIUS, RADIUS)
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = HEIGHT // 2

        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.paddle_a, self.paddle_b, self.ball)

        self.finish = False
        self.clock = pygame.time.Clock()

        self.score_a, self.score_b = 0, 0
        self.reward = 0

        
    def get_reward(self):
        max_reward = PDL_HEIGHT // 2
        min_reward = -max_reward

        # Get the absolute y_distance between the paddle and ball centers
        y_distance = abs(self.paddle_a.rect.centery - self.ball.rect.centery)

        # Calculate the reward based on a decreasing function
        reward = - (y_distance / HEIGHT) * max_reward
        if y_distance < PDL_HEIGHT // 2:
            reward += max_reward  # Positive reward for proximity to center

        return max(min_reward, reward)
    
    def distille_state(self):
        if (self.paddle_a.rect.centery - RADIUS <= self.ball.rect.centery <= self.paddle_a.rect.y + RADIUS):
            distilled_state = 0  # Ball's y-value center is within range of the paddle's y-value center
        elif self.ball.rect.centery < self.paddle_a.rect.centery:
            distilled_state = 1  # Ball's y-value center is less than the paddle's y-value center
        else:
            distilled_state = 2  # Ball's y-value center is greater than the paddle's y-value center
        
        return distilled_state

    
    def play(self):
        global TRAINING
        action_a = 0
        while not self.finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.finish = True


            distilled_state = self.distille_state()


            self.state = (
                distilled_state,
                action_a
            )

            reward_a = 0

            action_a = self.paddle_a.get_action(self.state)
            self.paddle_b.simple_ai(self.ball.rect.y, SIMPLE_AI_SPEED)
    
            if action_a == 1:
                self.paddle_a.moveUp(PDL_SPEED)
            elif action_a == 2:
                self.paddle_a.moveDown(PDL_SPEED)

            self.ball.update()

            if TRAINING:
                reward_a = self.get_reward()

            if pygame.sprite.spritecollide(self.ball, [self.paddle_a], False):
                self.ball.bounce()
            if pygame.sprite.spritecollide(self.ball, [self.paddle_b], False):
                self.ball.bounce()

            if self.ball.rect.x > WIDTH:
                (self.ball.rect.x, self.ball.rect.y) = (WIDTH // 2, HEIGHT // 2)
                self.ball.velocity[0] *= -1
                self.score_a += 1
            elif self.ball.rect.x < 0:
                (self.ball.rect.x, self.ball.rect.y) = (WIDTH // 2, HEIGHT // 2)
                self.ball.velocity[0] *= -1
                self.score_b += 1


            if self.ball.rect.y > HEIGHT - 2*RADIUS:
                self.ball.velocity[1] *= -1
            if self.ball.rect.y < 0:
                self.ball.velocity[1] *= -1

            if TRAINING:
                distilled_state = self.distille_state()

                next_state = (
                    distilled_state,
                    action_a
                )
                self.paddle_a.update_q_table(self.state, action_a, reward_a, next_state)

            self.screen.fill(WHITE)
            pygame.draw.line(self.screen, COLOR, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 5)
            self.all_sprites_list.draw(self.screen)

            font = pygame.font.Font(None, 74)
            text = font.render(str(self.score_a), 1, COLOR)
            self.screen.blit(text, (WIDTH // 4, 10))
            text = font.render(str(self.score_b), 1, COLOR)
            self.screen.blit(text, (3 * WIDTH // 4, 10))

            self.all_sprites_list.update()

            pygame.display.flip()
            self.clock.tick(FPS)

            if TRAINING:
                self.reward += reward_a

            if self.score_a == MAX_SCORE or self.score_b == MAX_SCORE:
                self.finish = True
                pygame.quit()

if __name__ == "__main__":
    player_b = Paddle(COLOR, PDL_WIDTH, PDL_HEIGHT,"B")
    if TRAINING:
        player_a = Paddle(COLOR, PDL_WIDTH, PDL_HEIGHT, "A")

        for i in range(501):
            game = Game(player_a, player_b)
            game.play()
            if (i) % 10 == 0:
                player_a.save(i)
            player_a.plot_model(game.reward, i)
            print(f"game: {i} epsilon A : {player_a.epsilon} score A : {game.score_a} rewards A : {game.reward}")
    else:
        player_a = Paddle(COLOR, PDL_WIDTH, PDL_HEIGHT,"A")
        player_a.load('player_A_250_qtable.pkl')

        game = Game(player_a, player_b)
        game.play()