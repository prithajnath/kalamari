from .exceptions import OverrideRootError, TreeHeightError
from typing import List


class Node:
    def __init__(self, data: str, parent: None or 'Node'=None) -> None:
        self.data = data # name of Node
        self.parent = parent # reference to parent Node object
        self.children = [] # list of children Node objects
        self.container = [] # list to contain values. Should be empty if instance has children

        if self.parent:
            self.parent.add_child(self)

    def __str__(self) -> str:
        return self.data

    def __repr__(self) -> str:
        return self.data

    def add_child(self, node: 'Node') -> None:
        self.children.append(node)

    def add_parent(self, node: 'Node') -> None:
        self.parent = node
        node.children.append(self)

    def add_value(self, value: str) -> None:
        self.container.append(value)

    def get_parent(self) -> 'Node':
        return self.parent

    def get_children(self) -> List['Node']:
        return self.children

    def get_value(self) -> 'Node' or str:
        if len(self.container) == 1:
            return self.container[0]
        else:
            return self.container

class Tree:
    def __init__(self, root: None or Node =None) -> None:
        self.root = root
        if self.root:
            self.tree = {0: [self.root]}
        else:
            self.tree = {}

    def __repr__(self) -> str:
        return str(self.tree)

    def __getitem__(self, level: int) -> List[Node]:
        return self.tree[level]

    def __iter__(self) -> (int, Node):
        for i in self.tree:
            for j in self.tree[i]:
                yield (i, j)

    def add_node(self, node: Node, level: int =0) -> None:
        if self.root:
            if level:
                try:
                    if level <= self.depth:
                        self.tree[level].append(node)
                    else:
                        raise TreeHeightError
                except KeyError:
                    self.tree[level] = [node]
            else:
                raise OverrideRootError
        else:
            self.root = node
            self.tree.update({0: [self.root]})

    def reveal(self) -> str:
        res = self.print_tree(self.root, "", True, 1000)  # assuming a max depth of a 1000.
        return res

    def peek(self) -> str:
        if (self.depth > 3):
            res = self.print_tree(self.root, "", True, 3)
            return res

        # since the tree is small, just reveal the whole tree
        self.reveal()


    '''
    the idea is to recurse through the tree and pretty-print the node and the children
    the indent (string) and the last_child (bool) keeps track of which child we look at and
    indent accordingly. The max_depth (int) and depth (int) are used by the peek() function
    to limit how deep in the tree we traverse.
    '''
    def print_tree(self, node: Node, indent: str, last_child: bool, max_depth: int, depth: int =0) -> str:
        ret = indent + "+--" + str(node) + "\n"

        if depth > max_depth:
            return ret

        if last_child:
            indent += "   "
        else:
            indent += "|  "

        for index, child in enumerate(node.children):
            ret += self.print_tree(child, indent, index == len(node.children) - 1, max_depth, depth + 1)
        return ret

    @property
    def depth(self) -> int:
        return sum(1 for key in self.tree.keys())

    @classmethod
    def tree_from_dict(cls, json_dict: dict) -> 'Tree':
        from collections import deque
        tree = cls()
        q = deque()
        q.append({
            'parent': Node("root"),
            'children': json_dict,
            'level': 0
                })
        while q:
            current_obj = q.popleft()
            current_parent = current_obj['parent']
            if not tree.root:
                tree.add_node(current_parent)
                current_obj['level'] += 1
            for i in current_obj['children']:
                if type(current_obj['children'][i]) == dict:
                    node_obj = Node(i, current_parent)
                    q.append({
                        'parent': node_obj,
                        'children': current_obj['children'][i],
                        'level': current_obj['level'] + 1
                            })
                    tree.add_node(node_obj, current_obj['level'])
                elif type(current_obj['children'][i]) == list:
                    weird_list = current_obj['children'][i]
                    if weird_list:
                        list_type = type(weird_list[0])
                        if list_type == str:
                            # Create Node instances from str values and add them to the tree
                            node_obj = Node(i, current_parent)
                            for some_str in weird_list:
                                node_obj.add_value(some_str)
                            tree.add_node(node_obj, current_obj['level'])
                        elif list_type == dict:
                            # Append dicts to queue, w respective parent and level values
                            node_obj = Node(i, current_parent)
                            for some_dict in weird_list:
                                q.append({
                                    'parent': node_obj,
                                    'children': some_dict,
                                    'level': current_obj['level'] + 1
                                })
                else:
                    node_obj = Node(i, current_parent)
                    node_obj.add_value(current_obj['children'][i])
                    tree.add_node(node_obj, current_obj['level'])
        return tree
