import struct

# Your float or double
value = 123.456

# Pack as float
packed_value = struct.pack('>h', value)

print(packed_value)