class AnnotationException(Exception):
    __module__ = Exception.__module__

def enfore_annotations(func):
    def wrapper(*args):
        print(len(func.__annotations__))
        for x in range(len(func.__annotations__)):
            if not (type(args[x]) == list(func.__annotations__.values())[x]):
                raise AnnotationException(f"Expected {list(func.__annotations__.values())[x]} but got {type(args[x])} at argument {x}")
        return func(*args)
    return wrapper

@enfore_annotations
def test(a, b):
    return a

a = "0000000000000000000000100000000000000000000000001011000100111111"

def bits_to_number(bits):
    return int(bits, 2)

print(a[0:26])
print(a[26:52])
print(a[52:])

print(bits_to_number(a[0:26]))
print(bits_to_number(a[26:52]))
print(bits_to_number(a[52:]))