## Calabar
Calabar is a Python package that makes extracting data from JSON a lot easier. Instead of typing out explicit absolute paths to desired keys, you can just pass them as parameters to calabar methods or use query strings. You can also choose your preferred way of traversal.

### Initialization
All major extraction methods are available through instances of the `smartJSON` class.
```py
>>> from calabar import smartJSON
>>> import requests
>>> r = requests.get('https://yourapi.io/someendpoint') # returns some JSON
>>> data = smartJSON(r.content)
```

Say that the above GET request returns the following information and you'd like to extract the highest number of views accumulated for a video

```json
{
  "videos": {
    "0": {
      "title": "Pytest tutorial (1/5)",
      "url": "https://myvid.com/454F5gK9700e",
      "author": "pythonguy226",
      "total_views": "4561452"
    },
    "1": {
      "title": "JavaScript async await",
      "url": "https://myvid.com/784F5gF9800e",
      "author": "jsguy995",
      "total_views": "784569"
    }
  }
}
```

With calabar, this can be achieved with only a few lines of code

```py
>>> _views = data.get_attrs("total_views")
>>> views = max(map(int, _views["total_views"]))
>>> views
>>> 4561452
```

### Level order methods

* `get_attrs()`
