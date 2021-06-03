import arcade

class MyGameWindow(arcade.Window):
	def __ini__(self, width, height, title):
		super().__init__(width, height, title)
		self.set_location(400, 200)
		
MyGameWindow(1280, 720, "My Game window")
arcade.run()