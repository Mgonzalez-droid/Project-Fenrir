
class Scene:

    def __init__(self):
        self.next = self

    def handle_event(self, event):
        """This is an abstract method that will handle all events in the queue. This will be
        your key binding and mouse pointers. This will change for each scene(menu, combat and
        overworld) therefore we need to implement them separately in our scene classes.

        ***Abstract method must implement or will raise exception***
        """

        raise NotImplementedError

    def update(self):
        """This is an abstract method that must be implemented and will be where game
        logic is handled. This will update each time in the game loop. For example in
        here you will update the player or players positions on the map here which will
        be an attribute of your scene class. Then the render function will update that
        location to the screen this separates the logic from the rendering. Complex logic
        can be abstracted out in other classes when needed like in combat.

        ***Abstract method must implement or will raise exception***
        """

        raise NotImplementedError

    def render(self, screen):
        """This is an abstract method that must be overwritten your class. This should
        contain your rendering code to paint objects on to the scene.

        ***Abstract method must implement or will raise exception***
        """

        raise NotImplementedError

    def switch_to_scene(self, next_scene):
        """This is the main driver behind the switching scenes. When called it will set
        itself to the next scene and the game loop will render that scene. This can be
        called using self.switch_to_scene(CombatScene()) ... this will switch to combat scene
        """

        self.next = next_scene

    def terminate(self):
        """Will cause the main game loop to exit and close the game. This should not be
           called from your scene unless there is a close game option like in main menu
        """

        self.switch_to_scene(None)