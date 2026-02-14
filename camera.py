"""
Camera Module
Handles camera positioning, movement, and view matrix calculations.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt
import math


class Camera:
    """Manages 3D camera positioning and movement in the scene."""
    
    def __init__(self):
        """Initialize camera with default position and orientation."""
        # Camera position in world space
        self.position = np.array([30.0, 20.0, 30.0], dtype=np.float32)
        
        # Target point the camera looks toward
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # Up vector for camera orientation
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Camera movement speed
        self.move_speed = 0.5
        self.rotation_speed = 2.0
        self.zoom_speed = 1.0
        
        # Spherical coordinates for orbiting around target
        self.distance = np.linalg.norm(self.position - self.target)
        self.theta = math.atan2(self.position[0], self.position[2]) * 180 / math.pi
        self.phi = math.asin(self.position[1] / self.distance) * 180 / math.pi
        
    def apply_view_matrix(self):
        """Apply camera view transformation using gluLookAt."""
        gluLookAt(
            self.position[0], self.position[1], self.position[2],  # Camera position
            self.target[0], self.target[1], self.target[2],        # Look-at point
            self.up[0], self.up[1], self.up[2]                     # Up vector
        )
        
    def rotate_horizontal(self, delta: float):
        """
        Rotate camera horizontally around target (yaw).
        
        Args:
            delta: Rotation angle in degrees
        """
        self.theta += delta * self.rotation_speed
        self._update_position_from_spherical()
        
    def rotate_vertical(self, delta: float):
        """
        Rotate camera vertically around target (pitch).
        
        Args:
            delta: Rotation angle in degrees
        """
        # Clamp vertical rotation to avoid flipping
        new_phi = self.phi + delta * self.rotation_speed
        if -89.0 < new_phi < 89.0:
            self.phi = new_phi
        self._update_position_from_spherical()
        
    def move_forward(self):
        """Move camera forward along its viewing direction."""
        direction = self.target - self.position
        direction = direction / np.linalg.norm(direction)
        self.position += direction * self.move_speed
        self.target += direction * self.move_speed
        
    def move_backward(self):
        """Move camera backward along its viewing direction."""
        direction = self.target - self.position
        direction = direction / np.linalg.norm(direction)
        self.position -= direction * self.move_speed
        self.target -= direction * self.move_speed
        
    def move_left(self):
        """Move camera left (perpendicular to viewing direction)."""
        direction = self.target - self.position
        right = np.cross(direction, self.up)
        right = right / np.linalg.norm(right)
        self.position -= right * self.move_speed
        self.target -= right * self.move_speed
        
    def move_right(self):
        """Move camera right (perpendicular to viewing direction)."""
        direction = self.target - self.position
        right = np.cross(direction, self.up)
        right = right / np.linalg.norm(right)
        self.position += right * self.move_speed
        self.target += right * self.move_speed
        
    def move_up(self):
        """Move camera upward in world space."""
        self.position += self.up * self.move_speed
        self.target += self.up * self.move_speed
        
    def move_down(self):
        """Move camera downward in world space."""
        self.position -= self.up * self.move_speed
        self.target -= self.up * self.move_speed
        
    def zoom_in(self):
        """Zoom in by moving closer to target."""
        self.distance -= self.zoom_speed
        if self.distance < 10.0:  # Clamp minimum distance
            self.distance = 10.0
        self._update_position_from_spherical()
        
    def zoom_out(self):
        """Zoom out by moving farther from target."""
        self.distance += self.zoom_speed
        if self.distance > 500.0:  # Clamp maximum distance
            self.distance = 500.0
        self._update_position_from_spherical()
        
    def reset_view(self):
        """Reset camera to initial viewing position."""
        self.position = np.array([30.0, 20.0, 30.0], dtype=np.float32)
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self._recalculate_spherical()
        
    def _update_position_from_spherical(self):
        """Update camera position based on spherical coordinates."""
        theta_rad = self.theta * math.pi / 180.0
        phi_rad = self.phi * math.pi / 180.0
        
        x = self.distance * math.cos(phi_rad) * math.sin(theta_rad)
        y = self.distance * math.sin(phi_rad)
        z = self.distance * math.cos(phi_rad) * math.cos(theta_rad)
        
        self.position = self.target + np.array([x, y, z], dtype=np.float32)
        
    def _recalculate_spherical(self):
        """Recalculate spherical coordinates from current position."""
        diff = self.position - self.target
        self.distance = np.linalg.norm(diff)
        self.theta = math.atan2(diff[0], diff[2]) * 180 / math.pi
        self.phi = math.asin(diff[1] / self.distance) * 180 / math.pi
