from dataclasses import field, dataclass
from typing import Any, Dict, List, Union

from uast.core.containers.containers_mixin import (
    JsonMixin,
    EqualityMixin,
)

__all__ = [
    "Variable",
    "Method",
    "Class",
    "Import",
    "Script",
]

_LEAF = "|-- "


@dataclass
class Variable(EqualityMixin, JsonMixin):
    """
    The class represents a variable with attributes for its name, value, variable type,
    and optional annotation. It provides methods for generating a dictionary representation,
    schema representation, and a string representation of its type and annotation.

    :param name : str
        The name of the variable.
    :param value : Any, optional
        The value of the variable (default is None).
    :param variable_type : str, optional
        The type of the variable (default is an empty string).
    :param annotation : Any, optional
        The annotation of the variable (default is None).
    """
    name: str
    value: Any = field(default=None)
    variable_type: str = ""
    annotation: Any = field(default=None)

    def __dict__(self) -> Dict:
        """
        Generate a dictionary representation of the class.

        :return: A dictionary representation of the variable.
        :rtype: Dict
        """
        return {
            "name": self.name,
            "value": self.value,
            "variable_type": self.variable_type,
            "annotation": self.annotation,
        }

    def schema(self, _prefix: str = "", _with_leaf: bool = False) -> str:
        """
        Generate a schema representation of the class.

        :param _prefix: A prefix string to prepend to the schema representation (default is "").
        :type _prefix: str
        :param _with_leaf: A boolean flag indicating whether to include leaf indicators in the schema representation
            (default is False).
        :type _with_leaf: bool

        :return: A schema representation of the class.
        :rtype: str
        """
        return f"{_prefix}{_LEAF * _with_leaf}{self.name}: {self.variable_type} {self._type_and_annotation_repr()}"

    def _type_and_annotation_repr(self) -> str:
        """
        The method generates a string representation of the type and annotation of a variable. If both the annotation
        and the value of the variable are present, the string includes both the annotation and the value. If only the
        annotation is present, the string includes only the annotation. If only the value is present, the string
        includes only the value. If neither the annotation nor the value is present, an empty string is returned.

        :return: A string representing the type and annotation of the variable.
        :rtype: str
        """
        if self.annotation and self.value:
            return f"(annotation: {self.annotation}, value: {self.value})"
        elif self.annotation:
            return f"(annotation: {self.annotation})"
        elif self.value:
            return f"(value: {self.value})"
        return ""


@dataclass
class Method(EqualityMixin, JsonMixin):
    name: str
    arguments: List[Variable] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)

    def __dict__(self) -> Dict:
        """
        Generate a dictionary representation of the class.

        :return: A dictionary representation of the variable.
        :rtype: Dict
        """
        return {
            "name": self.name,
            "arguments": [_argument.__dict__() for _argument in self.arguments],
            "decorators": self.decorators,
        }

    @property
    def arguments_names(self) -> List[str]:
        """
        The property returns a list containing the names of the arguments associated with the method.

        :return: A list containing the names of the arguments.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.arguments)

    def schema(self, _prefix: str = "", _indent: int = 1, _with_leaf: bool = False) -> str:
        """
        Generate a schema representation of the class.

        :param _prefix: A prefix string to prepend to the schema representation (default is "").
        :type _prefix: str
        :param _indent: An integer to set the indent.
        :type _indent: int
        :param _with_leaf: A boolean flag indicating whether to include leaf indicators in the schema representation
            (default is False).
        :type _with_leaf: bool

        :return: A schema representation of the class.
        :rtype: str
        """
        schema = f"{_prefix}{_LEAF * _with_leaf}{self.name}: method {self._decorator_representation()}"
        for argument in self.arguments:
            schema += "\n"
            schema += argument.schema(
                _prefix=_generate_prefix(prefix=_prefix, indent=_indent, with_leaf=_with_leaf),
                _with_leaf=True,
            )
        return schema

    def _decorator_representation(self) -> str:
        return f"(decorators: {', '.join(self.decorators)})" if self.decorators else ""


@dataclass
class Class(EqualityMixin, JsonMixin):
    name: str
    bases: List[str] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
    class_variables: List[Variable] = field(default_factory=list)
    instance_variables: List[Variable] = field(default_factory=list)

    def __dict__(self) -> Dict:
        """
        Generate a dictionary representation of the class.

        :return: A dictionary representation of the variable.
        :rtype: Dict
        """
        return {
            "name": self.name,
            "bases": self.bases,
            "methods": [_methods.__dict__() for _methods in self.methods],
            "class_variables": [_variable.__dict__() for _variable in self.class_variables],
            "instance_variables": [_variable.__dict__() for _variable in self.instance_variables],
        }

    @property
    def class_variables_names(self) -> List[str]:
        """
        The property returns a list containing the names of the class variables associated with the class.

        :return: A list containing the names of the class variables.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.class_variables)

    @property
    def instance_variables_names(self) -> List[str]:
        """
        The property returns a list containing the names of the instance variables associated with the class.

        :return: A list containing the names of the instance variables.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.instance_variables)

    @property
    def methods_names(self) -> List[str]:
        """
        The property returns a list containing the names of the methods associated with the class.

        :return: A list containing the names of the methods.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.methods)

    def schema(self, _prefix: str = "", _indent: int = 1, _with_leaf: bool = False) -> str:
        """
        Generate a schema representation of the class.

        :param _prefix: A prefix string to prepend to the schema representation (default is "").
        :type _prefix: str
        :param _indent: An integer to set the indent.
        :type _indent: int
        :param _with_leaf: A boolean flag indicating whether to include leaf indicators in the schema representation
            (default is False).
        :type _with_leaf: bool

        :return: A schema representation of the class.
        :rtype: str
        """
        schema = f"{_prefix}{_LEAF * _with_leaf}{self.name}: class {self._base_representation()}"

        for class_variable in self.class_variables:
            schema += "\n"
            schema += class_variable.schema(_prefix=f"{_prefix}{'|' * _with_leaf}{' ' * _indent}{_LEAF}")

        for method in self.methods:
            schema += "\n"
            schema += method.schema(
                _prefix=_generate_prefix(prefix=_prefix, indent=_indent, with_leaf=_with_leaf),
                _indent=4,
                _with_leaf=True
            )
        return schema

    def _base_representation(self) -> str:
        """
        The method generates a string representation of the bases from which the class extends. If the class has
        one or more bases, the string includes the phrase "extends from" followed by a comma-separated list of the
        base names. If the class has no bases, an empty string is returned.

        :return: A string representing the bases from which the class extends.
        :rtype: str
        """
        return f"(extends from: {', '.join(self.bases)})" if self.bases else ""


@dataclass
class Import(EqualityMixin, JsonMixin):
    module: str
    component: str = None
    asname: str = None

    def __dict__(self) -> Dict[str, str]:
        """
        Generate a dictionary representation of the class.

        :return: A dictionary representation of the variable.
        :rtype: Dict
        """
        return {
            "module": self.module,
            "component": self.component,
            "asname": self.asname,
        }

    def schema(self, _prefix: str = "", _with_leaf: bool = False) -> str:
        """
        Generate a schema representation of the class.

        :param _prefix: A prefix string to prepend to the schema representation (default is "").
        :type _prefix: str
        :param _with_leaf: A boolean flag indicating whether to include leaf indicators in the schema representation
            (default is False).
        :type _with_leaf: bool

        :return: A schema representation of the class.
        :rtype: str
        """
        schema = f"{_prefix}{_LEAF * _with_leaf}"

        if self.component is None:
            return schema + f"import {self.module}"
        if self.component is not None and self.asname is None:
            return schema + f"from {self.module} import {self.component}"
        if self.component is not None and self.asname is not None:
            return schema + f"from {self.module} import {self.component} as {self.asname}"


@dataclass
class Script(EqualityMixin, JsonMixin):
    name: str
    imports: List[Import] = field(default_factory=list)
    global_variables: List[Variable] = field(default_factory=list)
    classes: List[Class] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)

    def __dict__(self) -> Dict[str, Union[str, List[Dict]]]:
        """
        Generate a dictionary representation of the class.

        :return: A dictionary representation of the variable.
        :rtype: Dict
        """
        return {
            "name": self.name,
            "imports": [_import.__dict__() for _import in self.imports],
            "global_variables": [_variable.__dict__() for _variable in self.global_variables],
            "classes": [_class.__dict__() for _class in self.classes],
            "methods": [_methods.__dict__() for _methods in self.methods],
        }

    @property
    def import_modules(self) -> List[str]:
        """
        The property returns a list containing the names of the imports associated with the script.

        :return: A list containing the names of the imports.
        :rtype: List[str]
        """
        return [import_.module for import_ in self.imports]

    @property
    def global_variables_names(self) -> List[str]:
        """
        The property returns a list containing the names of the global variables associated with the script.

        :return: A list containing the names of the global variables.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.global_variables)

    @property
    def classes_names(self) -> List[str]:
        """
        The property returns a list containing the names of the classes associated with the script.

        :return: A list containing the names of the classes.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.classes)

    @property
    def methods_names(self) -> List[str]:
        """
        The property returns a list containing the names of the method associated with the script.

        :return: A list containing the names of the methods.
        :rtype: List[str]
        """
        return _return_container_names(containers=self.methods)

    def schema(self) -> str:
        """
        Generate a schema representation of the class.

        :return: A schema representation of the class.
        :rtype: str
        """
        schema = f"{self.name}"

        if self.imports:
            schema += "\n"
            schema += f" {_LEAF}imports"

            for import_ in self.imports:
                schema += "\n"
                schema += import_.schema(_prefix=" |    ", _with_leaf=True)

        for global_variable in self.global_variables:
            schema += "\n"
            schema += global_variable.schema(_prefix=f" {_LEAF}")

        for class_ in self.classes:
            schema += "\n"
            schema += class_.schema(_prefix=" ", _indent=4, _with_leaf=True)

        for method in self.methods:
            schema += "\n"
            schema += method.schema(_prefix=" ", _indent=4, _with_leaf=True)

        return schema


def _generate_prefix(prefix: str, indent: int, with_leaf: bool) -> str:
    """
    The method generates a prefix string to create the schema of a container. The prefix string is composed of the
    base prefix, followed by a leaf symbol (if `with_leaf` is True), and additional indentation spaces
    (specified by `indent`).

    :param prefix: The base prefix string.
    :type prefix: str
    :param indent: The number of spaces to indent.
    :type indent: int
    :param with_leaf: Whether to include a leaf symbol.
    :type with_leaf: bool

    :return: The formatted prefix string.
    :rtype: str
    """
    return f"{prefix}{'|' * with_leaf}{' ' * indent}"


def _return_container_names(containers: List[Union[Variable, Method, Class, Script]]) -> List[str]:
    """
    The method takes a list of container objects, which can include variables, methods, classes, or scripts,
    and extracts their names. It returns a list containing the names of all the containers in the input list.

    :param containers: A list of container objects (variables, methods, classes, or scripts).
    :type containers: List[Union[Variable, Method, Class, Script]]

    :return: A list containing the names of the containers.
    :rtype: List[str]
    """
    return [container.name for container in containers]
