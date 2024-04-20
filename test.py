import random
import time

def check(sequence):
    num = 1
    for i in sequence:
        if i == num:
            num += 1
        else:
            return False
    return True

start = time.time()
a = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
while not check(a):
    random.shuffle(a)
print(time.time() - start)

"""
            def send_chunks():
                pr = cProfile.Profile()
                pr.enable()
    
                width = 20
                height = 20
    
                center = 0
    
                start = (width // 2, height // 2)
    
                x_coord = center - start[0]
                y_coord = center - start[1]
    
                for x in range(width + 1 if width % 2 == 0 else width):
                    for y in range(height + 1 if height % 2 == 0 else height):
                        chunk_data_update_light = ChunkDataUpdateLight(x_coord, y_coord, b'', b'')
                        clientbound.send_encrypted(chunk_data_update_light, gamestate, encryptor)
                        print("Packet")
                        y_coord += 1
                    x_coord += 1
                    y_coord = center - start[1]
                print("Sent chunks")
                pr.disable()
                s = io.StringIO()
                sortby = SortKey.TIME
                ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                ps.print_stats()
                print(s.getvalue())
    
            threading.Thread(target=send_chunks).start() #This is so slow I have to thread it
"""


"""
            def send_chunks():
                pr = cProfile.Profile()
                pr.enable()
                x, y, dx, dy = 0, 0, 0, -1

                for _ in range((2*20+1)**2):
                    if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
                        dx, dy = -dy, dx

                    chunk_data_update_light = ChunkDataUpdateLight(x, y, b'', b'')
                    clientbound.send_encrypted(chunk_data_update_light, gamestate, encryptor)

                    x, y = x + dx, y + dy
                print("Sent chunks")
                pr.disable()
                s = io.StringIO()
                sortby = SortKey.TIME
                ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                ps.print_stats()
                print(s.getvalue())

            threading.Thread(target=send_chunks).start() #This is so slow I have to thread it
"""
