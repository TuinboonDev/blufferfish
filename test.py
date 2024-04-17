# import time
# start = time.time()
# import random
import threading

# def generate_noise(width, height, seed):
#     random.seed(seed)
#     return [[random.random() for _ in range(width)] for _ in range(height)]

# # Usage
# noise = generate_noise(1024, 1024, seed=12345)
# print(noise[10][10])
# print(time.time() - start)

import threading

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
while True:
    print(a[0]) if a else None
    a.pop(0) if a else None


"""
            packet_queue = []

            def handle_queue():
                while packet_queue:
                    clientbound.send_encrypted(packet_queue[0], gamestate, encryptor)

            def handle_y(y_coord):
                for y in range(height + 1 if height % 2 == 0 else height):
                    start_time = time.time()
                    packet_queue.append(ChunkDataUpdateLight(x_coord, y_coord, b'', b''))
                    y_coord += 1

            for x in range(width + 1 if width % 2 == 0 else width):
                threading.Thread(target=handle_y, args=(y_coord)).start()
                x_coord += 1
                y_coord = center - start[1]
"""

"""
pr = cProfile.Profile()
pr.enable()
pr.disable()
s = io.StringIO()
sortby = SortKey.TIME
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
"""