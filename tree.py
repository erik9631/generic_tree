from typing import Optional, Callable, Generic, TypeVar

T = TypeVar("T")


class Tree(Generic[T]):
    value: Optional[T]
    is_leaf: bool = True
    _nodes: dict[str, 'Tree[T]']
    is_root: bool
    root: Optional['Tree[T]']
    parent: Optional['Tree[T]']
    key: str
    path: str

    def __init__(self, key: str, value: Optional[T] = None):
        super().__init__()
        self.value = value
        self._nodes = {}
        self.is_root = True
        self.root = self
        self.parent = None
        self.key = key
        self.path = key

    def add_node(self, node: 'Tree[T]', update=True):
        node.is_root = False
        node.parent = self
        if not self.is_root:
            node.root = self.parent.root
        else:
            node.root = self
        node.path = self.path + '.' + node.path
        self._nodes[node.key] = node
        if update:
            self._update_tree(self.root)
        self.is_leaf = False

    def remove_node(self, node: 'Tree[T]'):
        self._nodes.pop(node.key)
        if not len(self._nodes):
            self.is_leaf = True
        node.parent = None
        node.is_root = True
        node._update_tree(node)
        return node

    def create_node(self, key, value: Optional[T], update=True):
        node = Tree(key, value)
        self.add_node(node, update)
        return node

    def get_node(self, key: str):
        node = self._nodes[key]
        return node

    def get_nodes(self) -> dict[str, 'Tree[T]']:
        return self._nodes

    def _get_node_by_path(self, path: [str]):
        next_path = path.pop(0)

        if next_path != '*':
            if next_path not in self._nodes:
                return None
            node = self._nodes[next_path]
            if len(path) == 0:
                return node
            return node._get_node_by_path(path)

        for key in self._nodes:
            node = self._nodes[key]
            if len(path) == 0:
                return node
            result = node._get_node_by_path(path)
            if result is not None:
                return result
        return None

    def get_node_by_path(self, path: str):
        path = path.split('.')
        if self.key == path.pop(0) and len(path) == 0:
            return self
        return self._get_node_by_path(path)

    def _update_tree(self, root: 'Tree[T]'):
        self._update_all_roots(root)
        self._update_all_paths()

    def _update_all_paths(self):
        self.path = self.key
        if not self.is_root:
            self.path = self.parent.path + '.' + self.path

        for key in self._nodes:
            self._nodes[key]._update_all_paths()

    def _update_all_roots(self, new_root: 'Tree[T]'):
        self.root = new_root
        for key in self._nodes:
            self._nodes[key]._update_all_roots(new_root)

    def _create_nodes_from_path(self, key_list: [str], value: Optional[T], default_value: Optional[T] = None) -> 'Tree[T]':
        if len(key_list) == 0:
            self.value = value
            self._update_tree(self.root)
            return self

        next_key = key_list.pop(0)
        if self.key == next_key:
            return self._create_nodes_from_path(key_list, value)

        next_node = self._nodes.get(next_key)
        if next_node is None:
            next_node = self.create_node(next_key, default_value, False)

        return next_node._create_nodes_from_path(key_list, value)

    def create_node_from_path(self, path: str, value: Optional[T], default_value: Optional[T] = None) -> 'Tree[T]':
        paths = path.split('.')
        return self._create_nodes_from_path(paths, value, default_value)

    def bottom_up_traverse(self, callback: Callable[['Tree[T]'], 'Tree[T]' or None]):
        for key in self._nodes:
            self._nodes[key].bottom_up_traverse(callback)
        callback(self)

    def top_down_traverse(self, callback: Callable[['Tree[T]'], 'Tree[T]' or None]):
        callback(self)
        for key in self._nodes:
            self._nodes[key].top_down_traverse(callback)
