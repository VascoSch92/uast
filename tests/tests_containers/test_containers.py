from typing import List

from tests.utils import (
    error_message,
    lists_are_equal,
)



def _check_instance(sample: List, instance_names: List[str]) -> None:
    error_message_stack = ""
    for instance_name in instance_names:
        if getattr(sample[0], instance_name) != sample[1][instance_name]:
            error_message_stack += error_message(
                expected=sample[1][instance_name],
                got=getattr(sample[0], instance_name),
            )
            error_message_stack += "\n"

    if error_message_stack:
        raise Exception(error_message_stack)


############
# VARIABLE #
############


def test_instance_variable_containers(variable_sample) -> None:
    _check_instance(sample=variable_sample, instance_names=["name", "value", "annotation", "variable_type"])


##########
# METHOD #
##########


def test_instance_method_containers(method_sample) -> None:
    _check_instance(sample=method_sample, instance_names=["name", "arguments", "decorators"])

#########
# CLASS #
#########


def test_instance_class_containers(class_sample) -> None:
    _check_instance(
        sample=class_sample,
        instance_names=["name", "bases", "methods", "instance_variables", "class_variables"],
    )


##########
# SCRIPT #
##########


def test_instance_script_container(script_sample) -> None:
    input_script = script_sample[0]
    expected_script = script_sample[1]

    if input_script.name != expected_script["name"]:
        error_message(expected=expected_script.name, got=input_script.name)

    if lists_are_equal(a=input_script.content, b=expected_script["content"]) is False:
        error_message(expected=input_script.content, got=expected_script.content)


##########
# COMMON #
##########


def test_dict_representation(dict_sample) -> None:
    input_dict_repr = dict_sample[0].as_dict()
    expected_dict_repr = dict_sample[1]

    # checks that the two dicts have same set of keys
    if input_dict_repr.keys() != expected_dict_repr.keys():
        raise KeyError(error_message(expected=input_dict_repr.keys(), got=expected_dict_repr.keys()))

    # checks that the two dicts have same values
    for key in input_dict_repr.keys():
        if input_dict_repr[key] != expected_dict_repr[key]:
            raise ValueError(error_message(expected=expected_dict_repr[key], got=input_dict_repr[key]))


def test_schema(schema_sample) -> None:
    if schema_sample[0].schema() != schema_sample[1]:
        raise ValueError(error_message(expected=schema_sample[1], got=schema_sample[0].schema()))
