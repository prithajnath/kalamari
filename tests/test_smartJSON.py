from kalamari import smartJSON
import pytest


@pytest.fixture
def basic_json():
    '''Returns a basic smartJSON object, similar to the README.md example'''
    data = '''
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
    '''
    return smartJSON(data)


def test_get_attrs(basic_json):
    attrs = basic_json.get_attrs("author", "total_views")
    assert attrs == {'author': ['pythonguy226', 'jsguy995'], 'total_views': ['4561452', '784569']}


def test_max_video_views(basic_json):
    views = basic_json.get_attrs("total_views")
    views = map(int, views["total_views"])
    max_view = max(list(views))
    assert max_view == 4561452
