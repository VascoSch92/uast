from typing import List

from tests.utils import error_message


def _check_instance(sample: List, instance_names: List[str]) -> None:
    error_message_stack = ""
    for instance_name in instance_names:
        if getattr(sample[0], instance_name) != sample[1][instance_name]:
            error_message_stack += error_message(
                expected=vars(sample[0])[instance_name],
                got=sample[1][instance_name],
            )
            error_message_stack += "\n"

    if error_message_stack:
        raise Exception(error_message_stack)


############
# VARIABLE #
############

def test_instance_variable_containers(variable_sample):
    _check_instance(sample=variable_sample, instance_names=["name", "value", "annotation", "variable_type"])


##########
# METHOD #
##########

def test_instance_method_containers(method_sample):
    _check_instance(sample=method_sample, instance_names=["name", "arguments", "decorators"])


def test_method_properties(method_property_sample):
    _check_instance(sample=method_property_sample, instance_names=["arguments_names"])


#########
# CLASS #
#########

def test_instance_class_containers(class_sample):
    _check_instance(
        sample=class_sample,
        instance_names=["name", "bases", "methods", "instance_variables", "class_variables"],
    )


def test_class_properties(class_property_sample):
    _check_instance(
        sample=class_property_sample,
        instance_names=["class_variables_names", "instance_variables_names", "methods_names"]
    )


##########
# SCRIPT #
##########

def test_instance_script_containers(script_sample):
    _check_instance(
        sample=script_sample,
        instance_names=["name", "imports", "methods", "global_variables", "classes"]
    )


def test_script_properties(script_property_sample):
    _check_instance(
        sample=script_property_sample,
        instance_names=["global_variables_names", "classes_names", "methods_names"],
    )


##########
# COMMON #
##########

def test_dict_representation(dict_sample):
    input_dict_repr = dict_sample[0].__dict__()
    expected_dict_repr = dict_sample[1]

    # checks that the two dicts have same set of keys
    if input_dict_repr.keys() != expected_dict_repr.keys():
        raise KeyError(
            error_message(expected=input_dict_repr.keys(), got=expected_dict_repr.keys())
        )

    # checks that the two dicts have same values
    for key in input_dict_repr.keys():
        if input_dict_repr[key] != expected_dict_repr[key]:
            raise ValueError(
                error_message(expected=expected_dict_repr[key], got=input_dict_repr[key])
            )


def test_schema(schema_sample):
    assert schema_sample[0].schema() == schema_sample[1], error_message(expected=schema_sample[1], got=schema_sample[0].schema())

