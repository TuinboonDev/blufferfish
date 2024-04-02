a = b"\xbcM\x8a\xaeL\x86H\xaa\xa3<\t\xefp'\xea\xda"

#turn the uuid bytes into a string
def uuid_to_str(uuid):
    return ''.join([hex(byte)[2:] for byte in uuid])

print(uuid_to_str(a)) #bc4d8aae4c8648aaa33c09ef7027eadb

#this code doesnt decode a 0 in the uuid bytes, so the output is incorrect
#rewrite here
def uuid_to_str(uuid):
    return ''.join([f"{byte:02x}" for byte in uuid])


print(uuid_to_str(a)) #bc4d8aae4c8648aaa33c09ef7027eadb

#write in basic for loop
def uuid_to_str(uuid):
    result = ""
    for byte in uuid:
        result += f"{byte:02x}"
    return result

#what does the f string with the {byte:02x} do?
#it takes the byte and converts it to a hex string with 2 characters
#so every byte is converted to a 2 character hex string