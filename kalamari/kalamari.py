from collections import deque
from json import loads
import re


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

    def get_attrs_by_value(self, rule):
        q, result = deque(), {}
        regex = re.compile(rule)
        q.append(self.json)
        while q:
            current_obj = q.popleft()
            for key in current_obj:
                if type(current_obj[key]) != dict:
                    match = regex.search(current_obj[key])
                    if match:
                        try:
                            result[key].append(current_obj[key])
                        except KeyError:
                            result[key] = [current_obj[key]]
                else:
                    q.append(current_obj[key])
        return result
