import ast
from typing import Any, List, Union, Literal
from collections import defaultdict

from uast.core.containers.containers import (
    Class,
    Import,
    Method,
    Variable,
)

__all__ = [
    "parse_ast_assign",
    "parse_ast_import",
    "parse_ast_class_def",
    "parse_ast_ann_assign",
    "parse_ast_import_from",
    "parse_ast_function_def",
]


def _check_argument_type(expected: Any, got: Any) -> None:
    """
    Privet method that check if the type of the input matches the expected type.

    :param expected: The expected type of the input.
    :type expected: Any

    :param got: The input value to be checked.
    :type got: Any

    :return: None

    :raises TypeError: If the type of the expected argument is not equal to the type of the got argument.
    """
    if isinstance(got, expected) is False:
        raise TypeError(f"Input must be an instance of {expected}. Got {type(got)}.")


def parse_value(value: Any) -> str:
    """
    Get the string representation of the provided value.

    :param value: The value to be parsed.
    :type value: Union[str, int, ast.Constant, ast.List, ast.Dict, ast.Tuple, ast.Call]

    :return: The string representation of the provided value.
    :rtype: str

    :raises TypeError: If the type of the value is not supported for parsing.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return value.__str__()
    if isinstance(value, ast.Constant):
        return parse_ast_constant(ast_constant=value)
    elif isinstance(value, ast.List):
        return parse_ast_list(ast_list=value)
    elif isinstance(value, ast.Dict):
        return parse_ast_dict(ast_dict=value)
    elif isinstance(value, ast.Tuple):
        output = []
        for _value in value.elts:
            if isinstance(_value, ast.Constant):
                output.append(parse_ast_constant(ast_constant=_value))
            else:
                output.append(parse_value(value=_value))
        return ", ".join(output)
    elif isinstance(value, ast.Call):
        return parse_ast_call(value)
    else:
        raise TypeError(f"Unable to parse value with type {type(value)}.")


def parse_ast_constant(ast_constant: ast.Constant) -> str:
    """
    Parses an abstract syntax tree (AST) constant into its string representation.

    :param ast_constant: The AST constant to parse.
    :type ast_constant: ast.Constant

    :return: The string representation of the parsed constant.
    :rtype: str

    :raises TypeError: If the input `ast_constant` is not an instance of `ast.Constant`,
                        or if the type of `ast_constant` is not recognized.

    :Example:

    >>> parse_ast_constant(ast.Constant(value=42))
    >>> '42'
    >>> parse_ast_constant(ast.Constant(value='hello'))
    >>> "'hello'"
    """
    _check_argument_type(expected=ast.Constant, got=ast_constant)

    if ast_constant.value is None:
        return "None"
    elif isinstance(ast_constant.value, int):
        return ast_constant.value.__str__()
    elif isinstance(ast_constant.value, str):
        return f"'{ast_constant.value}'"
    else:
        raise TypeError(f"Unable to parse type {type(ast_constant.value)}.")


def parse_ast_list(ast_list: ast.List) -> str:
    """
    Parses an abstract syntax tree (AST) list into its string representation.

    This function iterates over the elements of the AST list, parsing each element
    using `_parse_ast_constant` if it is a constant. The parsed elements are then
    joined together to form a string representation of the list.

    :param ast_list: The AST list to parse.
    :type ast_list: ast.List

    :return: The string representation of the parsed list.
    :rtype: str

    :raises TypeError: If the input `ast_list` is not an instance of `ast.List`,
                        or if the type of `ast_list` is not recognized.

    :Example:

    >>> parse_ast_list(ast.List(elts=[ast.Constant(value=1), ast.Constant(value=2)]))
    >>> "[1, 2]"
    >>> parse_ast_list(ast.List(elts=[ast.Constant(value='hello'), ast.Constant(value='world')]))
    >>> "['hello', 'world']"
    """
    _check_argument_type(expected=ast.List, got=ast_list)

    _values = []
    for _value in ast_list.elts:
        if isinstance(_value, ast.Constant):
            _values.append(parse_ast_constant(ast_constant=_value))
        else:
            raise TypeError(f"Unable to parse type {type(_value)}.")

    return "[" + ", ".join(_values) + "]"


def parse_ast_dict(ast_dict: ast.Dict) -> str:
    """
    Parses an abstract syntax tree (AST) dictionary into its string representation.

    :param ast_dict: The AST dictionary to parse.
    :type ast_dict: ast.Dict

    :return: The string representation of the parsed dictionary.
    :rtype: str

    :raises TypeError: If the input `ast_dict` is not an instance of `ast.Dict`.

    :Examples:

    >>> parse_ast_dict(
    >>>     ast_dict=ast.Dict(
    >>>         keys=[ast.Constant(value='a'), ast.Constant(value='b')],
    >>>         values=[ast.Constant(value=1), ast.Constant(value=2)]
    >>>     )
    >>>)
    >>> "{'a': 1, 'b': 2}"
    """
    _check_argument_type(expected=ast.Dict, got=ast_dict)

    _values = [
        (parse_value(value=_key), parse_value(value=value)) for _key, value in zip(ast_dict.keys, ast_dict.values)
    ]
    return "{" + ", ".join([f"{_key.__str__()}: {_value.__str__()}" for _key, _value in _values]) + "}"


def parse_func(func: Union[ast.Attribute, ast.Name]) -> str:
    """
    Parse the given function node and return its string representation.

    :param func: The function node to parse.
    :type func: Union[ast.Attribute, ast.Name]

    :return: The string representation of the parsed function.
    :rtype: str

    :raises TypeError: If the type of the function node is not supported for parsing.
    """
    if isinstance(func, ast.Attribute):
        attribute = func.attr
        if hasattr(func, "value"):
            if isinstance(func.value, ast.Name):
                return f"{func.value.id}.{attribute}"
            elif isinstance(func.value, ast.Call):
                parsed_call = parse_ast_call(ast_call=func.value)
                return f"{parsed_call}.{attribute}"
    elif isinstance(func, ast.Name):
        return f"{func.id}"
    else:
        raise TypeError(f"Unable to parse func of type {type(func)}.")


def parse_ast_call(ast_call: ast.Call) -> str:
    """
    Parse the given ast.Call node and return its string representation.

    :param ast_call: The ast.Call node to parse.
    :type ast_call: ast.Call

    :return: The string representation of the parsed ast.Call.
    :rtype: str

    :raises TypeError: If the input is not an instance of ast.Call.
    """
    _check_argument_type(expected=ast.Call, got=ast_call)

    function = parse_func(func=ast_call.func)
    arguments = ", ".join([parse_value(value=value) for value in ast_call.args])

    arguments = "(" + arguments + ")" if function == "tuple" else arguments

    return f"{function}({arguments})"


def parse_ast_assign(
    assignments: ast.Assign,
    variable_type: Literal["class variable", "instance variable", "global variable"],
) -> List[Variable]:
    """
    Get variable containers for assignments in the provided AST node.

    The function extracts variable information from the assignments AST node and returns a list of Variable objects.

    :param assignments: The AST node representing assignments.
    :type assignments: ast.Assign
    :param variable_type: The type of variables being assigned. It could be "class variable", "instance variable",
            or "global variable".
    :type variable_type: Literal["class variable", "instance variable", "global variable"]

    :return: A list of Variable objects representing the assigned variables.
    :rtype: List[Variable]

    :raises TypeError: If the input is not an instance of ast.Assign.
    """
    _check_argument_type(expected=ast.Assign, got=assignments)

    for assignment in assignments.targets:
        if isinstance(assignment, ast.Name):
            return [
                Variable(
                    name=assignment.id,
                    value=parse_value(value=assignments.value),
                    variable_type=variable_type,
                )
                for assignment in assignments.targets
            ]
        elif isinstance(assignment, ast.Tuple):
            return [
                Variable(
                    name=assignment.id,
                    value=parse_value(value=_value.value),
                    variable_type=variable_type,
                )
                for assignment, _value in zip(assignments.targets[0].elts, assignments.value.elts)
            ]


def _parse_type_from_annotation(annotation: Any) -> Union[str, None]:
    """
    Parse the type information from the given annotation and return its string representation.

    :param annotation: The annotation to parse.
    :type annotation: Any

    :return: The string representation of the parsed type information.
    :rtype: Union[str, None]

    This function takes an annotation as input and returns its string representation. It supports various
    types of annotations including basic types (int, str), constants, names, subscripts, slices, attributes,
    indexes, tuples, etc.

    If the annotation is None, it returns None. If the annotation cannot be parsed, it raises a TypeError.
    """
    if annotation is None:
        return None
    if isinstance(annotation, int):
        return "int"
    if isinstance(annotation, str):
        return "str"
    elif isinstance(annotation, ast.Constant):
        return "..." if annotation.value.__str__() == "Ellipsis" else parse_ast_constant(ast_constant=annotation)
    elif isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Subscript):
        return f"{annotation.value.id}[{_parse_type_from_annotation(annotation=annotation.slice)}]"
    elif isinstance(annotation, ast.Slice):
        return _parse_type_from_annotation(annotation=annotation.slice.value)
    elif isinstance(annotation, ast.Attribute):
        return f"{_parse_type_from_annotation(annotation=annotation.value)}.{annotation.attr}"
    elif isinstance(annotation, ast.Index):
        return ", ".join([_type.id for _type in annotation.value.elts])
    elif isinstance(annotation, ast.Tuple):
        return ", ".join([_parse_type_from_annotation(_type) for _type in annotation.dims])
    else:
        raise TypeError(f"Unable to parse `annotation` instance of type {type(annotation)}.")


def parse_ast_arguments(arguments: ast.arguments) -> List[Variable]:
    """
    Parse the AST arguments and return a list of Variable objects representing method arguments.

    :param arguments: The AST arguments to parse.
    :type arguments: ast.arguments

    :return: A list of Variable objects representing method arguments.
    :rtype: List[Variable]

    :raises TypeError: If the input is not an instance of ast.arguments.
    """
    _check_argument_type(expected=ast.arguments, got=arguments)

    default_value = [None] * (len(arguments.args) - len(arguments.defaults)) + arguments.defaults
    return [
        Variable(
            name=argument.arg,
            annotation=_parse_type_from_annotation(annotation=argument.annotation),
            value=default_value[idx].value if default_value[idx] else default_value[idx],
            variable_type="method argument",
        )
        for idx, argument in enumerate(arguments.args)
    ]


def parse_ast_ann_assign(
    annotate_assignment: ast.AnnAssign,
    variable_type: Literal["class variable", "instance variable", "global variable"],
) -> Variable:
    """
    Parse the AST annotated assignment and return a Variable object representing the assigned variable.

    :param annotate_assignment: The AST annotated assignment to parse.
    :type annotate_assignment: ast.AnnAssign
    :param variable_type: The type of variable (class variable, instance variable, or global variable).
    :type variable_type: Literal["class variable", "instance variable", "global variable"]

    :return: A Variable object representing the assigned variable.
    :rtype: Variable

    :raises TypeError: If the input is not an instance of ast.AnnAssign.
    """
    _check_argument_type(expected=ast.AnnAssign, got=annotate_assignment)

    return Variable(
        name=annotate_assignment.target.id,
        annotation=_parse_type_from_annotation(annotation=annotate_assignment.annotation),
        value=parse_value(value=annotate_assignment.value),
        variable_type=variable_type,
    )


def parse_ast_function_def(method: ast.FunctionDef) -> Method:
    """
    Parse the AST function definition and return a Method object representing the defined method.

    :param method: The AST function definition to parse.
    :type method: ast.FunctionDef

    :return: A Method object representing the defined method.
    :rtype: Method

    :raises TypeError: If the input is not an instance of ast.FunctionDef.
    """
    _check_argument_type(expected=ast.FunctionDef, got=method)

    return Method(
        name=method.name,
        arguments=parse_ast_arguments(arguments=method.args),
        decorators=[decorator.id for decorator in method.decorator_list],
    )


def parse_ast_class_def(branch: ast.ClassDef) -> Class:
    """
    Parse an AST class definition node and extract class information, including class name, base classes,
    class variables, instance variables, and methods, and returns a Class object.

    :param branch: The AST class definition node to parse.
    :type branch: ast.ClassDef

    :return: A Class object representing the class extracted from the AST node.
    :rtype: Class

    :raises TypeError: If the input is not an instance of ast.ClassDef.
    """
    _check_argument_type(expected=ast.ClassDef, got=branch)

    container_entry = defaultdict(list)
    for leaf in branch.body:
        if isinstance(leaf, ast.Assign):
            container_entry["class_variables"].extend(
                parse_ast_assign(
                    assignments=leaf,
                    variable_type="class variable",
                )
            )

        if isinstance(leaf, ast.AnnAssign):
            container_entry["class_variables"].append(
                parse_ast_ann_assign(annotate_assignment=leaf, variable_type="class variable")
            )

        if isinstance(leaf, ast.FunctionDef):
            container_entry["methods"].append(parse_ast_function_def(method=leaf))

    return Class(
        name=branch.name,
        bases=[base.id for base in branch.bases],
        class_variables=container_entry["class_variables"],
        instance_variables=container_entry["instance_variables"],
        methods=container_entry["methods"],
    )


def parse_ast_import_from(ast_import_from: ast.ImportFrom) -> List[Import]:
    """
    Parse an AST import from node and extract import information, including module names and optional aliases,
    and returns a list of Import objects.

    :param ast_import_from: The AST import from node to parse.
    :type ast_import_from: ast.ImportFrom

    :return: A list of Import objects representing the imports extracted from the AST node.
    :rtype: List[Import]

    :raises TypeError: If the input is not an instance of ast.ImportFrom.
    """
    _check_argument_type(expected=ast.ImportFrom, got=ast_import_from)

    components = [(component.name, component.asname) for component in ast_import_from.names]

    return [Import(module=ast_import_from.module, component=component, asname=alias) for component, alias in components]


def parse_ast_import(ast_import: ast.Import) -> List[Import]:
    """
    Parse an AST import node and extract import information, including module names and optional aliases,
    and returns a list of Import objects.

    :param ast_import: The AST import node to parse.
    :type ast_import: ast.Import

    :return: A list of Import objects representing the imports extracted from the AST node.
    :rtype: List[Import]

    :raises TypeError: If the input is not an instance of ast.Import.
    """
    _check_argument_type(expected=ast.Import, got=ast_import)

    imports = [(_import.name, _import.asname) for _import in ast_import.names]

    return [
        Import(
            module=module,
            asname=alias,
        )
        for module, alias in imports
    ]
