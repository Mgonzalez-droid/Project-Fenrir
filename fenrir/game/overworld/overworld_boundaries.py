from fenrir.common.config import DisplaySettings


class Boundaries:
    def __init__(self, screen, hero):
        self.screen = screen

        # Current player position
        self.player_x = hero.x
        self.player_y = hero.y

        # Measurements of the player png
        self.player_width = hero.sprite.get_width()
        self.player_height = hero.sprite.get_height()

    # Checks if the player is moving outside the window
    def collision_up(self):
        if self.player_y <= 0:
            return 0
        else:
            self.player_y -= 10
            return self.player_y

    def collision_down(self):
        if self.player_y >= DisplaySettings.SCREEN_RESOLUTION.value[1] - self.player_height:
            return DisplaySettings.SCREEN_RESOLUTION.value[1] - self.player_height
        else:
            self.player_y += 10
            return self.player_y

    def collision_left(self):
        if self.player_x <= 0:
            return 0
        else:
            self.player_x -= 10
            return self.player_x

    def collision_right(self):
        if self.player_x >= DisplaySettings.SCREEN_RESOLUTION.value[0] - self.player_width:
            return DisplaySettings.SCREEN_RESOLUTION.value[0] - self.player_width
        else:
            self.player_x += 10
            return self.player_x
