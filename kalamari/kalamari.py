from collections import deque
from json import loads
import re
import os


class smartJSON:
    def __init__(self, json):
        if type(json) == dict:
            self.json = json
        else:
            if os.path.isfile(json):
                with open(json, "r") as f:
                    self.json = loads(f.read())
            else:
                self.json = loads(json)

    def __repr__(self):
        keys = {i:type(self.json[i]) for i in self.json.keys()}
        value_type_symbols = {dict:"{...}", list:"[...]", str:"..."}
        return "{ " + " , ".join([i + f" : {value_type_symbols[keys[i]]}" for i in keys]) + " }"

    def get_attrs(self, *attrs):
        q, result = deque(), {i: [] for i in attrs}
        q.append(self.json)
        while q:
            current_obj = q.popleft()
            for key in current_obj:
                if key in result:
                    result[key].append(current_obj[key])
                if type(current_obj[key]) == dict:
                    q.append(current_obj[key])
        return result

    def get_attrs_by_value(self, rule):
        q, result = deque(), {}
        regex = re.compile(rule)
        q.append(self.json)
        while q:
            current_obj = q.popleft()
            for key in current_obj:
                if type(current_obj[key]) == str:
                    match = regex.search(current_obj[key])
                    if match:
                        try:
                            result[key].append(current_obj[key])
                        except KeyError:
                            result[key] = [current_obj[key]]
                elif type(current_obj[key]) == dict:
                    q.append(current_obj[key])
        return result

    def get_attrs_by_key(self, rule):
        q, result = deque(), {}
        regex = re.compile(rule)
        q.append(self.json)
        while q:
            current_obj = q.popleft()
            for key in current_obj:
                match = regex.search(key)
                if match:
                    try:
                        result[key].append(current_obj[key])
                    except KeyError:
                        result[key] = [current_obj[key]]
                if type(current_obj[key]) == dict:
                    q.append(current_obj[key])
        return result

    def get_attrs_by_parent(self, rule, *attrs):
        q = deque()
        q.append(self.json)
        regex = re.compile(rule)
        object_with_desired_parents = {}
        while q:
            current_obj = q.popleft()
            for key in current_obj:
                if type(current_obj[key]) == dict:
                    match = regex.search(key)
                    if match:
                        try:
                            object_with_desired_parents[key].append(current_obj[key])
                        except KeyError:
                            object_with_desired_parents[key] = [current_obj[key]]
                    q.append(current_obj[key])
        return object_with_desired_parents
