"""
OpenGL Renderer Module
Handles OpenGL initialization, lighting, projection setup, and texture management.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os

# Explicit imports for compatibility
try:
    from OpenGL.GL import glLightModel, glLight, glMaterial
except ImportError:
    pass


class OpenGLRenderer:
    """Manages OpenGL rendering pipeline, lighting, and textures."""
    
    def __init__(self, width: int, height: int):
        """Initialize OpenGL renderer with viewport dimensions."""
        self.width = width
        self.height = height
        self.textures = {}
        self.setup_viewport()
        self.setup_projection()
        self.setup_lighting()
        
    def setup_viewport(self):
        """Configure viewport and basic OpenGL state."""
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.01, 0.01, 0.02, 1.0)  # Deep space black
        
        # Enable depth testing for proper 3D rendering
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Smooth shading for better appearance
        glShadeModel(GL_SMOOTH)
        
    def setup_projection(self):
        """Setup perspective projection matrix."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # FOV: 45°, Aspect ratio based on viewport, Near: 0.1, Far: 10000
        gluPerspective(45.0, (self.width / self.height), 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def setup_lighting(self):
        """Configure 3D lighting with sun as light source."""
        # Light positioned at sun (origin)
        light_position = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        
        # Ambient light (slight illumination everywhere)
        ambient = np.array([0.3, 0.3, 0.3, 1.0], dtype=np.float32)
        # Diffuse light (main lighting)
        diffuse = np.array([0.9, 0.9, 0.8, 1.0], dtype=np.float32)
        # Specular light (highlights)
        specular = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        
        glLight(GL_LIGHT0, GL_POSITION, light_position)
        glLight(GL_LIGHT0, GL_AMBIENT, ambient)
        glLight(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLight(GL_LIGHT0, GL_SPECULAR, specular)
        
        # Global ambient lighting
        global_ambient = np.array([0.2, 0.2, 0.25, 1.0], dtype=np.float32)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        
    def setup_material(self, shininess: float = 32.0):
        """Configure material properties for lighting response."""
        ambient = np.array([0.2, 0.2, 0.2, 1.0], dtype=np.float32)
        diffuse = np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32)
        specular = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        
        glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, shininess)
        
    def load_texture(self, texture_name: str, image_path: str) -> int:
        """
        Load a texture from file and return its OpenGL ID.
        
        Args:
            texture_name: Name to store texture under
            image_path: Path to image file
            
        Returns:
            OpenGL texture ID
        """
        if texture_name in self.textures:
            return self.textures[texture_name]
            
        try:
            # Open and convert image
            image = Image.open(image_path)
            image = image.convert("RGB")
            image_data = image.tobytes("raw", "RGB", 0, -1)
            
            # Create OpenGL texture
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Set texture parameters
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Upload texture data
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                        0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
            glGenerateMipmap(GL_TEXTURE_2D)
            
            self.textures[texture_name] = texture_id
            print(f"✓ Loaded texture: {texture_name}")
            return texture_id
            
        except Exception as e:
            print(f"✗ Error loading texture {texture_name}: {e}")
            return -1
            
    def get_texture(self, texture_name: str) -> int:
        """Get previously loaded texture ID."""
        return self.textures.get(texture_name, -1)
        
    def clear_screen(self):
        """Clear depth and color buffers."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def setup_modelview(self):
        """Prepare for model-view transformations."""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
