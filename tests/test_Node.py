from kalamari import Node
import pytest


@pytest.fixture
def node_w_children():
    root = Node("root")
    students_node = Node("students",root)

    student_one_name = Node("name", students_node)
    student_one_name.add_value("Theo")

    student_two_name = Node("name", students_node)
    student_two_name.add_value("Rachel")

    return (students_node, student_one_name, student_two_name)



@pytest.fixture
def two_unrelated_nodes():
    node_one = Node("name")
    node_one.add_value("Michael")

    node_two = Node("name")
    node_two.add_value("Justin")

    return (node_one, node_two)

def test_node_identity():
    a = Node("a")
    b = Node("a")
    assert id(a) != id(b) and hash(a) != hash(b)


def test_get_parent(node_w_children):
    parent, node, _ = node_w_children
    assert node.get_parent() == parent


def test_get_children(node_w_children):
    p, c1, c2 = node_w_children
    children = p.get_children()
    assert c1 in children and c2 in children

def test_get_value(node_w_children):
    _, n1, n2 = node_w_children
    desired_values = set(n1.container + n2.container)
    assert n1.get_value() in desired_values and n2.get_value() in desired_values


def test_add_child(two_unrelated_nodes):
    n1, n2 = two_unrelated_nodes
    n1.add_child(n2)
    assert n2 in n1.children

def test_add_parent(two_unrelated_nodes):
    n1, n2 = two_unrelated_nodes
    n1.add_parent(n2)
    assert n2 == n1.parent and n1 in n2.children

def test_add_value():
    a = Node("a")
    a.add_value(25)
    assert 25 in a.container
