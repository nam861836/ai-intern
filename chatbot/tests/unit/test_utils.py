import pytest
from app.utils.utils import get_value_from_dict

def test_get_value_from_dict_single_key():
    data = {'a': 1, 'b': 2}
    fn = get_value_from_dict('a', data)
    assert fn() == 1

def test_get_value_from_dict_key_path():
    data = {'a': {'b': {'c': 42}}}
    fn = get_value_from_dict('a.b.c', data)
    assert fn() == 42

def test_get_value_from_dict_default():
    data = {'a': 1}
    fn = get_value_from_dict('missing', data, default=99)
    assert fn() == 99

def test_get_value_from_dict_keyerror():
    data = {'a': 1}
    fn = get_value_from_dict('missing', data)
    with pytest.raises(KeyError):
        fn()
