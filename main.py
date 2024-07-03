import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 4
CARD_WIDTH = 100
CARD_HEIGHT = 100
CARD_MARGIN = 10
BG_COLOR = (255, 255, 255)
CARD_COLOR = (100, 100, 100)
CARD_BACK_COLOR = (200, 200, 200)

class Card:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * (CARD_WIDTH + CARD_MARGIN) + CARD_MARGIN
        self.y = row * (CARD_HEIGHT + CARD_MARGIN) + CARD_MARGIN
        self.is_face_up = False

    def draw(self, screen):
        if self.is_face_up:
            pygame.draw.rect(screen, CARD_COLOR, (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))
        else:
            pygame.draw.rect(screen, CARD_BACK_COLOR, (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))

    def flip(self):
        self.is_face_up = not self.is_face_up

def create_grid(grid_size):
    cards = []
    for row in range(grid_size):
        for col in range(grid_size):
            card = Card(row, col)
            cards.append(card)
    return cards

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Memory Game')

    clock = pygame.time.Clock()

    cards = create_grid(GRID_SIZE)

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

        for card in cards:
            card.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()