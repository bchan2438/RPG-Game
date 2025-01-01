"""
Platformer Game
"""
import arcade


# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "RPG"
CHARACTER_SCALING = .1
TILE_SCALING = 1.2
PLAYER_MOVEMENT_SPEED = 5
LAYER_NAME_WALLS = "Walls_Collidable"
class MyGame(arcade.Window):
    """
    Main application class.
    """
   


    def __init__(self):


        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        self.scene = None
        self.gui_camera = None


        self.player_sprite = None


        self.physics_engine = None

        self.camera = None
        self.health = 0


        arcade.set_background_color(arcade.csscolor.BLACK)


               
       


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.scene = arcade.Scene()

        map_name = "Levels/Map_Template.json"
        layer_options = {
            LAYER_NAME_WALLS: {"use_spatial_hash": True},
        }


        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        



        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash = True)
       
        image_source =  "Images/Warrior_Image.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 156
        self.player_sprite.center_y = 156
        self.scene.add_sprite("Player", self.player_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)



        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.scene.get_sprite_list(LAYER_NAME_WALLS)
        )

        self.camera = arcade.Camera(self.width, self.height)

                # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Keep track of the score
        self.health = 10 
        """Will be changed to characer.health"""

        

        
       
        
   
    def on_draw(self):
        """Render the screen."""


        self.clear()
        # Code to draw the screen goes here

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

        score_text = f"Health: {self.health}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
   
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
    def center_camera_player(self):
        # Define the zoom level (e.g., 0.7 for zoomed-in view)
        zoom_level = 0.7

        # Set the camera scale for zoom
        self.camera.scale = zoom_level

        # Calculate the viewport dimensions based on the zoom level
        viewport_width = SCREEN_WIDTH / zoom_level
        viewport_height = SCREEN_HEIGHT / zoom_level

        # Calculate the target camera position to center around the player
        target_x = self.player_sprite.center_x - (viewport_width/ 3)
        target_y = self.player_sprite.center_y - (viewport_height/3 )

        
        self.camera.move_to((target_x, target_y))

        


        


    def on_update(self, delta_time):
        """Movement and game logic"""


        # Move the player with the physics engine
        self.physics_engine.update()

        self.center_camera_player()

        """Add update health when enemies hit once theose are implemented"""

        """add game over when health = 0"""


   
def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()




if __name__ == "__main__":
    main()

