from Exceptions import AnnotationException

def enforce_annotations(func):
    def wrapper(*args):
        for x in range(len(func.__annotations__)):
            if str(args).startswith("(<"):
                continue
            if not (type(args[x]) == list(func.__annotations__.values())[x]):
                raise AnnotationException(f"Expected {list(func.__annotations__.values())[x]} but got {type(args[x])} at argument {x}")
        return func(*args)
    return wrapper