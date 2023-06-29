import json
from typing import Callable, List

from .tree import Tree


class JsonSerializer:
    _loaded_json: dict

    def __init__(self):
        self._loaded_json = {}

    def read(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _tree_from_json(self, root: Tree, json_root: dict):
        new_json_root = {}
        for key in json_root:
            if type(json_root[key]) is dict:
                new_json_root = json_root[key]
                new_node: Tree = root.create_node(key, "")
                self._tree_from_json(new_node, new_json_root)
            else:
                root.create_node(key, json_root[key])

    def deserialize(self, path: str):
        self._loaded_json = self.read(path)
        root = Tree('root', "")
        if type(self._loaded_json) is list:
            for index in range(0, len(self._loaded_json)):
                item = self._loaded_json[index]
                current_root = Tree(str(index), "")
                self._tree_from_json(current_root, item)
                root.add_node(current_root)
            return root
        self._tree_from_json(root, self._loaded_json)
        return root
