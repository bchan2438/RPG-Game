"""
Platformer Game
"""
import arcade


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "RPG"
CHARACTER_SCALING = .2
TILE_SCALING = 0.05
PLAYER_MOVEMENT_SPEED = 5
class MyGame(arcade.Window):
    """
    Main application class.
    """
   


    def __init__(self):


        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        self.scene = None


        self.player_sprite = None


        self.physics_engine = None


        arcade.set_background_color(arcade.csscolor.BLACK)


               
       


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.scene = arcade.Scene()


        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash = True)
       
        image_source =  "Images/Warrior_Image.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)


        for x in range(0, 1250, 64):
            wall = arcade.Sprite("Images/Rock.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)


        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
   
    def on_draw(self):
        """Render the screen."""


        self.clear()
        # Code to draw the screen goes here
        self.scene.draw()
   
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    def on_key_release(self, key, modifiers):
       


        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """Movement and game logic"""


        # Move the player with the physics engine
        self.physics_engine.update()


   
def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()




if __name__ == "__main__":
    main()

