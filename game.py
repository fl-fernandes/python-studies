import pygame
import random

class Cell:
	def __init__(self, size: int, pos: pygame.Vector2, is_bomb: bool):
		self.__border_width = 1
		rect_size = size - self.__border_width
		self.__size = size 
		self.__rect = pygame.Rect(pos.x, pos.y, rect_size, rect_size)
		self.__fill_color = '#d1cfcf' # light grey
		self.__border_color = '#6b6b6b' # dark grey
		self.__is_bomb = is_bomb
		self.__is_revealed = False
		self.__number_of_adjacent_bombs = 0
		self.__played_explosion_sound = False
		self.__explosion_sound = pygame.mixer.Sound('assets/audios/bit-explosion.wav')

	@property
	def is_bomb(self) -> bool:
		return self.__is_bomb
	
	@property
	def is_revealed(self) -> bool:
		return self.__is_revealed
	
	@property
	def number_of_adjacent_bombs(self) -> int:
		return self.__number_of_adjacent_bombs
	
	@number_of_adjacent_bombs.setter
	def number_of_adjacent_bombs(self, amount: int):
		self.__number_of_adjacent_bombs = amount

	def __str__(self) -> str:
		return f'Cell(size={self.__size},pos=[x:{self.__rect.left}, y:{self.__rect.top}], is_bomb={self.is_bomb}, adj={self.number_of_adjacent_bombs})'

	def __repr__(self) -> str:
		return self.__str__()

	def __draw_rect(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.__fill_color, self.__rect)

	def __draw_border(self, surface: pygame.Surface):
		x, y = self.__rect.left, self.__rect.top
		rect_width, rect_height = self.__rect.width, self.__rect.height
		border_cords = ((x, y), (x+rect_width, y), (x+rect_width, y+rect_height), (x, y+rect_height))
		pygame.draw.lines(surface, self.__border_color, True, border_cords, self.__border_width)

	def __draw_number_of_adjacents(self, surface: pygame.Surface):
		if not self.is_revealed or self.number_of_adjacent_bombs == 0:
			return

		font = pygame.font.Font(size=int(self.__size // 2))
		text = font.render(str(self.number_of_adjacent_bombs), True, 'blue')
		text_rect = text.get_rect()
		text_rect.center = (self.__rect.left + self.__size // 2), (self.__rect.top + self.__size // 2)
		surface.blit(text, text_rect)

	def __draw_bomb(self, surface: pygame.Surface):
		if not self.is_revealed or not self.is_bomb:
			return
		
		self.__play_explosion_sound()
		bomb_image = pygame.image.load('assets/images/bomb.png').convert_alpha()
		bomb_surface = pygame.transform.scale(bomb_image, (self.__size // 2, self.__size // 2))
		bomb_rect = bomb_surface.get_rect()
		bomb_rect.center = (self.__rect.left + self.__size // 2), (self.__rect.top + self.__size // 2)
		surface.blit(bomb_surface, bomb_rect)

	def __play_explosion_sound(self):
		if not self.__played_explosion_sound:
			self.__explosion_sound.play()
			self.__played_explosion_sound = True

	def render(self, surface: pygame.Surface):
		self.__draw_rect(surface)
		self.__draw_border(surface)
		self.__draw_number_of_adjacents(surface)
		self.__draw_bomb(surface)

	def reveal(self):
		if self.__is_revealed:
			return
		
		self.__is_revealed = True
		if not self.is_bomb:
			self.__fill_color = '#808080' # darker grey
		else:
			self.__fill_color = '#fa6161' # light red

	def collidepoint(self, pos: tuple[int, int]) -> bool:
		return self.__rect.collidepoint(pos[0], pos[1])

class Game:
	def __init__(self):
		self.window_size = 800
		self.running = True
		self.theme_music = pygame.mixer.Sound('assets/audios/theme-music.mp3')
		self.theme_music.set_volume(.2)
		self.theme_music.play(-1)
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.clock = pygame.time.Clock()
		self.number_of_bombs = 25
		self.number_of_cells_per_row_col = 10
		self.bomb_coords = self.__generate_bomb_coords()
		self.cells = self.__generate_cell_grid()
		self.__set_number_of_adjacent_bombs()
		self.game_over = False

		pygame.display.set_caption('Mineweeper')

	def __generate_bomb_coords(self) -> list[tuple[int, int]]:
		bomb_coords: list[tuple[int, int]] = []
		max_col = self.number_of_cells_per_row_col - 1

		for i in range(0, self.number_of_bombs):
			bomb_coords.append((random.randint(0, max_col), random.randint(0, max_col)))	
		
		return bomb_coords 
	
	def __is_bomb(self, cell_coords: tuple[int, int]) -> bool:
		return cell_coords in self.bomb_coords
	
	def __calculate_adjacent_bombs(self, cell_pos: tuple[int, int]) -> int:
		number_of_adjacent_bombs = 0
		row, col = cell_pos[0], cell_pos[1]
		adjacent_cells_coords: dict[Cell, tuple[int, int]] = [
			(row+1, col), # bottom
			(row-1, col), # top
			(row, col+1), # right
			(row, col-1), # left
			(row+1, col+1), # bottom-right diag
			(row+1, col-1), # bottom-left diag
			(row-1, col+1), # top-right diag
			(row-1, col-1), # top-left diag
		]
		
		for r, c in adjacent_cells_coords:
			if (
				(r >= 0 and r < self.number_of_cells_per_row_col) and
				(c >= 0 and c < self.number_of_cells_per_row_col)
			):
				cell = self.cells[r][c]
				number_of_adjacent_bombs += 1 if cell.is_bomb else 0

		return number_of_adjacent_bombs

	def __set_number_of_adjacent_bombs(self):
		for row in range(0, len(self.cells)):
			for col in range(0, len(self.cells[row])):
				cell = self.cells[row][col]
				if not cell.is_bomb:
					cell.number_of_adjacent_bombs = self.__calculate_adjacent_bombs((row, col))

	def __generate_cell_grid(self) -> list[list[Cell]]:
		grid: list[list[Cell]] = []
		cell_size = self.window_size / self.number_of_cells_per_row_col
		for row in range(0, self.number_of_cells_per_row_col): # row
			column: list[Cell] = []
			for col in range(0, self.number_of_cells_per_row_col): # col
				cell_pos = pygame.Vector2(row * cell_size, col * cell_size)
				column.append(Cell(cell_size, cell_pos, self.__is_bomb((row, col))))
			grid.append(column)
		return grid
	
	def __render_cell_grid(self):
		for row in self.cells:
			for cell in row:
				cell.render(self.screen)

	def __index_not_out_of_range(self, row: int, col: int) -> bool:
		return (
			(row >= 0 and row < self.number_of_cells_per_row_col) and
			(col >= 0 and col < self.number_of_cells_per_row_col)
		)

	def __reveal_non_bomb_cell(self, cell_coords: tuple[int, int]):
		row, col = cell_coords
		adjacent_cell_coords = [
			(row+1, col), # bottom
			(row-1, col), # top
			(row, col+1), # right
			(row, col-1), # left
		]
		if self.__index_not_out_of_range(row, col):
			cell = self.cells[row][col]
			if not cell.is_bomb:
				cell.reveal()
				if cell.number_of_adjacent_bombs == 0:
					for adjacent_cell_coord in adjacent_cell_coords:
						r, c = adjacent_cell_coord
						if self.__index_not_out_of_range(r, c) and not self.cells[r][c].is_revealed:
							self.__reveal_non_bomb_cell((r, c))
						else:
							pass

	def __review_all_bombs(self):
		for row in self.cells:
			for cell in row:
				if cell.is_bomb:
					cell.reveal()

	def __reveal_cells(self, initial_coords: tuple[int, int]):
		row, col = initial_coords
		cell = self.cells[row][col]
		if cell.is_bomb:
			cell.reveal()
			self.__review_all_bombs()
			self.game_over = True
			return
		self.__reveal_non_bomb_cell(initial_coords)

	def __on_grid_click(self, mouse_click_pos: tuple[int, int]):
		for row in range(0, len(self.cells)):
			for col in range(0, len(self.cells[row])):
				if self.cells[row][col].collidepoint(mouse_click_pos):
					self.__reveal_cells((row, col))

	def __handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
				mouse_click_pos = pygame.mouse.get_pos()
				self.__on_grid_click(mouse_click_pos)

	def __render_game_over(self):
		if self.game_over:
			font = pygame.font.Font(size=100)
			game_over_text = font.render('Game Over!', True, 'red')
			text_rect = game_over_text.get_rect()
			text_rect.center = self.window_size // 2, self.window_size // 2
			self.screen.blit(game_over_text, text_rect)
			self.cells = self.__generate_cell_grid()

	def run(self):
		while self.running:
			self.__handle_event()

			# fill the screen with a color to wipe away anything from last frame
			self.screen.fill("green")
			self.__render_cell_grid()
			#self.__render_game_over()
			# flip() the display to put your work on screen
			pygame.display.flip()

			# limits FPS to 60
			# dt is delta time in seconds since last frame, used for framerate-
			# independent physics.
			self.clock.tick(60)

pygame.init()
game = Game()
game.run()
pygame.quit()