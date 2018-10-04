from exceptions import OverrideRootError


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []

        if self.parent:
            self.parent.add_child(self)

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data

    def add_child(self, node):
        self.children.append(node)

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    @classmethod
    def create_fake_root(cls, data="root"):
        return cls(data)


class Tree:
    def __init__(self, root=None):
        self.root = root
        if self.root:
            self.tree = {0: [self.root]}
        else:
            self.tree = {}

    def __getitem__(self, level):
        return self.tree[level]

    def __iter__(self):
        for i in self.tree:
            for j in self.tree[i]:
                yield (i, j)

    def add_node(self, node, level=0):
        if self.root:
            if level:
                try:
                    self.tree[level].append(node)
                except KeyError:
                    self.tree[level] = [node]
            else:
                raise OverrideRootError
        else:
            self.root = node
            self.tree.update({0: [self.root]})

    def reveal(self):
        # do bfs
        # print tree horizontally
        #           | --   node1 -- node3
        #   root -- |
        #           | --   node2 -- node4
        #                             |
        #                             | -- node5
        #                             | -- node6
        pass

    def head(self):
        # do bfs for 1 to 3 levels, depending on self.depth
        # print tree horizontally
        #           | --   node1 -- node3
        #   root -- |
        #           | --   node2 -- node4
        #                             |
        #                             | -- node5
        #                             | -- node6
        #                             | -- node7 -- ...
        pass

    def get_tree_depth(self):
        return max(list(self.tree.keys())) + 1

    @classmethod
    def tree_from_dict(cls, json_dict):
        from collections import deque
        tree = Tree()
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
                else:
                    node_obj = Node(i, current_parent)
                    tree.add_node(node_obj, current_obj['level'])
        return tree
