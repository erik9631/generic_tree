from .json_serializer import JsonSerializer
from .tree import Tree


class Serializable(JsonSerializer):
    def deserialize(self, root: Tree, path):
        pass
