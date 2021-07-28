from fenrir.common.config import DisplaySettings


class Boundaries:
    def __init__(self, screen, hero):
        self.screen = screen


        # Current player position
        self.player_x = hero.rect.x
        self.player_y = hero.rect.y

        # Measurements of the player png
        self.player_width = hero.sprite.get_width()
        self.player_height = hero.sprite.get_height()

    # Checks if the player is moving outside the window
    def collision_up(self):
        if self.player_y <= 0:
            #return 0
            return True
        else:
            self.player_y -= 10
            #return self.player_y
            return False

    def collision_down(self):
        if self.player_y >= DisplaySettings.SCREEN_RESOLUTION.value[1] - self.player_height:
            #return DisplaySettings.SCREEN_RESOLUTION.value[1] - self.player_height
            return True
        else:
            self.player_y += 10
            #return self.player_y
            return False

    def collision_left(self):
        if self.player_x <= 0:
            #return 0
            return True
        else:
            self.player_x -= 10
            #return self.player_x
            return False

    def collision_right(self):
        if self.player_x >= DisplaySettings.SCREEN_RESOLUTION.value[0] - self.player_width:
            #return DisplaySettings.SCREEN_RESOLUTION.value[0] - self.player_width
            return True
        else:
            self.player_x += 10
            #return self.player_x
            return False
