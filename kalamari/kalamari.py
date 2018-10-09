from json import loads
from .tree import Tree
import re
import os


class smartJSON:
    def __init__(self, json):
        if type(json) == dict:
            self.json = Tree.tree_from_dict(json)
        else:
            if os.path.isfile(json):
                with open(json, "r") as f:
                    self.json = Tree.tree_from_dict(loads(f.read()))
            else:
                self.json = Tree.tree_from_dict(loads(json))

    def __repr__(self):
        result = {}
        for node in self.json[1]:
            if node.children:
                result[node.data] = "{...}"
            if node.container:
                result[node.data] = "..."
        return str(result)

    def __len__(self):
        return self.json.depth

    def __getitem__(self, key):
        if isinstance(key, slice):
            result = []
            for i in range(len(self.json.tree)):
                result.append(self.json[i])
            return result[key]
        elif isinstance(key, int):
            return self.json[key]

    def get_attrs(self, *attrs):
        result = {i: [] for i in attrs}
        for n, node in self.json:
            if node.data in attrs:
                result[node.data].append(node.get_value())
        return result

    def get_attrs_by(self, f, *attrs):
        result = {}
        for n, node in self.json:
            try:
                if f(n, node) and node.container:
                    if node.data in attrs:
                        try:
                            result[node.data].append(node.get_value())
                        except KeyError:
                            result[node.data] = [node.get_value()]
            except AttributeError: # tree exhausted
                continue
        return result

    def get_attrs_by_value(self, rule):
        result = {}
        regex = re.compile(rule)
        for n, node in self.json:
            if node.container:
                match = regex.search(node.get_value())
                if match:
                    try:
                        result[node.data].append(node.get_value())
                    except KeyError:
                        result[node.data] = [node.get_value()]
        return result

    def get_attrs_by_key(self, rule):
        result = {}
        regex = re.compile(rule)
        for n, node in self.json:
            if node.container:
                match = regex.search(node.data)
                if match:
                    try:
                        result[node.data].append(node.get_value())
                    except KeyError:
                        result[node.data] = [node.get_value()]
        return result

    def get_attrs_by_parent(self, rule, *attrs):
        regex = re.compile(rule)
        result = {}
        for n, node in self.json:
            if node.children:
                match = regex.search(node.data)
                if match:
                    node_children = node.get_children()
                    value_dict = {child.data:child.get_value() for child in node_children}
                    try:
                        result[node.data].append(value_dict)
                    except KeyError:
                        result[node.data] = [value_dict]
        return result


    def reveal(self):
        if self.json == None:
            print("No data available")
            return None
        res = self.json.reveal()
        print(res)
        return res

    def peek(self):
        if self.json == None:
            print("No data available")
            return None
        res = self.json.peek()
        print(res)
        return res

      
    def revert_smartJSON(self, current_node):
        if type(current_node).__name__ == 'Node':
            if len(current_node.container) == 1 :
                return {str(current_node.data): current_node.container[0]}
            else:
                return {str(current_node.data): current_node.container}
        else:
            if len(current_node) == 1:
                current_node = current_node[0]
                if current_node.container != []:
                    if len(current_node.container) == 1:
                        return {str(current_node.data): current_node.container[0]}
                    else:
                        return {str(current_node.data): current_node.container}
                else:
                    res = self.revert_smartJSON(current_node.children)
                    return {str(current_node.data): res}
            else:
                res = {}
                for i in range(len(current_node)):
                    if current_node[i].container != []:
                        if len(current_node[i].container) == 1:
                            res = {**res, str(current_node[i].data): current_node[i].container[0]}
                        else:
                            res = {**res, str(current_node[i].data): current_node[i].container}
                    else:
                        r = self.revert_smartJSON(current_node[i].children)
                        res = {**res, str(current_node[i]): r}
                return res

    def __iter__(self):
        reverted_tree = self.revert_smartJSON(self.json[0])
        for x, y in reverted_tree['root'].items():
            yield x, y
