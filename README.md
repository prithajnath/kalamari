## Kalamari
Kalamari is a Python package that makes extracting data from JSON a lot easier. Instead of typing out explicit absolute paths to desired keys, you can just pass them as parameters to kalamari methods.

### Initialization
All major extraction methods are available through instances of the `smartJSON` class.
```py
>>> from kalamari import smartJSON
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
      "email": "pythonguy226@gmail.com",
      "total_views": "4561452"
    },
    "1": {
      "title": "JavaScript async await",
      "url": "https://myvid.com/784F5gF9800e",
      "author": "jsguy995",
      "email": "jsguy995@gmail.com",
      "total_views": "784569"
    }
  }
}
```

With kalamari, this can be achieved with only a few lines of code

```py
>>> _views = data.get_attrs("total_views")
>>> views = max(map(int, _views["total_views"]))
>>> views
>>> 4561452
```
Pretty cool right? You can also fetch more than one attribute at a time.

```py
>>> views_w_authors = data.get_attrs("author","total_views")
>>> views_w_authors
>>> {'author': ['pythonguy226', 'jsguy995'], 'total_views': ['4561452', '784569']}
```
### Extraction methods

* `get_attrs()`
 * This is the simplest method. It accepts the names of all the attributes that you wish to extract and returns a `dict`. (Used in above example)
* `get_attrs_by_value_regex()`
 * This method accepts a regular expression and returns all attributes whose values match that regular expression

 ```py
>>> attrs_w_guy = data.get_attrs_by_value_regex("(.*)guy(.*)")
>>> attrs_w_guy
>>> {'author': ['pythonguy226', 'jsguy995'], 'email': ['pythonguy226@gmail.com', 'jsguy995@gmail.com']}
 ```
