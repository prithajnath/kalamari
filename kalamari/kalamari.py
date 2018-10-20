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
                if f(n, node):
                    if node.container:
                        if node.data in attrs:
                            try:
                                result[node.data].append(node.get_value())
                            except KeyError:
                                result[node.data] = [node.get_value()]
                    else: # has children (only grabs string key:values and does not traverse deeper children dicts)
                        if node.data in attrs:
                            children = node.get_children()
                            data_nodes = [k for k in children if not k.container]
                            container_nodes = [j for j in children if j.container]
                            data_node_values = {kk.data:"{...}" for kk in data_nodes}
                            container_nodes_values = {jj.data:jj.get_value() for jj in container_nodes}

                            try:
                                result[node.data].append({**data_node_values, **container_nodes_values})
                            except KeyError:
                                result[node.data] = [{**data_node_values, **container_nodes_values}]
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
