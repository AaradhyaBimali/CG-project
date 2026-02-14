"""
3D Solar System Simulator
A professional Computer Graphics project using PyOpenGL, Pygame, and NumPy.

Controls:
- WASD: Rotate camera view around the scene
- Q/E: Move camera up/down
- Mouse drag: Free-look camera rotation
- Scroll/+/-: Zoom in/out
- R: Reset camera view
- P: Pause/Resume animation
- ESC: Exit application

Author: CG Project
Date: 2026
"""

import sys
import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Import project modules
from renderer import OpenGLRenderer
from camera import Camera
from planet import Planet
from texture_generator import generate_all_textures


# Constants for solar system
SUN_RADIUS = 2.0
SUN_COLOR = (1.0, 1.0, 0.3)

# Planet orbital parameters: (name, radius, distance, orbit_speed, rotation_speed)
PLANETS_DATA = [
    ("Mercury", 0.38, 8.0, 4.0, 3.0),
    ("Venus", 0.95, 12.0, 1.5, -1.0),
    ("Earth", 1.0, 16.0, 1.0, 2.0),
    ("Mars", 0.53, 21.0, 0.8, 1.9),
    ("Jupiter", 2.5, 30.0, 0.3, 2.4),
    ("Saturn", 2.0, 40.0, 0.15, 2.3),
]

# Window configuration
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS_TARGET = 60


class SolarSystemSimulator:
    """Main application class managing the solar system simulation."""
    
    def __init__(self):
        """Initialize the solar system simulator."""
        # Pygame initialization
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Solar System Simulator")
        pygame.mouse.set_visible(True)
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.show_orbits = True
        
        # OpenGL renderer
        self.renderer = OpenGLRenderer(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Camera system
        self.camera = Camera()
        
        # Generate textures
        generate_all_textures()
        
        # Initialize planets
        self.planets = self._create_planets()
        
        # Frame statistics
        self.frame_count = 0
        self.fps = 0
        self.time_elapsed = 0.0
        
        print("✓ Solar System Simulator initialized")
        print(f"✓ Window: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"✓ Planets: {len(self.planets)}")
        
    def _create_planets(self) -> list:
        """
        Create all planets with their orbital parameters and textures.
        
        Returns:
            List of Planet objects
        """
        planets = []
        texture_names = ["mercury", "venus", "earth", "mars", "jupiter", "saturn"]
        
        for i, (name, radius, distance, orbit_speed, rotation_speed) in enumerate(PLANETS_DATA):
            texture_name = texture_names[i]
            texture_path = f"textures/{texture_name}.png"
            
            # Load texture
            texture_id = self.renderer.load_texture(texture_name, texture_path)
            
            # Create planet
            planet = Planet(
                name=name,
                radius=radius,
                distance=distance,
                orbit_speed=orbit_speed,
                rotation_speed=rotation_speed,
                texture_id=texture_id
            )
            planets.append(planet)
        
        return planets
        
    def _render_sun(self):
        """Render the sun at the origin with emissive properties."""
        glPushMatrix()
        
        # Sun uses emissive material to appear bright
        emission = np.array([1.0, 1.0, 0.5, 1.0], dtype=np.float32)
        glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, emission)
        
        glColor3f(SUN_COLOR[0], SUN_COLOR[1], SUN_COLOR[2])
        
        # Create sphere for sun
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluSphere(quadric, SUN_RADIUS, 32, 32)
        
        # Reset emission
        emission_reset = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, emission_reset)
        
        glPopMatrix()
        
    def _render_starfield(self):
        """Render a background starfield."""
        glPushMatrix()
        
        glDisable(GL_LIGHTING)
        glPointSize(1.5)
        
        glColor3f(0.8, 0.8, 1.0)
        glBegin(GL_POINTS)
        
        # Create stars using deterministic random positions
        np.random.seed(42)  # Fixed seed for consistent starfield
        num_stars = 500
        star_distance = 300.0
        
        for _ in range(num_stars):
            theta = np.random.uniform(0, 2 * math.pi)
            phi = np.random.uniform(0, math.pi)
            
            x = star_distance * math.sin(phi) * math.cos(theta)
            y = star_distance * math.sin(phi) * math.sin(theta)
            z = star_distance * math.cos(phi)
            
            glVertex3f(x, y, z)
        
        glEnd()
        glPointSize(1.0)
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
        
    def _update_simulation(self):
        """Update all planetary positions and rotations."""
        if not self.paused:
            for planet in self.planets:
                planet.update(delta_time=1.0)
                
    def _render_scene(self):
        """Render the complete scene with all objects."""
        # Clear the screen and depth buffer
        self.renderer.clear_screen()
        
        # Setup camera view
        self.renderer.setup_modelview()
        self.camera.apply_view_matrix()
        
        # Render background starfield
        self._render_starfield()
        
        # Setup material for planets
        self.renderer.setup_material()
        
        # Render sun (light source)
        self._render_sun()
        
        # Render planets
        for planet in self.planets:
            planet.draw()
        
        # Optionally render orbit paths
        if self.show_orbits:
            for planet in self.planets:
                planet.draw_orbit_line()
    
    def _handle_input(self):
        """Handle keyboard and mouse input."""
        keys = pygame.key.get_pressed()
        
        # Continuous input (held keys)
        if keys[K_w]:
            self.camera.rotate_horizontal(1)
        if keys[K_s]:
            self.camera.rotate_horizontal(-1)
        if keys[K_a]:
            self.camera.rotate_vertical(1)
        if keys[K_d]:
            self.camera.rotate_vertical(-1)
        if keys[K_q]:
            self.camera.move_up()
        if keys[K_e]:
            self.camera.move_down()
        if keys[K_EQUALS] or keys[K_PLUS]:
            self.camera.zoom_in()
        if keys[K_MINUS]:
            self.camera.zoom_out()
        
        # Mouse input for free-look (right click drag)
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:  # Right mouse button
            mouse_rel = pygame.mouse.get_rel()
            self.camera.rotate_horizontal(mouse_rel[0] * 0.05)
            self.camera.rotate_vertical(-mouse_rel[1] * 0.05)
        else:
            pygame.mouse.get_rel()  # Reset relative position
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    
                elif event.key == K_r:
                    # Reset camera
                    self.camera.reset_view()
                    
                elif event.key == K_p:
                    # Toggle pause
                    self.paused = not self.paused
                    status = "PAUSED" if self.paused else "RUNNING"
                    print(f"Simulation {status}")
                    
                elif event.key == K_o:
                    # Toggle orbit visualization
                    self.show_orbits = not self.show_orbits
                    status = "ON" if self.show_orbits else "OFF"
                    print(f"Orbits: {status}")
            
            elif event.type == MOUSEBUTTONDOWN:
                # Mouse wheel zoom
                if event.button == 4:  # Scroll up
                    self.camera.zoom_in()
                elif event.button == 5:  # Scroll down
                    self.camera.zoom_out()
    
    def _display_stats(self):
        """Calculate and potentially display frame statistics."""
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            current_fps = self.clock.get_fps()
            if self.frame_count % 60 == 0:
                status = "PAUSED" if self.paused else "RUNNING"
                print(f"FPS: {current_fps:.1f} | Status: {status}")
    
    def run(self):
        """
        Main application loop.
        Coordinates update, render, and input handling.
        """
        print("\n" + "="*60)
        print("CONTROLS:")
        print("  WASD       - Rotate view")
        print("  Q/E        - Move up/down")
        print("  Mouse+RMB  - Free-look")
        print("  Scroll/+/- - Zoom")
        print("  R          - Reset camera")
        print("  P          - Pause/Resume")
        print("  O          - Toggle orbits")
        print("  ESC        - Exit")
        print("="*60 + "\n")
        
        while self.running:
            # Input handling
            self._handle_input()
            
            # Update simulation
            self._update_simulation()
            
            # Render scene
            self._render_scene()
            
            # Display frame
            pygame.display.flip()
            
            # Maintain target FPS
            self.clock.tick(FPS_TARGET)
            
            # Display statistics
            self._display_stats()
        
        self._cleanup()
        
    def _cleanup(self):
        """Clean up resources before exit."""
        pygame.quit()
        print("\n✓ Application closed")


def main():
    """Entry point for the application."""
    try:
        simulator = SolarSystemSimulator()
        simulator.run()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
