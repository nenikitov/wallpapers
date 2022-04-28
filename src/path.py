from os import path

class ProjectPath(str):
    __root_folder = path.abspath(path.join(path.dirname( __file__ ), '..'))

    def __init__(self, *paths):
        self.__path = path.abspath(path.join(ProjectPath.__root_folder, *paths))


    def __add__(self, other):
        return path.join(self.__path, other)
    def __iadd__(self, other):
        self.__path = self.__add__(other)


    def __sub__(self, other):
        return self.__add__(other * '..')
    def __isub__(self, other):
        self.__path = self.__sub__(other)


    def __str__(self):
        return self.__path
