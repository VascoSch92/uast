import ast

import pytest

from tests.utils import error_message
from uast.core.ast_parsers import (
    parse_func,
    parse_value,
    parse_ast_call,
    parse_ast_dict,
    parse_ast_list,
    parse_ast_assign,
    parse_ast_import,
    parse_ast_constant,
    parse_ast_arguments,
    parse_ast_class_def,
    _check_argument_type,
    parse_ast_ann_assign,
    parse_ast_import_from,
    parse_ast_function_def,
    _parse_type_from_annotation,
)


def test_parse_value(value_sample) -> None:
    if parse_value(value=value_sample[0]) != value_sample[1]:
        raise ValueError(
            error_message(
                expected=value_sample[1],
                got=parse_value(value=value_sample[0]),
            )
        )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (ast.Constant(value=None), "None"),
        (ast.Constant(value=42), "42"),
        (ast.Constant(value="hello"), "'hello'"),
    ]
)
def test_parse_ast_constant(input_value, expected_value) -> None:
    if parse_ast_constant(ast_constant=input_value) != expected_value:
        raise ValueError(
            error_message(
                expected=expected_value,
                got=parse_ast_constant(ast_constant=input_value),
            )
        )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (ast.List(elts=[]), "[]"),
        (ast.List(elts=[ast.Constant(value=1), ast.Constant(value=2)]), "[1, 2]"),
        (ast.List(elts=[ast.Constant(value="hello"), ast.Constant(value="world")]), "['hello', 'world']"),
    ]
)
def test_parse_ast_list(input_value, expected_value) -> None:
    if parse_ast_list(ast_list=input_value) != expected_value:
        raise ValueError(
            error_message(
                expected=expected_value,
                got=parse_ast_list(ast_list=input_value),
            )
        )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (ast.Dict(keys=[], values=[]), "{}"),
        (
                ast.Dict(
                    keys=[ast.Constant(value="a"), ast.Constant(value="b")],
                    values=[ast.Constant(value=1), ast.Constant(value=2)]
                ),
                "{'a': 1, 'b': 2}"
        ),
    ]
)
def test_parse_ast_dict(input_value, expected_value) -> None:
    if parse_ast_dict(ast_dict=input_value) != expected_value:
        raise ValueError(
            error_message(
                expected=expected_value,
                got=parse_ast_dict(ast_dict=input_value),
            )
        )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (
                ast.Call(
                    func=ast.Name(id="my_function", ctx=ast.Load()),
                    args=[ast.Num(n=0)],
                    keywords=[],
                    starargs=None,
                    kwargs=None
                ),
                "my_function(0)"),
    ]
)
def test_parse_ast_call(input_value, expected_value) -> None:
    if parse_ast_call(ast_call=input_value) != expected_value:
        raise ValueError(
            error_message(
                expected=expected_value,
                got=parse_ast_call(ast_call=input_value),
            )
        )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (ast.Attribute(value=ast.Name(id="module", ctx=ast.Load()), attr="method", ctx=ast.Load()), "module.method"),
        (ast.Name(id="function", ctx=ast.Load()), "function"),
    ]
)
def test_parse_func(input_value, expected_value) -> None:
    if parse_func(func=input_value) != expected_value:
        raise ValueError(
            error_message(
                expected=expected_value,
                got=parse_func(func=input_value),
            )
        )


def test_parse_type_from_annotation(annotation_sample) -> None:
    if _parse_type_from_annotation(annotation=annotation_sample[0]) != annotation_sample[1]:
        raise ValueError(
            error_message(
                expected=annotation_sample[1],
                got=_parse_type_from_annotation(annotation=annotation_sample[0]),
            )
        )


def test_parse_ast_ann_assign(annotate_assignment_sample) -> None:
    variable_container = parse_ast_ann_assign(
        annotate_assignment=annotate_assignment_sample[0],
        variable_type="global variable"
    )
    if variable_container != annotate_assignment_sample[1]:
        raise ValueError(
            error_message(
                expected=annotate_assignment_sample[1],
                got=variable_container,
            )
        )


def test_parse_ast_assign(assignment_sample) -> None:
    variable_containers = parse_ast_assign(
        assignments=assignment_sample[0],
        variable_type="global variable"
    )
    for variable_container, expected_output in zip(variable_containers, assignment_sample[1]):
        if variable_container != expected_output:
            raise ValueError(
                error_message(expected=expected_output, got=variable_container)
            )


def test_parse_ast_function_def(method_sample) -> None:
    method_container = parse_ast_function_def(method=method_sample[0])
    if method_container != method_sample[1]:
        raise ValueError(
            error_message(expected=method_container, got=method_sample[1])
        )


def test_parse_ast_arguments(argument_sample) -> None:
    argument_containers = parse_ast_arguments(arguments=argument_sample[0])
    for argument_container, expected_output in zip(argument_containers, argument_sample[1]):
        if argument_container != expected_output:
            raise ValueError(
                error_message(expected=argument_container, got=expected_output[1])
            )


def test_parse_ast_class_def(class_sample) -> None:
    class_container = parse_ast_class_def(branch=class_sample[0])
    if class_container != class_sample[1]:
        raise ValueError(
            error_message(expected=class_container, got=class_sample[1])
        )


def test_parse_ast_import_from(import_from_sample) -> None:
    import_containers = parse_ast_import_from(ast_import_from=import_from_sample[0])

    for import_container, expected_output in zip(import_containers, import_from_sample[1]):
        if import_container != expected_output:
            raise ValueError(
                error_message(expected=import_container, got=expected_output)
            )


def test_parse_ast_import(import_sample) -> None:
    import_containers = parse_ast_import(ast_import=import_sample[0])

    for import_container, expected_output in zip(import_containers, import_sample[1]):
        if import_container != expected_output:
            raise ValueError(
                error_message(expected=import_container, got=expected_output)
            )


@pytest.mark.parametrize(
    "expected, got",
    [
        (ast.ClassDef, ast.Constant(value=0)),
        (ast.List, ast.Constant(value=0)),
    ]
)
def test_check_argument_type(expected, got) -> None:
    with pytest.raises(
            expected_exception=TypeError,
            match=f"Input must be an instance of {expected}. Got {type(got)}."
    ):
        _check_argument_type(expected=expected, got=got)
