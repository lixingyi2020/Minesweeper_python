import os
import sys
import time
from enum import Enum
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from mine_field import MineStatus, MineField


FIELD_WIDTH = 30
FIELD_HEIGHT = 16
MINE_COUNT = 99

MINE_SIZE = 20

SCREEN_WIDTH = FIELD_WIDTH * MINE_SIZE
SCREEN_HEIGHT = (FIELD_HEIGHT + 2) * MINE_SIZE

RED = (200, 40, 40)
WHITE = (225, 225, 225) 


class GameStatus(Enum):
    READY = 1
    STARTED = 2
    OVER = 3
    WIN = 4


class Game:
    def __init__(self, resource_folder="resources"):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")

        self.bgcolor = WHITE  # background color

        self.load_resource(resource_folder)

        self.reset_game()

    def run(self):
        """Main game loop"""
        while True:
            self.screen.fill(self.bgcolor)
            
            self.handle_events()
            self.render_minesweeper()
            self.render_game_info()
            self.update_game_status()
            self.render_face()

            pygame.display.update()

    def load_resource(self, resource_folder):
        # Add path validation
        if not os.path.isdir(resource_folder):
            raise FileNotFoundError(f"Resource folder not found: {resource_folder}")
        
        self.font = pygame.font.Font(f"{resource_folder}/a.TTF", MINE_SIZE * 2)
        self.font_width, self.font_height = self.font.size("999")        
        # load images, because the size of resource file is not the same, so it is processed uniformly
        # en: Load and scale number images (0-8)
        self.img_dict = {}
        for i in range(9):
            img = pygame.image.load(f"{resource_folder}/{i}.bmp").convert()
            self.img_dict[i] = pygame.transform.smoothscale(img, (MINE_SIZE, MINE_SIZE))

        # load other game elements
        elements = ["blank", "flag", "ask", "mine", "blood", "error"]

        for elem in elements:
            img = pygame.image.load(f"{resource_folder}/{elem}.bmp").convert()
            self.img_dict[elem] = pygame.transform.smoothscale(img, (MINE_SIZE, MINE_SIZE))

        # load face images
        self.face_size = int(MINE_SIZE * 1.5)
        self.face_pos_x = (SCREEN_WIDTH - self.face_size) // 2
        self.face_pos_y = (MINE_SIZE * 2 - self.face_size) // 2
        faces = ["face_fail", "face_normal", "face_success"]
        for face in faces:
            img = pygame.image.load(f"{resource_folder}/{face}.bmp").convert()
            self.img_dict[face] = pygame.transform.smoothscale(
                img, (self.face_size, self.face_size)
            )

    def print_text(self, x, y, text, fcolor=(255, 255, 255)):
        imgText = self.font.render(text, True, fcolor)
        self.screen.blit(imgText, (x, y))

    def render_minesweeper(self):
        """Render minesweeper game blocks"""
        self.flag_count = 0
        self.opened_count = 0

        for row in self.field.block:
            for mine in row:
                pos = (mine.x * MINE_SIZE, (mine.y + 2) * MINE_SIZE)
                if mine.status == MineStatus.OPENED:
                    self.screen.blit(self.img_dict[mine.around_mine_count], pos)
                    self.opened_count += 1
                elif mine.status == MineStatus.BOTH_BUTTON_CLICKING:
                    self.screen.blit(self.img_dict[mine.around_mine_count], pos)
                elif mine.status == MineStatus.BOOMED:
                    self.screen.blit(self.img_dict["blood"], pos)
                elif mine.status == MineStatus.FLAGGED:
                    self.screen.blit(self.img_dict["flag"], pos)
                    self.flag_count += 1
                elif mine.status == MineStatus.QUESTION_MARK:
                    self.screen.blit(self.img_dict["ask"], pos)
                elif mine.status == MineStatus.HINTING:
                    self.screen.blit(self.img_dict[0], pos)
                elif self.game_status == GameStatus.OVER and mine.value:
                    self.screen.blit(self.img_dict["mine"], pos)
                elif mine.value == 0 and mine.status == MineStatus.FLAGGED:
                    self.screen.blit(self.img_dict["error"], pos)
                elif mine.status == MineStatus.INITIAL:
                    self.screen.blit(self.img_dict["blank"], pos)

        return self.flag_count, self.opened_count

    def is_win(self):
        block_count = FIELD_WIDTH * FIELD_HEIGHT
        return (self.flag_count + self.opened_count == block_count) or \
            (block_count - self.opened_count == MINE_COUNT)

    def update_game_status(self):
        if self.game_status == GameStatus.STARTED:
            self.elapsed_time = int(time.time() - self.start_time)

        if self.is_win():
            self.game_status = GameStatus.WIN
            # en: Auto-flag all mines when won
            for row in self.field.block:
                for mine in row:
                    if mine.value:
                        mine.status = MineStatus.FLAGGED

    def render_game_info(self):
        # Render mine counter
        self.print_text(
            30,
            (MINE_SIZE * 2 - self.font_height) // 2 - 2,
            "%02d" % (MINE_COUNT - self.flag_count),
            RED,
        )

        # Render timer
        self.print_text(
            SCREEN_WIDTH - self.font_width - 30,
            (MINE_SIZE * 2 - self.font_height) // 2 - 2,
            "%03d" % self.elapsed_time,
            RED,
        )

    def render_face(self):
        # Render face according to game status
        if self.game_status == GameStatus.OVER:
            self.screen.blit(
                self.img_dict["face_fail"], (self.face_pos_x, self.face_pos_y)
            )
        elif self.game_status == GameStatus.WIN:
            self.screen.blit(
                self.img_dict["face_success"], (self.face_pos_x, self.face_pos_y)
            )
        else:
            self.screen.blit(
                self.img_dict["face_normal"], (self.face_pos_x, self.face_pos_y)
            )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)
            elif event.type == MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)

    def handle_mouse_button_down(self, event):
        self.mouse_x, self.mouse_y = event.pos
        x = self.mouse_x // MINE_SIZE
        y = self.mouse_y // MINE_SIZE - 2
        self.left_btn_pressed, _, self.right_btn_pressed = pygame.mouse.get_pressed()  # ingore middle button
        
        # when both left and right mouse buttons are pressed, if all mines are marked,
        # then open around 8 un-opened blocks, if not all mines are marked, then show the effect
        # that around blocks are pressed down
        if self.game_status == GameStatus.STARTED and self.left_btn_pressed and self.right_btn_pressed:
            mine = self.field.get_mine(x, y)
            if (
                mine.status == MineStatus.OPENED
                and not self.field.double_mouse_button_down(x, y)
            ):
                self.game_status = GameStatus.OVER

    def face_clicked(self, mouse_x, mouse_y):
        y = mouse_y // MINE_SIZE - 2
        return y < 0 and (
            self.face_pos_x <= mouse_x <= self.face_pos_x + self.face_size
            and self.face_pos_y <= mouse_y <= self.face_pos_y + self.face_size
        )

    def handle_mouse_button_up(self, event):
        x = self.mouse_x // MINE_SIZE
        y = self.mouse_y // MINE_SIZE - 2

        if self.face_clicked(self.mouse_x, self.mouse_y):
            self.reset_game()
            return

        if self.game_status == GameStatus.READY:
            self.start_game()
            
        if self.game_status == GameStatus.STARTED:
            self.handle_gameplay_actions(x, y, self.left_btn_pressed, self.right_btn_pressed)

    def reset_game(self):
        self.game_status = GameStatus.READY
        self.field = MineField(FIELD_WIDTH, FIELD_HEIGHT, MINE_COUNT)
        self.elapsed_time = 0
        self.flag_count = 0
        self.opened_count = 0

    def start_game(self):
        self.game_status = GameStatus.STARTED
        self.start_time = time.time()
        self.elapsed_time = 0

    def handle_gameplay_actions(self, x, y, left_btn_pressed, right_btn_pressed):
        mine = self.field.get_mine(x, y)
        if left_btn_pressed and not right_btn_pressed:
            if mine.status == MineStatus.INITIAL and not self.field.open_mine(x, y):
                self.game_status = GameStatus.OVER
        elif not left_btn_pressed and right_btn_pressed:
            mine.toggle_status()
        elif left_btn_pressed and right_btn_pressed and mine.status == MineStatus.BOTH_BUTTON_CLICKING:
            self.field.double_mouse_button_up(x, y)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

