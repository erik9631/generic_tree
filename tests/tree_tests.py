from typing import List
from tree import Tree


def test_tree_hierarchy():
    tree = Tree('root', 'root')
    child1 = tree.create_node('child1', 'child1')
    child2 = tree.create_node('child2', 'child2')
    assert len(tree._nodes) == 2
    assert tree.value == 'root'
    assert tree.path == 'root'
    assert tree.get_node("child1").value == 'child1'
    assert tree.get_node("child2").value == 'child2'
    assert tree.get_node("child1").path == 'root.child1'
    assert tree.get_node("child2").path == 'root.child2'
    assert tree.is_root is True
    assert child1.is_root is False
    assert child2.is_root is False

    child1_1 = child1.create_node('child1.1', 'child1.1')
    child1_2 = child1.create_node('child1.2', 'child1.2')
    assert len(child1._nodes) == 2
    assert child1.value == 'child1'
    assert child1.get_node("child1.1").value == 'child1.1'
    assert child1.get_node("child1.2").value == 'child1.2'
    assert child1.get_node("child1.1").path == 'root.child1.child1.1'
    assert child1.get_node("child1.2").path == 'root.child1.child1.2'
    assert tree.is_root is True
    assert child1_1.is_root is False
    assert child1_2.is_root is False

    child2_1 = child2.create_node('child2.1', 'child2.1')
    assert len(child2._nodes) == 1
    assert child2.value == 'child2'
    assert child2.get_node("child2.1").value == 'child2.1'
    assert child2.get_node("child2.1").path == 'root.child2.child2.1'
    assert tree.is_root is True
    assert child2_1.is_root is False


def test_tree_hierarchy_removal():
    tree = Tree('root', 'root')
    child1 = tree.create_node('child1', 'child1')
    child2 = tree.create_node('child2', 'child2')
    child1_1 = child1.create_node('child1.1', 'child1.1')
    child1_1_1 = child1_1.create_node('child1.1.1', 'child1.1.1')
    child1_1_2 = child1_1.create_node('child1.1.2', 'child1.1.2')

    assert len(tree._nodes) == 2

    root_node = tree.remove_node(child1)
    assert root_node == child1
    assert len(root_node._nodes) == 1
    assert root_node.is_root is True
    assert root_node.get_node('child1.1') == child1_1
    assert root_node.get_node('child1.1').get_node('child1.1.1').value == 'child1.1.1'
    assert root_node.get_node('child1.1').get_node('child1.1.2').value == 'child1.1.2'
    assert root_node.get_node('child1.1').get_node('child1.1.1').path == 'child1.child1.1.child1.1.1'
    assert root_node.get_node('child1.1').get_node('child1.1.1').is_root is False
    assert root_node.get_node('child1.1').get_node('child1.1.2').is_root is False


tree_snapshot: List[Tree] = []
index = 0


def traverse(node: Tree):
    global index
    assert node.value == tree_snapshot[index].value
    assert node.is_root == tree_snapshot[index].is_root
    assert node.parent is tree_snapshot[index].parent
    assert node.path is tree_snapshot[index].path
    if node.parent is not None:
        assert node.parent.value == tree_snapshot[index].parent.value
        assert node.parent.is_root == tree_snapshot[index].parent.is_root
        assert node.parent.path == tree_snapshot[index].parent.path
    assert node.root is tree_snapshot[index].root
    index += 1


def test_tree_traversal():
    tree = Tree('root', 'root')
    child1 = tree.create_node('child1', 'child1')
    child2 = tree.create_node('child2', 'child2')
    child1_1 = child1.create_node('child1.1', 'child1.1')
    child1_1_1 = child1_1.create_node('child1.1.1', 'child1.1.1')
    child1_1_2 = child1_1.create_node('child1.1.2', 'child1.1.2')
    child_1_1_3 = child1_1.create_node('child1.1.3', 'child1.1.3')
    child_2_1 = child2.create_node('child2.1', 'child2.1')
    child_2_2 = child2.create_node('child2.2', 'child2.2')
    child_2_3 = child2.create_node('child2.3', 'child2.3')

    tree_snapshot.append(tree)
    tree_snapshot.append(child1)
    tree_snapshot.append(child1_1)
    tree_snapshot.append(child1_1_1)
    tree_snapshot.append(child1_1_2)
    tree_snapshot.append(child_1_1_3)
    tree_snapshot.append(child2)
    tree_snapshot.append(child_2_1)
    tree_snapshot.append(child_2_2)
    tree_snapshot.append(child_2_3)

    tree.top_down_traverse(traverse)


def test_tree_path_find():
    tree = Tree('root', 'root')
    child1 = tree.create_node('child1', 'child1')
    child2 = tree.create_node('child2', 'child2')
    child1_1 = child1.create_node('child1_1', 'child1_1')
    child1_1_1 = child1_1.create_node('child1_1_1', 'child1_1_1')
    child1_1_2 = child1_1.create_node('child1_1_2', 'child1_1_2')
    child_1_1_3 = child1_1.create_node('child1_1_3', 'child1_1_3')
    child_2_1 = child2.create_node('child2_1', 'child2_1')
    child_2_2 = child2.create_node('child2_2', 'child2_2')
    child_2_3 = child2.create_node('child2_3', 'child2_3')

    assert tree.get_node_by_path('*.child1').value == 'child1'
    assert tree.get_node_by_path('*.child2').value == 'child2'
    assert tree.get_node_by_path('*.*.child1_1').value == 'child1_1'
    assert tree.get_node_by_path('*.*.*.child1_1_1').value == 'child1_1_1'
    assert tree.get_node_by_path('root.child1.child1_1.child1_1_2').value == "child1_1_2"


def test_tree_add_by_path_by_root():
    tree = Tree('root', 'root')
    leaf = tree.create_node_from_path('root.child1.child1_1.child1_1_1', 'child1_1_1')
    assert leaf.value == 'child1_1_1'
    assert leaf.path == 'root.child1.child1_1.child1_1_1'
    assert leaf.parent.value is None
    assert leaf.parent.path == 'root.child1.child1_1'
    assert leaf.parent.parent.value is None
    assert leaf.parent.parent.path == 'root.child1'
    assert leaf.parent.parent.parent.value == 'root'
    assert leaf.parent.parent.parent.path == 'root'

def test_tree_add_by_path():
    tree = Tree('root', 'root')
    leaf = tree.create_node_from_path('child1.child1_1.child1_1_1', 'child1_1_1')
    assert leaf.value == 'child1_1_1'
    assert leaf.path == 'root.child1.child1_1.child1_1_1'
    assert leaf.parent.value is None
    assert leaf.parent.path == 'root.child1.child1_1'
    assert leaf.parent.parent.value is None
    assert leaf.parent.parent.path == 'root.child1'
    assert leaf.parent.parent.parent.value == 'root'
    assert leaf.parent.parent.parent.path == 'root'
