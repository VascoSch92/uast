import json
from typing import Any, Dict


class EqualityMixin:
    """
    A mixin class for implementing equality comparison methods.

    This mixin provides an `__eq__` method to compare instances of the class
    for equality based on the equality between their container contents.
    """

    def __eq__(self, other) -> bool:
        """
        Compare two objects for equality.

        :param other: The object to compare against.
        :type other: Any

        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """
        return equality_between_containers(a=self, b=other, _type=type(self))


def equality_between_containers(a: Any, b: Any, _type: Any) -> bool:
    """
    The method compares two containers 'a' and 'b' of the specified type '_type'
    for equality. It first checks if 'b' is an instance of the specified type.
    If it is, it compares the dictionaries of attributes of both containers for equality
    using the `equality_between_dictionaries` function.

    :param a: The first container to compare.
    :type a: Any
    :param b: The second container to compare.
    :type b: Any
    :param _type: The type of the containers to be compared.
    :type _type: Any

    :return: True if the containers are equal, False otherwise.
    :rtype: bool
    """
    if isinstance(b, _type) is False:
        return False

    return _equality_between_dictionaries(a=a.__dict__(), b=b.__dict__())


def _equality_between_dictionaries(a: Dict, b: Dict) -> bool:
    """
    The method compares two dictionaries 'a' and 'b' for equality.
    It first checks if the keys of both dictionaries are the same.
    If they are, it iterates over the keys and checks if the values
    associated with each key are equal.

    :param a: The first dictionary to compare.
    :type a: Dict
    :param b: The second dictionary to compare.
    :type b: Dict

    :return: True if the dictionaries are equal, False otherwise.
    :rtype: bool
    """
    if a.keys != b.keys():
        return False
    for key in a.keys():
        if a[key] != b[key]:
            return False
    return True


class JsonMixin:
    """
    A mixin class for providing JSON serialization capability.

    The mixin class provides a `json` method to serialize an object's attributes
    into a JSON string.
    """

    def json(self) -> str:
        """
        Serialize the object's attributes into a JSON string.

        :return: A JSON string representing the object's attributes.
        :rtype: str
        """
        return json.dumps(self.__dict__(), indent=4)
