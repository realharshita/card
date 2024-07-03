import pygame
import random
import json
import os

# Constants
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
LEADERBOARD_FILE = 'leaderboard.json'

# Card class
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

# Game functions
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
    time_penalty = elapsed_time  # 1 second = 1 point penalty
    move_penalty = moves * 10    # Each move costs 10 points
    score = max(base_score - time_penalty - move_penalty, 0)
    return score

def draw_text(screen, text, x, y, color=FONT_COLOR, size=FONT_SIZE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r') as file:
        return json.load(file)

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file)

def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({'name': name, 'score': score})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    save_leaderboard(leaderboard)

def draw_leaderboard(screen):
    leaderboard = load_leaderboard()
    screen.fill(BG_COLOR)
    draw_text(screen, "Leaderboard", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6, size=48)
    for i, entry in enumerate(leaderboard):
        draw_text(screen, f"{i + 1}. {entry['name']} - {entry['score']}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 30, size=30)
    draw_text(screen, "Press any key to return to the menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, size=24)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

def get_player_name(screen):
    name = ""
    input_active = True
    while input_active:
        screen.fill(BG_COLOR)
        draw_text(screen, "Enter your name:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, size=48)
        draw_text(screen, name, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, size=36)
        draw_text(screen, "Press Enter to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, size=24)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

    return name

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
        draw_text(screen, "5. Leaderboard", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, size=30)
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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    return

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
                    elif event.key == pygame.K_5:
                        draw_leaderboard(screen)
    
    grid_size = select_difficulty()
    player_name = get_player_name(screen)

    cards = create_grid(grid_size)
    random.shuffle(cards)
    flipped_cards = []
    matched_pairs = []

    moves = 0
    game_over = False
    start_time = pygame.time.get_ticks()

    reset_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 50)

    reset_message = ""

    def reset_game():
        nonlocal moves, game_over, start_time, cards, flipped_cards, matched_pairs, reset_message
        random.shuffle(cards)
        for card in cards:
            card.is_face_up = False
            card.is_matched = False
        moves = 0
        game_over = False
        start_time = pygame.time.get_ticks()
        flipped_cards = []
        matched_pairs = []
        reset_message = "Game reset!"

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if reset_button.collidepoint(pos):
                    reset_game()
                else:
                    if not game_over:
                        for card in cards:
                            if card.is_face_up or card.is_matched:
                                continue
                            if card.x < pos[0] < card.x + CARD_WIDTH and card.y < pos[1] < card.y + CARD_HEIGHT:
                                card.flip()
                                flipped_cards.append(card)
                                if len(flipped_cards) == 2:
                                    moves += 1
                                    if flipped_cards[0].is_same(flipped_cards[1]):
                                        flipped_cards[0].is_matched = True
                                        flipped_cards[1].is_matched = True
                                        matched_pairs.extend(flipped_cards)
                                    else:
                                        pygame.time.wait(1000)
                                        flipped_cards[0].flip()
                                        flipped_cards[1].flip()
                                    flipped_cards = []
                                break

        for card in cards:
            card.draw(screen)

        if check_game_over(cards) and not game_over:
            game_over = True
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            final_score = calculate_score(moves, elapsed_time)
            draw_text(screen, f"Game Over! Final Score: {final_score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, size=48)
            update_leaderboard(player_name, final_score)
            draw_text(screen, "Score saved! Check the leaderboard.", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

        pygame.draw.rect(screen, (0, 0, 255), reset_button)
        draw_text(screen, "Reset", reset_button.centerx, reset_button.centery)

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        draw_text(screen, f"Moves: {moves}", 100, SCREEN_HEIGHT - 50, size=30)
        draw_text(screen, f"Time: {elapsed_time} s", 300, SCREEN_HEIGHT - 50, size=30)
        draw_text(screen, reset_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, size=24)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
