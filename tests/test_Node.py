from kalamari import Node
import pytest


@pytest.fixture
def data_node():
    parent = Node("root")
    node = Node("zip",parent)
    node.add_value("05401")

    return (node, parent)


@pytest.fixture
def node_w_children():
    root = Node("root")
    students_node = Node("students",root)

    student_one_name = Node("name", students_node)
    student_one_name.add_value("Theo")

    student_two_name = Node("name", students_node)
    student_two_name.add_value("Rachel")

    return (students_node, student_one_name, student_two_name)


def test_node_identity():
    a = Node("a")
    b = Node("a")

    assert id(a) != id(b) and hash(a) != hash(b)


def test_get_parent(data_node):
    node, parent = data_node
    assert node.get_parent() == parent


def test_get_children(node_w_children):
    p, c1, c2 = node_w_children
    children = p.get_children()
    assert c1 in children and c2 in children
