# import time
# start = time.time()
# import random

# def generate_noise(width, height, seed):
#     random.seed(seed)
#     return [[random.random() for _ in range(width)] for _ in range(height)]

# # Usage
# noise = generate_noise(1024, 1024, seed=12345)
# print(noise[10][10])
# print(time.time() - start)


from Handlers.GeneralChunkHandler import *

blocks = []
for i in range(2048):
    blocks.append(Block(0))
    blocks.append(Block(1))
section = ChunkSection(blocks)
serialized = section.serialize()

b = []
for byte in serialized:
    b.append(byte)

# print(b)