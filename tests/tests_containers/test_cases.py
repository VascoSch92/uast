from typing import List

from uast.core.containers.containers import (
    Class,
    Method,
    Script,
    Variable,
)

############
# VARIABLE #
############

variables = [
    Variable(name="variable_1"),
    Variable(name="variable_2", value=3),
    Variable(name="variable_3", annotation=int),
    Variable(name="variable_4", value="abc", annotation=str),
    Variable(name="variable_5", value=[1, 2, 3], annotation=List[str], variable_type="clas variable"),
]

VARIABLE_INSTANCES_TEST_CASES = {
    "input_value": variables,
    "expected_value": [
        {"name": "variable_1", "value": None, "variable_type": "", "annotation": None},
        {"name": "variable_2", "value": 3, "variable_type": "", "annotation": None},
        {"name": "variable_3", "value": None, "variable_type": "", "annotation": int},
        {"name": "variable_4", "value": "abc", "variable_type": "", "annotation": str},
        {"name": "variable_5", "value": [1, 2, 3], "variable_type": "clas variable", "annotation": List[str]},
    ]
}


##########
# METHOD #
##########

methods = [
    Method(name="method_1"),
    Method(name="method_2", arguments=[Variable(name="variable_1")]),
    Method(name="method_3", arguments=[Variable(name="variable_1"), Variable(name="variable_2")]),
]

METHOD_INSTANCES_TEST_CASES = {
    "input_value": methods,
    "expected_value": [
        {"name": "method_1", "arguments": [], "decorators": []},
        {"name": "method_2", "arguments": [Variable(name="variable_1")], "decorators": []},
        {"name": "method_3", "arguments": [Variable(name="variable_1"), Variable(name="variable_2"), ], "decorators": []},
    ]
}

METHOD_PROPERTIES_TEST_CASES = {
    "input_value": methods,
    "expected_value": [
        {"arguments_names": []},
        {"arguments_names": ["variable_1"]},
        {"arguments_names": ["variable_1", "variable_2"]},
    ]
}


#########
# CLASS #
#########

classes = [
    Class(name="class_1"),
    Class(name="class_2", bases=["basis"]),
    Class(name="class_3", class_variables=[Variable(name="variable_1")]),
    Class(name="class_4", instance_variables=[Variable(name="variable_1")]),
    Class(name="class_5", methods=[Method(name="method_1")]),
]

CLASS_INSTANCES_TEST_CASES = {
    "input_value": classes,
    "expected_value": [
        {"name": "class_1", "bases": [], "methods": [], "class_variables": [], "instance_variables":[]},
        {"name": "class_2", "bases": ["basis"], "methods": [], "class_variables": [], "instance_variables":[]},
        {"name": "class_3", "bases": [], "methods": [], "class_variables": [Variable(name="variable_1")], "instance_variables": []},
        {"name": "class_4", "bases": [], "methods": [], "class_variables": [], "instance_variables":[Variable(name="variable_1")]},
        {"name": "class_5", "bases": [], "methods": [Method(name="method_1")], "class_variables": [], "instance_variables": []},
    ]
}

CLASS_PROPERTIES_TEST_CASES = {
    "input_value": classes,
    "expected_value": [
        {"class_variables_names": [], "instance_variables_names": [], "methods_names": []},
        {"class_variables_names": [], "instance_variables_names": [], "methods_names": []},
        {"class_variables_names": ["variable_1"], "instance_variables_names": [], "methods_names": []},
        {"class_variables_names": [], "instance_variables_names": ["variable_1"], "methods_names": []},
        {"class_variables_names": [], "instance_variables_names": [], "methods_names": ["method_1"]},
    ]
}

##########
# SCRIPT #
##########

script = [
    Script(name="script_1"),
    Script(name="script_2", imports=["import_1"]),
    Script(name="script_3", global_variables=[Variable(name="variable_1")]),
    Script(name="script_4", classes=[Class(name="class_1")]),
    Script(name="script_5", methods=[Method(name="method_1")]),
]

SCRIPT_INSTANCES_TEST_CASES = {
    "input_value": script,
    "expected_value": [
        {"name": "script_1", "imports": [], "global_variables": [], "classes": [], "methods":[]},
        {"name": "script_2", "imports": ["import_1"], "global_variables": [], "classes": [], "methods":[]},
        {"name": "script_3", "imports": [], "global_variables": [Variable(name="variable_1")], "classes": [], "methods":[]},
        {"name": "script_4", "imports": [], "global_variables": [], "classes": [Class(name="class_1")], "methods":[]},
        {"name": "script_5", "imports": [], "global_variables": [], "classes": [], "methods":[Method(name="method_1")]},
    ]
}

SCRIPT_PROPERTY_TEST_CASES = {
    "input_value": script,
    "expected_value": [
        {"global_variables_names": [], "classes_names": [], "methods_names": []},
        {"global_variables_names": [], "classes_names": [], "methods_names": []},
        {"global_variables_names": ["variable_1"], "classes_names": [], "methods_names": []},
        {"global_variables_names": [], "classes_names": ["class_1"], "methods_names": []},
        {"global_variables_names": [], "classes_names": [], "methods_names": ["method_1"]},
    ]
}

##########
# COMMON #
##########

DICT_TEST_CASES = {
    "input_value": [
        Variable(name="variable", value=[1, 2, 3], annotation=List[str], variable_type="class_variable"),
        Method(name="method", arguments=[Variable(name="variable_1"), Variable(name="variable_2")]),
        Class(name="class", methods=[Method(name="method")]),
        Script(name="script", global_variables=[Variable(name="variable")], classes=[Class(name="class")], methods=[Method(name="method")]),
    ],
    "expected_value": [
        {"name": "variable", "value": [1, 2, 3], "annotation": List[str], "variable_type": "class_variable"},
        {"name": "method", "arguments": [{"name": "variable_1", "value": None, "variable_type": "", "annotation": None}, {"name": "variable_2", "value": None, "variable_type": "", "annotation": None}], "decorators": []},
        {"name": "class", "bases": [], "methods": [{"name": "method", "arguments": [], "decorators": []}], "instance_variables": [], "class_variables": []},
        {"name": "script", "imports": [], "classes": [{"name": "class", "bases": [], "methods": [], "class_variables": [], "instance_variables": []}], "methods": [{"name": "method", "arguments": [], "decorators": []}], "global_variables": [{"name": "variable", "value": None, "variable_type": "", "annotation": None}]},
    ],
}

SCHEMA_TEST_CASES = {
    "input_value": [
        Variable(name="d", value=None, variable_type="method argument", annotation="Union[str, int]"),
        Method(
            name="base",
            arguments=[
                Variable(name="self", value=None, variable_type="method argument", annotation=None),
                Variable(name="d", value=None, variable_type="method argument", annotation="Union[str, int]"),
                Variable(name="c", value=None, variable_type="method argument", annotation="np.ndarray"),
            ],
            decorators=["abstractmethod"]
        )
    ],
    "expected_value": [
        "d: method argument (annotation: Union[str, int])",
        "base: method (decorators: abstractmethod)\n"
        " |-- self: method argument \n"
        " |-- d: method argument (annotation: Union[str, int])\n"
        " |-- c: method argument (annotation: np.ndarray)",
    ]

}
