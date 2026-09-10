import arcade
import random

class Game(arcade.View):
	def  __init__(self):
		super().__init__()
		self.font = arcade.load_font("Renogare-Regular.otf")
		self.numbers = [1, 2, 3,
				  		4, 5, 6,
				  		7, "*", 8]
		self.cx = self.width / 2 - 3 * 50
		self.cy = self.height / 2 + 3 * 50
		self.texts = []
		self.rects = []
		self.state = 0
		self.win_text = arcade.Text(
			"Congratulations! You won", self.width / 2,
			self.height / 2, arcade.color.WHITE,
			32, font_name="Renogare", anchor_x="center"
		)
		self.restart_text = arcade.Text(
			"Restart", self.width / 2 - 80,
			self.height / 2 - 50, arcade.color.YELLOW,
			24, font_name="Renogare", anchor_x="center"
		)
		self.quit_text = arcade.Text(
			"Quit", self.width / 2 + 80,
			self.height / 2 - 50, arcade.color.WHITE,
			24, font_name="Renogare", anchor_x="center"
		)
		self.scroll = 0
		self.delay = 0
		self.start_game()

	def start_game(self):
		self.validate_game()
		self.update_game()

	def scroll_update(self):
		if not self.scroll:
			self.restart_text.color = arcade.color.YELLOW
			self.quit_text.color = arcade.color.WHITE

		else:
			self.quit_text.color = arcade.color.YELLOW
			self.restart_text.color = arcade.color.WHITE

	def validate_game(self):
		valid = 0
		while not valid:
			random.shuffle(self.numbers)
			nums = [n for n in self.numbers if n != "*"]
			count = 0
			for i in range(len(nums) - 1):
				for j in range(i, len(nums)):
					if nums[i] > nums[j]:
						count += 1
			if not count % 2:
				valid = 1

	def update_game(self):
		self.texts = []
		self.rects = []
		for i, number in enumerate(self.numbers):
			color = arcade.color.BLACK
			text = arcade.Text(
				str(number), self.cx + (i % 3) * 150, self.cy - (i // 3) * 150,
				color, 80, anchor_x="center", anchor_y="center",
				font_name="Renogare"
			)
			self.texts.append(text)
			r = arcade.rect.XYWH(self.cx + (i % 3) * 150, self.cy - (i // 3) * 150, 
						140, 140)
			self.rects.append(r)
		if self.is_solved():
			self.delay = 1
			self.state = 1
			return

	def can_move(self, block):
		idx = self.numbers.index("*")
		block_x = self.numbers.index(block) % 3
		block_y = self.numbers.index(block) // 3
		empty_x = idx % 3
		empty_y = idx // 3
		if empty_x + 1 == block_x and empty_y == block_y or \
			empty_x - 1 == block_x and empty_y == block_y or \
			empty_y + 1 == block_y and empty_x == block_x or \
			empty_y - 1 == block_y and empty_x == block_x:
				return True
		return False

	def is_solved(self):
		if all(isinstance(n, int) for n in self.numbers[:-1]) and \
			sorted(self.numbers[:-1]) == self.numbers[:-1]:
			return True
		return False

	def move(self, block):
		swp = block
		tmp = self.numbers.index("*")
		self.numbers[self.numbers.index(block)] = "*"
		self.numbers[tmp] = swp
		self.update_game()

	def on_update(self, delta_time):
		if self.delay > 0:
			self.delay = max(0, self.delay - delta_time)

	def on_mouse_press(self, x, y, button, modifiers):
		if self.delay:
			return
		for i, rec in enumerate(self.rects):
			if rec.left  <= x <= rec.right  \
				and rec.bottom <= y <= rec.top:
					if self.can_move(self.numbers[i]):
						self.move(self.numbers[i])

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.Q:
			self.window.close()
		if self.state == 1:
			if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
				self.scroll = (self.scroll + 1) % 2
				self.scroll_update()
			if symbol == arcade.key.ENTER:
				if not self.scroll:
					self.state = 0
					self.start_game()
				else:
					self.window.close()

	def on_draw(self):
		self.clear()
		if not self.state or self.delay:
			for i in range(9):
				arcade.draw_rect_filled(self.rects[i],
				arcade.color.GRAY if not isinstance(self.numbers[i], str) else \
					arcade.color.BLACK)
				self.texts[i].draw()
		else:
			self.win_text.draw()
			self.restart_text.draw()
			self.quit_text.draw()

window = arcade.Window(900, 700, "Sliding Puzzle", center_window=True)
game = Game()
window.show_view(game)
arcade.run()