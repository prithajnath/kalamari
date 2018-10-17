from kalamari import Node, Tree, TreeHeightError, OverrideRootError
import pytest


@pytest.fixture
def three_unlrelated_nodes():
    a = Node("a")
    b = Node("b")
    c = Node("c")

    return (a,b,c)

def test_add_node_wo_root(three_unlrelated_nodes):
    root, n1, n2 = three_unlrelated_nodes
    tree = Tree()
    tree.add_node(root)
    tree.add_node(n1, 1)
    tree.add_node(n2, 1)

    assert root in tree.tree[0] and {n1, n2} == set(tree.tree[1])


def test_add_node_w_root(three_unlrelated_nodes):
    root, n1, n2 = three_unlrelated_nodes
    tree = Tree(root)
    tree.add_node(n1,1)
    tree.add_node(n2, 1)

    assert root in tree.tree[0] and {n1, n2} == set(tree.tree[1])

def test_tree_height_error(three_unlrelated_nodes):
    root, n1, _ = three_unlrelated_nodes
    tree = Tree()
    tree.add_node(root)
    with pytest.raises(TreeHeightError):
        tree.add_node(n1, 2)


def test_override_root(three_unlrelated_nodes):
    root, n1, _ = three_unlrelated_nodes
    tree = Tree()
    tree.add_node(root)
    with pytest.raises(OverrideRootError):
        tree.add_node(n1, 0)
