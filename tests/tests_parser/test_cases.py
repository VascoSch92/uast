from pathlib import Path

from uast.core.containers.containers import (
    Class,
    Import,
    Method,
    Script,
    Variable,
)

assignment = """
a = 9
"""
annotate_assignment = """
a: int = 9
"""
function_def = """
def function():
    return None
"""
double_function_def = """
def function_1():
    return None
def function_2():
    return None
"""
class_def = """
class Foo(ABC):
    a = 9
    a: int = 9

    def function():
        return None
"""

assignment_container = [Variable(name="a", value="9", variable_type="global variable")]
annotate_assignment_container = [Variable(name="a", value="9", annotation="int", variable_type="global variable")]
function_def_container = [Method(name="function")]
double_function_def_container = [Method(name="function_1"), Method(name="function_2")]
class_def_container = [
    Class(
        name="Foo",
        bases=["ABC"],
        class_variables=[
            Variable(name="a", value="9", variable_type="class variable"),
            Variable(name="a", value="9", annotation="int", variable_type="class variable"),
        ],
        methods=[Method(name="function")],
    )
]

script_test_case = Script(
    name="script_test_case.py",
    imports=[
        Import(module="abc", component="ABC", asname=None),
        Import(module="abc", component="abstractmethod", asname=None),
        Import(module="typing", component="Union", asname=None),
        Import(module="pathlib", component="Path", asname=None),
        Import(module="numpy", component=None, asname="np"),
    ],
    global_variables=[
        Variable(name="CONST", value="Path().cwd()", variable_type="global variable", annotation=None),
        Variable(name="GLOBAL", value="GLOBAL", variable_type="global variable", annotation=None),
        Variable(name="ANOTHER_GLOBAL", value="ANOTHER_GLOBAL", variable_type="global variable", annotation=None),
    ],
    classes=[
        Class(
            name="Base",
            bases=["ABC"],
            methods=[
                Method(
                    name="base",
                    arguments=[
                        Variable(name="self", value=None, variable_type="method argument", annotation=None),
                        Variable(name="d", value=None, variable_type="method argument", annotation="Union[str, int]"),
                        Variable(name="c", value=None, variable_type="method argument", annotation="np.ndarray"),
                    ],
                    decorators=["abstractmethod"],
                )
            ],
            class_variables=[],
            instance_variables=[],
        ),
        Class(
            name="Foo",
            bases=["Base"],
            methods=[
                Method(
                    name="__init__",
                    arguments=[
                        Variable(name="self", value=None, variable_type="method argument", annotation=None),
                        Variable(name="a", value=None, variable_type="method argument", annotation="int"),
                        Variable(name="b", value=None, variable_type="method argument", annotation="str"),
                    ],
                    decorators=[],
                ),
                Method(
                    name="base",
                    arguments=[
                        Variable(name="self", value=None, variable_type="method argument", annotation=None),
                        Variable(name="d", value=None, variable_type="method argument", annotation=None),
                        Variable(name="c", value=0.99, variable_type="method argument", annotation="float"),
                    ],
                    decorators=[],
                ),
            ],
            class_variables=[
                Variable(name="CONST_1", value="0", variable_type="class variable", annotation=None),
                Variable(name="CONST_2", value="'A'", variable_type="class variable", annotation="str"),
            ],
            instance_variables=[],
        ),
        Class(
            name="Bar",
            bases=[],
            methods=[Method(name="bar", arguments=[], decorators=["staticmethod"])],
            class_variables=[],
            instance_variables=[],
        ),
    ],
    methods=[],
)


TREE_TEST_CASES = {
    "input_value": [
        assignment,
        annotate_assignment,
        function_def,
        double_function_def,
        class_def,
    ],
    "expected_value": [
        assignment_container,
        annotate_assignment_container,
        function_def_container,
        double_function_def_container,
        class_def_container,
    ],
}
PARSE_TEST_CASE = {
    "input_value": [
        assignment,
        annotate_assignment,
        function_def,
        double_function_def,
        class_def,
        "tests/tests_parser/script_test_case.py",
        Path("tests/tests_parser/script_test_case.py"),
    ],
    "expected_value": [
        assignment_container,
        annotate_assignment_container,
        function_def_container,
        double_function_def_container,
        class_def_container,
        script_test_case,
        script_test_case,
    ],
}
