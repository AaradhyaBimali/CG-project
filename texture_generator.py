"""
Texture Generator Module
Generates procedural planet textures using Pillow.
"""

from PIL import Image, ImageDraw
import numpy as np
import math
import os


def generate_sun_texture(size: int = 256) -> str:
    """
    Generate a glowing sun texture.
    
    Args:
        size: Texture resolution in pixels
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "sun.png")
    
    # Create image with radial gradient
    img = Image.new("RGB", (size, size), (0, 0, 0))
    pixels = img.load()
    
    center = size // 2
    max_dist = center
    
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = np.sqrt(dx*dx + dy*dy)
            
            # Radial gradient from yellow to orange to red
            intensity = max(0, 1.0 - (dist / max_dist) ** 0.8)
            r = int(255 * intensity)
            g = int(200 * intensity * 0.8)
            b = int(50 * intensity * 0.3)
            
            pixels[x, y] = (r, g, b)
    
    img.save(path)
    return path


def generate_earth_texture(size: int = 256) -> str:
    """
    Generate a simple Earth-like texture with continents.
    
    Args:
        size: Texture resolution
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "earth.png")
    
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    center = size // 2
    
    for y in range(size):
        for x in range(size):
            # Create a simple pattern based on coordinates
            noise = np.sin(x * 0.02) * np.cos(y * 0.02)
            noise += np.sin(x * 0.001) * 0.5
            
            if noise > 0.3:  # Land
                r = int(100 + 80 * (noise - 0.3))
                g = int(150 + 60 * (noise - 0.3))
                b = 50
            else:  # Ocean
                r = 20
                g = 100 + int(80 * (0.3 - noise))
                b = int(180 + 60 * (0.3 - noise))
                
            pixels[x, y] = (r, g, b)
    
    img.save(path)
    return path


def generate_mars_texture(size: int = 256) -> str:
    """
    Generate a reddish Mars-like texture.
    
    Args:
        size: Texture resolution
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "mars.png")
    
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    for y in range(size):
        for x in range(size):
            # Red/rust coloring with variation
            noise = (np.sin(x * 0.015) * np.cos(y * 0.015)) * 0.5 + 0.5
            
            r = int(180 + 50 * noise)
            g = int(100 + 30 * noise)
            b = int(60 + 20 * noise)
            
            pixels[x, y] = (r, g, b)
    
    img.save(path)
    return path


def generate_jupiter_texture(size: int = 256) -> str:
    """
    Generate a banded Jupiter-like texture.
    
    Args:
        size: Texture resolution
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "jupiter.png")
    
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    for y in range(size):
        for x in range(size):
            # Horizontal banding effect
            band_pos = (y / size) * 10
            band_intensity = abs(np.sin(band_pos * math.pi * 2)) * 0.5 + 0.5
            
            # Base colors
            noise = np.sin(x * 0.01) * 0.3 + 0.7
            
            r = int(200 * band_intensity + 100 * (1 - band_intensity))
            g = int(150 * band_intensity + 80 * (1 - band_intensity))
            b = int(80 + 40 * noise)
            
            pixels[x, y] = (r, g, b)
    
    img.save(path)
    return path


def generate_saturn_texture(size: int = 256) -> str:
    """
    Generate a pale Saturn-like texture.
    
    Args:
        size: Texture resolution
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "saturn.png")
    
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    for y in range(size):
        for x in range(size):
            # Subtle banding
            band_pos = (y / size) * 5
            band_effect = abs(np.sin(band_pos * math.pi)) * 0.2 + 0.8
            
            noise = (np.sin(x * 0.01) + np.cos(y * 0.01)) * 0.1 + 0.9
            
            r = int(220 * noise * band_effect)
            g = int(210 * noise * band_effect)
            b = int(190 * noise * band_effect)
            
            pixels[x, y] = (r, g, b)
    
    img.save(path)
    return path


def generate_mercury_texture(size: int = 256) -> str:
    """
    Generate a grey Mercury-like texture with craters.
    
    Args:
        size: Texture resolution
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "mercury.png")
    
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    for y in range(size):
        for x in range(size):
            # Grey with crater-like variations
            noise = np.sin(x * 0.02) * np.cos(y * 0.02) * 0.5 + 0.5
            noise += np.sin(x * 0.005) * 0.2
            
            grey = int(140 + 60 * noise)
            
            pixels[x, y] = (grey, grey, grey - 20)
    
    img.save(path)
    return path


def generate_venus_texture(size: int = 256) -> str:
    """
    Generate a yellowish Venus-like texture with atmospheric effects.
    
    Args:
        size: Texture resolution
        
    Returns:
        Path to generated texture
    """
    path = os.path.join("textures", "venus.png")
    
    img = Image.new("RGB", (size, size))
    pixels = img.load()
    
    for y in range(size):
        for x in range(size):
            # Yellow/orange clouds
            noise = (np.sin(x * 0.01) + np.cos(y * 0.01)) * 0.3 + 0.7
            
            r = int(230 * noise)
            g = int(200 * noise)
            b = int(100 * noise * 0.7)
            
            pixels[x, y] = (r, g, b)
    
    img.save(path)
    return path


def generate_all_textures():
    """Generate all planet textures if they don't exist."""
    # Create textures directory
    os.makedirs("textures", exist_ok=True)
    
    print("Generating planet textures...")
    
    import math  # Import math module for use in functions
    
    # Generate textures
    generate_sun_texture()
    generate_mercury_texture()
    generate_venus_texture()
    generate_earth_texture()
    generate_mars_texture()
    generate_jupiter_texture()
    generate_saturn_texture()
    
    print("✓ All textures generated successfully")
