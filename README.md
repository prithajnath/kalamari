## Calabar
Calabar is a Python package that makes extracting data from JSON a lot easier. Instead of typing out explicit absolute paths to desired keys, you can just pass them as parameters to calabar methods or use query strings. You can also choose your preferred way of traversal.

### Initialization
All major extraction methods are available through instances of the `smartJSON` class.
```
>>> from calabar.calabar import smartJSON
>>> import requests
>>> r = requests.get('https://yourapi.io/someendpoint') # returns some JSON
>>> data = smartJSON(r.content)
```


### Level order methods

* `get_attrs()`
