from collections import deque
from json import loads


class smartJSON:
    def __init__(self, json):
        self.json = loads(json)

    def get_attrs(self, *attrs):
        q, result = deque(), {i: [] for i in attrs}
        q.append(self.json)
        while q:
            current_obj = q.popleft()
            for key in current_obj:
                if type(current_obj[key]) != dict:
                    if key in result:
                        result[key].append(current_obj[key])
                else:
                    q.append(current_obj[key])
        return result

    def get_attrs_preorder(self, *attrs):
        stack, result = [], {i: [] for i in attrs}
        stack.append(self.json)
        while stack:
            current_obj = stack.pop()
            for key in current_obj:
                if type(current_obj[key]) != dict:
                    if key in result:
                        result[key].append(current_obj[key])
                else:
                    stack.append(current_obj[key])
        return result
