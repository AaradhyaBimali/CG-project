"""
Planet Module
Defines the Planet class with orbital mechanics and rendering.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math


class Planet:
    """Represents a celestial body with orbital and rotational dynamics."""
    
    def __init__(self, name: str, radius: float, distance: float, 
                 orbit_speed: float, rotation_speed: float, 
                 texture_id: int, color: tuple = (0.8, 0.8, 0.8)):
        """
        Initialize a planet with physical and orbital parameters.
        
        Args:
            name: Planet name for identification
            radius: Physical radius of the planet
            distance: Distance from sun (orbital radius)
            orbit_speed: Degrees per frame for orbital motion
            rotation_speed: Degrees per frame for axial rotation
            texture_id: OpenGL texture ID for this planet
            color: RGB tuple for color (0.0-1.0) if no texture
        """
        self.name = name
        self.radius = radius
        self.distance = distance
        self.orbit_speed = orbit_speed
        self.rotation_speed = rotation_speed
        self.texture_id = texture_id
        self.color = color
        
        # Orbital state
        self.orbit_angle = np.random.uniform(0, 360)  # Random start position
        
        # Rotational state
        self.rotation_angle = np.random.uniform(0, 360)
        
        # Pre-create the sphere for rendering
        self.quadric = gluNewQuadric()
        gluQuadricNormals(self.quadric, GLU_SMOOTH)
        gluQuadricTexture(self.quadric, GL_TRUE)
        
    def update(self, delta_time: float = 1.0):
        """
        Update planet orbital and rotational positions.
        
        Args:
            delta_time: Time step (frames). Default 1.0 for one frame.
        """
        # Update orbital position
        self.orbit_angle += self.orbit_speed * delta_time
        if self.orbit_angle >= 360:
            self.orbit_angle -= 360
            
        # Update rotation
        self.rotation_angle += self.rotation_speed * delta_time
        if self.rotation_angle >= 360:
            self.rotation_angle -= 360
            
    def get_position(self) -> np.ndarray:
        """
        Get current 3D position in orbit.
        
        Returns:
            3D position vector (x, y, z)
        """
        # Circular orbit in XZ plane
        angle_rad = self.orbit_angle * math.pi / 180.0
        x = self.distance * math.cos(angle_rad)
        z = self.distance * math.sin(angle_rad)
        y = 0.0
        return np.array([x, y, z], dtype=np.float32)
        
    def draw(self):
        """
        Render the planet with proper transformations and lighting.
        
        Transformation sequence:
        1. Translate to orbital position
        2. Rotate around own axis
        3. Bind texture
        4. Render sphere
        """
        # Save transformation matrix state
        glPushMatrix()
        
        # Get current orbital position
        position = self.get_position()
        
        # 1. Translate to orbital position (revolution around sun)
        glTranslatef(position[0], position[1], position[2])
        
        # 2. Rotate around planet's own axis (rotation)
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)
        
        # 3. Bind texture if available
        if self.texture_id >= 0:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(self.color[0], self.color[1], self.color[2])
            
        # 4. Render sphere
        # gluSphere(quadric, radius, slices, stacks)
        # Using 32 slices and stacks for good detail
        gluSphere(self.quadric, self.radius, 32, 32)
        
        glDisable(GL_TEXTURE_2D)
        
        # Restore transformation matrix state
        glPopMatrix()
        
    def draw_orbit_line(self):
        """
        Draw a faint line showing the planet's orbital path (optional visualization).
        """
        glPushMatrix()
        
        # Use line drawing mode
        glDisable(GL_LIGHTING)  # Disable lighting for orbit lines
        glColor4f(0.3, 0.3, 0.5, 0.3)  # Semi-transparent blue
        
        # Draw orbit circle in XZ plane
        glBegin(GL_LINE_LOOP)
        segments = 128
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = self.distance * math.cos(angle)
            z = self.distance * math.sin(angle)
            glVertex3f(x, 0.0, z)
        glEnd()
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
