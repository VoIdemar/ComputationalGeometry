def enum(name, **enums):
    return type(name, (), enums)