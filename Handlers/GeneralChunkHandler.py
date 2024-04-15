"""
Make an api to abstract away chunk logic. This includes:
creating a classes for chunks, chunk sections, and perhaps an enum for blocks (although not necessary)
making methods for serializing them (you'll have to read into the relevant wiki page, be sure to ask questions)
(optional) adding convenience methods for setting and getting blocks (will be useful for when you'll be implementing player block interactions)
Sample perlin noise at all (x, z) positions. Remember that at integer coordinates the noise value is always the same. You'll have to transform block coordinates somehow.
Fill with blocks to noise height
Adjust noise until looks good
"""

class Chunk