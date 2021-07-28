from fenrir.game.overworld.overworld_npc import overworld_npc
from fenrir.game.overworld.Spritesheet import Spritesheet
import pygame


class overworld_hero_animated(overworld_npc):
    def __init__(self, x, y, filename, level, party, show_interaction, is_choice, dialogue):
        super().__init__(x, y, filename, level, party, show_interaction, is_choice, dialogue)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.load_frames(filename)
        self.rect = self.idle_frames_right[0].get_rect()
        self.rect.topleft = (x, y)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]
        self.sprite = self.current_image
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.LEFT_KEY = False
        self.RIGHT_KEY = False
        self.FACING_LEFT = False
         
    # can be replaced with a game object...
    def draw(self, display):
        #display.blit(self.hero.sprite, (self.hero.x, self.hero.y))
        #display.blit(self.current_image, self.rect)
        display.blit(self.current_image, (self.rect.x, self.rect.y))

    def update(self):
        self.velocity_x = 0
        self.velocity_y = 0
        if self.LEFT_KEY or self.RIGHT_KEY:
            if self.LEFT_KEY:
                self.velocity_x = -10
            elif self.RIGHT_KEY:
                self.velocity_x = 10
            self.rect.x += self.velocity_x
            self.x = self.rect.x
            
        if self.UP_KEY or self.DOWN_KEY:
            if self.UP_KEY:
                self.velocity_y = -10
            elif self.DOWN_KEY:
                self.velocity_y = 10
            self.rect.y += self.velocity_y
            self.y = self.rect.y
        
        self.set_state()
        self.animate()
        
    def set_state(self):
        self.state = 'idle'
        if self.velocity_x > 0 and self.velocity_y > 0:
            self.state = 'moving up right'
        elif self.velocity_x > 0 and self.velocity_y < 0:
            self.state = 'moving down right'
        elif self.velocity_x < 0 and self.velocity_y > 0:
            self.state = 'moving up left'
        elif self.velocity_x < 0 and self.velocity_y < 0:
            self.state = 'moving down left'
        elif self.velocity_x > 0:
            self.state = 'moving right'
        elif self.velocity_x < 0:
            self.state = 'moving left'
        elif self.velocity_y > 0:
            self.state = 'moving up'
        elif self.velocity_y < 0:
            self.state = 'moving down'
            
    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving up right':
                    self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving down right':
                    self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving up left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving down left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving up':
                    if self.FACING_LEFT:
                        self.current_image = self.walking_frames_left[self.current_frame]
                    else:
                        self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving down':
                    if self.FACING_LEFT:
                        self.current_image = self.walking_frames_left[self.current_frame]
                    else:
                        self.current_image = self.walking_frames_right[self.current_frame]
    
    
    def load_frames(self, filename):
        my_spritesheet = Spritesheet(filename)
        self.idle_frames_right_i = [
            my_spritesheet.parse_sprite('gabe_stance_0.png'),
        ]

        self.idle_frames_right = []
        for frame in self.idle_frames_right_i:
            self.idle_frames_right.append(pygame.transform.scale(frame, (75, 75)))
        
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame, True, False))
        
        self.walking_frames_right_i = [
            my_spritesheet.parse_sprite('gabe_stance_1.png'),
            my_spritesheet.parse_sprite('gabe_stance_2.png'),
            my_spritesheet.parse_sprite('gabe_stance_3.png'),
            my_spritesheet.parse_sprite('gabe_stance_4.png'),
            my_spritesheet.parse_sprite('gabe_stance_5.png'),
            my_spritesheet.parse_sprite('gabe_stance_6.png')
        ]

        self.walking_frames_right = []
        for frame in self.walking_frames_right_i:
            self.walking_frames_right.append(pygame.transform.scale(frame, (75, 75)))
        
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame, True, False))

