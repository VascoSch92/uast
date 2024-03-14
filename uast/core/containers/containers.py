from dataclasses import field, dataclass
from typing import Any, Dict, List, Union

from uast.core.containers.containers_mixin import EqualityMixin, JsonMixin

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
    name: str
    value: Any = field(default=None)
    variable_type: str = ""
    annotation: Any = field(default=None)

    def __dict__(self) -> Dict:
        return {
            "name": self.name,
            "value": self.value,
            "variable_type": self.variable_type,
            "annotation": self.annotation,
        }

    def schema(self, _prefix: str = "", _with_leaf: bool = False) -> str:
        return f"{_prefix}{_LEAF * _with_leaf}{self.name}: {self.variable_type} {self._type_and_annotation_repr()}"

    def _type_and_annotation_repr(self) -> str:
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
        return {
            "name": self.name,
            "arguments": [_argument.__dict__() for _argument in self.arguments],
            "decorators": self.decorators,
        }

    @property
    def arguments_names(self) -> List[str]:
        return _return_container_names(containers=self.arguments)

    def schema(self, _prefix: str = "", _indent: int = 1, _with_leaf: bool = False) -> str:
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
        return {
            "name": self.name,
            "bases": self.bases,
            "methods": [_methods.__dict__() for _methods in self.methods],
            "class_variables": [_variable.__dict__() for _variable in self.class_variables],
            "instance_variables": [_variable.__dict__() for _variable in self.instance_variables],
        }

    @property
    def class_variables_names(self) -> List[str]:
        return _return_container_names(containers=self.class_variables)

    @property
    def instance_variables_names(self) -> List[str]:
        return _return_container_names(containers=self.instance_variables)

    @property
    def methods_names(self) -> List[str]:
        return _return_container_names(containers=self.methods)

    def schema(self, _prefix: str = "", _indent: int = 1, _with_leaf: bool = False) -> str:
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
        return f"(extends from: {', '.join(self.bases)})" if self.bases else ""


@dataclass
class Import(EqualityMixin, JsonMixin):
    module: str
    component: str = None
    asname: str = None

    def __dict__(self) -> Dict[str, str]:
        return {
            "module": self.module,
            "component": self.component,
            "asname": self.asname,
        }

    def schema(self, _prefix: str = "", _with_leaf: bool = False) -> str:
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
        return {
            "name": self.name,
            "imports": [_import.__dict__() for _import in self.imports],
            "global_variables": [_variable.__dict__() for _variable in self.global_variables],
            "classes": [_class.__dict__() for _class in self.classes],
            "methods": [_methods.__dict__() for _methods in self.methods],
        }

    @property
    def import_names(self) -> List[str]:
        return _return_container_names(containers=self.self.imports)

    @property
    def global_variables_names(self) -> List[str]:
        return _return_container_names(containers=self.global_variables)

    @property
    def classes_names(self) -> List[str]:
        return _return_container_names(containers=self.classes)

    @property
    def methods_names(self) -> List[str]:
        return _return_container_names(containers=self.methods)

    def schema(self) -> str:
        schema = f"{self.name}"

        if self.imports:
            schema += "\n"
            schema += f" {_LEAF}imports"

            for import_ in self.imports:
                schema += "\n"
                schema += import_.schema(_prefix=f" |    ", _with_leaf=True)

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
    return f"{prefix}{'|' * with_leaf}{' ' * indent}"


def _return_container_names(containers: List[Union[Variable, Method, Class, Script]]) -> List[str]:
    return [container.name for container in containers]
