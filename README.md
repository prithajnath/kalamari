## Kalamari
[![Build Status](https://travis-ci.org/prithajnath/kalamari.svg?branch=master)](https://travis-ci.org/prithajnath/kalamari)

Kalamari is a convenience wrapper for Python's built-in `json` module that makes extracting data from JSON a lot easier. Instead of typing out absolute paths to your desired keys, you can just pass the keys as parameters to kalamari methods.

### Installation
This package is not available through PyPI yet, so you have to manually install it. Go ahead and clone the repository and run the following command

```sh
python3 setup.py sdist
```
This will create a sub-directory called `dist` which will contain a compressed archive file. The file format defaults to `tar.gz` on POSIX systems and `.zip` on Windows.

After creating this archive file, you can install the package via `pip3`

```sh
sudo pip3 install kalamari-0.1dev.tar.gz
```

### Initialization
All major extraction methods are available through instances of the `smartJSON` class.
```py
>>> from kalamari import smartJSON
>>> import requests
>>> r = requests.get('https://yourapi.io/someendpoint') # returns some JSON
>>> data = smartJSON(r.content)
```
### Usage
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
* `get_attrs_by_key()`
 * This method accepts a regular expression and returns all attributes that match that regular expression
* `get_attrs_by_value()`
 * This method accepts a regular expression and returns all attributes whose values match that regular expression

 ```py
>>> attrs_w_numbers = data.get_attrs_by_value("[0-9]")
>>> attrs_w_numbers
>>> {'title': ['Pytest tutorial (1/5)'], 'url': ['https://myvid.com/454F5gK9700e', 'https://myvid.com/784F5gF9800e'], 'author': ['pythonguy226', 'jsguy995'], 'email': ['pythonguy226@gmail.com', 'jsguy995@gmail.com'], 'total_views': ['4561452', '784569']}
 ```
* `get_attrs_by_parent()`
 * This method accepts a regular expression and returns all attributes whose immediate parent matches that regular expression

### TODO
 * Add method chaining
    * All methods should return a `smartJSON` object.
    * A `smartJSON` object should be convertible to a `dict`
