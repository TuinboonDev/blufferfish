def smallest_party_size():
    for total in range(1, 10000):  # Adjust the range as needed
        for glasses in range(1, total):
            no_glasses = total - glasses
            if glasses / no_glasses == 0.24:
                return total

print(smallest_party_size())