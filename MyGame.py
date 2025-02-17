"""
RPG Game
"""
import arcade
import random
import time


# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "RPG"
CHARACTER_SCALING = .15
TILE_SCALING = 1.4
INSIDE_WALL_SCALING = .1
PLAYER_MOVEMENT_SPEED = 4
LAYER_NAME_WALLS = "Walls_Collidable"

NUM_ENEMIES = 5
NUM_WALLS = 10

class Enemy(arcade.Sprite):
    def __init__(self, image_path, scale, health, speed, defense, damage, walls_list):
        super().__init__(image_path, scale)
        self.health = health
        self.damage = damage
        self.speed = speed
        self.defense = defense
        self.target = None
        self.last_attack_time = 0
        self.walls = walls_list

    def update(self):
        if self.target:
            self.follow_target(self.target)
        self.rebound()
        self.center_x += self.change_x
        self.center_y += self.change_y

    def follow_target(self, target):

        if self.has_clear_path(target, self.walls):
            if self.center_x < target.center_x:
                self.change_x = self.speed
            elif self.center_x > target.center_x:
                self.change_x = -self.speed

            if self.center_y < target.center_y:
                self.change_y = self.speed
            elif self.center_y > target.center_y:
                self.change_y = -self.speed
        else:
            self.change_y = 0
            self.change_x = 0
    def has_clear_path(self, target, walls):
       
            start = (self.center_x, self.center_y)
            end = (target.center_x, target.center_y)
           
            for wall in walls:
                # Get wall's bounding box as (left, right, bottom, top)
                rect = (wall.left, wall.right, wall.bottom, wall.top)
                if self.line_intersects_rect(start, end, rect):
                    return False
            return True

    def line_intersects_rect(self, p1, p2, rect):
        """
        Checks if the line segment (p1 to p2) intersects the rectangle defined by rect.
        """
        left, right, bottom, top = rect
        # Define the four edges of the rectangle
        edges = [
            ((left, bottom), (left, top)),     # left edge
            ((left, top), (right, top)),         # top edge
            ((right, top), (right, bottom)),     # right edge
            ((right, bottom), (left, bottom))    # bottom edge
        ]
        # If the line intersects any edge, return True.
        for edge in edges:
            if self.lines_intersect(p1, p2, edge[0], edge[1]):
                return True
        return False

    def lines_intersect(self, p1, p2, p3, p4):
        """
        Checks if line segments (p1, p2) and (p3, p4) intersect using the orientation method.
        """
        def orientation(a, b, c):
            # Calculate the cross product
            val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else 2  # Clockwise or Counterclockwise

        def on_segment(a, b, c):
            # Check if point b lies on segment ac.
            if min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and min(a[1], c[1]) <= b[1] <= max(a[1], c[1]):
                    return True
            return False

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        # General case: if orientations are different, the lines intersect.
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases
        if o1 == 0 and on_segment(p1, p3, p2): return True
        if o2 == 0 and on_segment(p1, p4, p2): return True
        if o3 == 0 and on_segment(p3, p1, p4): return True
        if o4 == 0 and on_segment(p3, p2, p4): return True

        return False




    def rebound(self):
        # Check for collision with the target (player)
        if arcade.check_for_collision(self, self.target):
            # Rebound the enemy from the player
            if self.center_x < self.target.center_x:
                self.center_x -= self.speed * 2
            elif self.center_x > self.target.center_x:
                self.center_x += self.speed * 2

            if self.center_y < self.target.center_y:
                self.center_y -= self.speed * 2
            elif self.center_y > self.target.center_y:
                self.center_y += self.speed * 2


class Goblin(Enemy):
    def __init__(self, walls_list):
        super().__init__("Images/Goblin.png", 0.08, health = random.randint(3,6),speed = random.uniform(0.8,1.2),defense = 0,damage = random.randint(1,2), walls_list=walls_list)
    
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

        self.enemy_physics_engines = []
        self.enemy_wall_engines = []

        self.swing_sound = arcade.load_sound("Sounds/Swing_Sword.mp3")


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
        self.scene.add_sprite_list("Stairs")
        self.scene.add_sprite_list("Walls", use_spatial_hash = True)

        self.scene.add_sprite_list("Inside Walls", use_spatial_hash= True)
       
        image_source =  "Images/Warrior_Image.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 156
        self.player_sprite.center_y = 156
        self.scene.add_sprite("Player", self.player_sprite)
        self.enemies = arcade.SpriteList()

        stairs = "Images/Staircase.png"
        self.stair_sprite = arcade.Sprite(stairs, CHARACTER_SCALING)
        self.stair_sprite.center_x = 850
        self.stair_sprite.center_y = 350
        self.scene.add_sprite("Stairs", self.stair_sprite)


        wall_list = self.scene.get_sprite_list(LAYER_NAME_WALLS)

        for _ in range(NUM_ENEMIES):
            Goblin1 = Goblin(wall_list)
            # Min 300,300. max 1100 650 
            Goblin1.center_x = random.randint(300,1100)
            Goblin1.center_y = random.randint(300,650)
            Goblin1.target = self.player_sprite
            self.enemies.append(Goblin1)
            enemy_physics_engine = arcade.PhysicsEngineSimple(
            Goblin1, self.scene.get_sprite_list(LAYER_NAME_WALLS)
            )
            self.enemy_physics_engines.append(enemy_physics_engine)
            
            
       

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)



        self.camera = arcade.Camera(self.width, self.height)

                # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_WALLS)
        )
       

        # Keep track of the score
        self.health = 50
        """Will be changed to characer.health"""
        self.walk_sound_player = None  # Keeps track of the sound player

        

        
       
        
   
    def on_draw(self):
        """Render the screen."""


        self.clear()
        # Code to draw the screen goes here

        self.camera.use()

        self.scene.draw()
        
        self.enemies.draw()

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
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            attack_range = 90  # Range of the attack

            # Check for enemies within range
            for enemy in self.enemies:
                distance = arcade.get_distance(self.player_sprite.center_x, self.player_sprite.center_y, enemy.center_x, enemy.center_y)
                if distance <= attack_range:
                    arcade.play_sound(self.swing_sound)
                    enemy.health -= 1
                

                    if enemy.health <= 0:
                        self.enemies.remove(enemy)

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

        self.enemies.update()
        for engine in self.enemy_physics_engines:
            engine.update()

        current_time = time.time()
    

        """Add update health when enemies hit once theose are implemented"""
        for enemy in self.enemies:
            if arcade.check_for_collision(self.player_sprite, enemy):
                if current_time - enemy.last_attack_time >= 2:  # 2-second cooldown
                    self.health -= enemy.damage
                    enemy.last_attack_time = current_time
            

        """add game over when health = 0"""
        


   
def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()




if __name__ == "__main__":
    main()

