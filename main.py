import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 100
CARD_MARGIN = 10
BG_COLOR = (255, 255, 255)
CARD_COLOR = (100, 100, 100)
CARD_BACK_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 36

class Card:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * (CARD_WIDTH + CARD_MARGIN) + CARD_MARGIN
        self.y = row * (CARD_HEIGHT + CARD_MARGIN) + CARD_MARGIN
        self.is_face_up = False
        self.is_matched = False

    def draw(self, screen):
        if self.is_face_up:
            pygame.draw.rect(screen, CARD_COLOR, (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))
        else:
            pygame.draw.rect(screen, CARD_BACK_COLOR, (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))

    def flip(self):
        self.is_face_up = not self.is_face_up

    def is_same(self, other):
        return self.row == other.row and self.col == other.col

def create_grid(grid_size):
    cards = []
    for row in range(grid_size):
        for col in range(grid_size):
            card = Card(row, col)
            cards.append(card)
    return cards

def check_game_over(cards):
    for card in cards:
        if not card.is_matched:
            return False
    return True

def calculate_score(moves, elapsed_time):
    base_score = 10000
    time_penalty = elapsed_time  
    move_penalty = moves * 10   
    score = max(base_score - time_penalty - move_penalty, 0)
    return score

def draw_text(screen, text, x, y, color=FONT_COLOR, size=FONT_SIZE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Memory Game')

    clock = pygame.time.Clock()
    
    def draw_menu():
        screen.fill(BG_COLOR)
        draw_text(screen, "Memory Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, size=48)
        draw_text(screen, "Select Difficulty", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, size=36)
        draw_text(screen, "1. Easy (4x4)", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, size=30)
        draw_text(screen, "2. Medium (6x6)", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, size=30)
        draw_text(screen, "3. Hard (8x8)", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, size=30)
        draw_text(screen, "4. Instructions", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, size=30)
        pygame.display.flip()
    
    def draw_instructions():
        screen.fill(BG_COLOR)
        draw_text(screen, "Instructions", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, size=48)
        instructions = [
            "1. Select a difficulty level to start the game.",
            "2. Click on a card to flip it over.",
            "3. Match pairs of cards to remove them from the board.",
            "4. The game ends when all pairs are matched.",
            "5. Your score is based on moves and time taken."
        ]
        for i, line in enumerate(instructions):
            draw_text(screen, line, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 30, size=24)
        draw_text(screen, "Press any key to return to the menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, size=24)
        pygame.display.flip()
    
    def select_difficulty():
        while True:
            draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 4  # Easy: 4x4 grid
                    elif event.key == pygame.K_2:
                        return 6  # Medium: 6x6 grid
                    elif event.key == pygame.K_3:
                        return 8  # Hard: 8x8 grid
                    elif event.key == pygame.K_4:
                        draw_instructions()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                if event.type == pygame.KEYDOWN:
                                    break
                            else:
                                continue
                            break
    
    grid_size = select_difficulty()

    cards = create_grid(grid_size)
    random.shuffle(cards)
    flipped_cards = []
    matched_pairs = []

    moves = 0
    game_over = False
    start_time = pygame.time.get_ticks()

    reset_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50)

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                if reset_button.collidepoint(pos):
                    random.shuffle(cards)
                    for card in cards:
                        card.is_face_up = False
                        card.is_matched = False
                    moves = 0
                    game_over = False
                    start_time = pygame.time.get_ticks()
                else:
                    for card in cards:
                        if card.is_face_up or card.is_matched:
                            continue
                        if card.x < pos[0] < card.x + CARD_WIDTH and card.y < pos[1] < card.y + CARD_HEIGHT:
                            card.flip()
                            flipped_cards.append(card)
                            if len(flipped_cards) == 2:
                                moves += 1
                                if flipped_cards[0].is_same(flipped_cards[1]):
                                    matched_pairs.extend(flipped_cards)
                                flipped_cards = []

        for card in cards:
            if not card.is_matched:
                card.draw(screen)

        if check_game_over(cards):
            game_over = True
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            final_score = calculate_score(moves, elapsed_time)
            draw_text(screen, f"Game Over! Moves: {moves}, Time: {elapsed_time} seconds", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, f"Final Score: {final_score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        
        draw_text(screen, f"Moves: {moves}", 100, 50)
        if not game_over:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            draw_text(screen, f"Time: {elapsed_time} seconds", SCREEN_WIDTH - 100, 50)

        pygame.draw.rect(screen, (0, 255, 0), reset_button)
        draw_text(screen, "Reset", reset_button.centerx, reset_button.centery)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
