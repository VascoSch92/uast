from uast.core.containers.containers import (
    Class,
    Import,
    Method,
    Variable,
)

assignment = """
int_1 = 0

str_1 = 's'

list_1 = []
list_2 = [1, 2, 3]
list_3 = ['f', 'o', 'o'],
list_4 = list("foo")

dict_1 = {'hello': 'world'}

tuple_1 = tuple((1, 2, 3))
tuple_2 = (1, 2, 3)

numpy_array_1 = np.zeros(3, 2)

path_1 = Path("path/to/file")
path_2 = Path().cwd()
"""
annotate_assignment = """
none_annotation: None = None

int_annotation_1: int = 0

str_annotation_1: str = 's'

list_annotation_1: list = []
list_annotation_2: List = []
list_annotation_3: List[int] = [1, 2, 3]
list_annotation_4: List[int, ...] = [1, 2, 3]

dict_annotation_1: dict = {}
dict_annotation_2: Dict = {}
dict_annotation_3: Dict[str] = {'hello': 'world'}
dict_annotation_4: Dict[str, str] = {'hello': 'world'}

path_annotation: Path = Path('path/to/somewhere')

numpy_annotation: np.ndarray = np.zeros(3,2)

class_annotation_1: NameOfAClass = name_of_a_class()
class_annotation_2: Type[NameOfAClass] = name_of_a_class()

optional_1: Optional[str] = None
optional_1: Union[None, str] = None

literal_1: Literal['hello', 'world'] = 'hello'
"""
method = """
def nothing():
    return
def one_variable(a)->int:
    return a
def one_variable_and_type(a:int)->str:
    return str(a)
@staticmethod
@helloworld
def decorators():
    return
"""
_class = """
class Foo(Base):
    CONST_1 = 0
    CONST_2: str = 'A'

    def __init__(self, a: int, b: str):
        self.a = a
        self.b = b

    def base(self, d,  c: float = 0.99) -> int:
        return self.a + 0
"""
import_from = """
from module_example import import_example
from import_module_1.import_module_2 import import_1
from import_module_1.import_module_2.import_module_3 import (
    import_1,
    import_2,
    import_3,
)
from imports import import_1, import_2
from import_example import component_example as component_alias
"""
_import = """
import module
import module_1.module_2
import module_1 as alias_1
"""

VALUE_TEST_CASES = {
    "input_values": assignment,
    "expected_values": [
        "0",
        "'s'",
        "[]",
        "[1, 2, 3]",
        "['f', 'o', 'o']",
        "list('foo')",
        "{'hello': 'world'}",
        "tuple((1, 2, 3))",
        "1, 2, 3",
        "np.zeros(3, 2)",
        "Path('path/to/file')",
        "Path().cwd()",
    ],
}
ANNOTATION_TEST_CASES = {
    "input_values": annotate_assignment,
    "expected_values": [
        "None",
        "int",
        "str",
        "list",
        "List",
        "List[int]",
        "List[int, ...]",
        "dict",
        "Dict",
        "Dict[str]",
        "Dict[str, str]",
        "Path",
        "np.ndarray",
        "NameOfAClass",
        "Type[NameOfAClass]",
        "Optional[str]",
        "Union[None, str]",
        "Literal['hello', 'world']",
    ],
}
ANNOTATE_ASSIGNMENT_TEST_CASES = {
    "input_values": annotate_assignment,
    "expected_values": [
        Variable(name="none_annotation", value="None", variable_type="global variable", annotation="None"),
        Variable(name="int_annotation_1", value="0", variable_type="global variable", annotation="int"),
        Variable(name="str_annotation_1", value="'s'", variable_type="global variable", annotation="str"),
        Variable(name="list_annotation_1", value="[]", variable_type="global variable", annotation="list"),
        Variable(name="list_annotation_2", value="[]", variable_type="global variable", annotation="List"),
        Variable(name="list_annotation_3", value="[1, 2, 3]", variable_type="global variable", annotation="List[int]"),
        Variable(
            name="list_annotation_4", value="[1, 2, 3]", variable_type="global variable", annotation="List[int, ...]"
        ),
        Variable(name="dict_annotation_1", value="{}", variable_type="global variable", annotation="dict"),
        Variable(name="dict_annotation_2", value="{}", variable_type="global variable", annotation="Dict"),
        Variable(
            name="dict_annotation_3",
            value="{'hello': 'world'}",
            variable_type="global variable",
            annotation="Dict[str]",
        ),
        Variable(
            name="dict_annotation_4",
            value="{'hello': 'world'}",
            variable_type="global variable",
            annotation="Dict[str, str]",
        ),
        Variable(
            name="path_annotation",
            value="Path('path/to/somewhere')",
            variable_type="global variable",
            annotation="Path",
        ),
        Variable(
            name="numpy_annotation",
            value="np.zeros(3, 2)",
            variable_type="global variable",
            annotation="np.ndarray",
        ),
        Variable(
            name="class_annotation_1",
            value="name_of_a_class()",
            variable_type="global variable",
            annotation="NameOfAClass",
        ),
        Variable(
            name="class_annotation_2",
            value="name_of_a_class()",
            variable_type="global variable",
            annotation="Type[NameOfAClass]",
        ),
        Variable(name="optional_1", value="None", variable_type="global variable", annotation="Optional[str]"),
        Variable(name="optional_1", value="None", variable_type="global variable", annotation="Union[None, str]"),
        Variable(
            name="literal_1", value="'hello'", variable_type="global variable", annotation="Literal['hello', 'world']"
        ),
    ],
}
ASSIGNMENT_TEST_CASES = {
    "input_values": assignment,
    "expected_values": [
        [Variable(name="int_1", value="0", variable_type="global variable", annotation=None)],
        [Variable(name="str_1", value="'s'", variable_type="global variable", annotation=None)],
        [Variable(name="list_1", value="[]", variable_type="global variable", annotation=None)],
        [Variable(name="list_2", value="[1, 2, 3]", variable_type="global variable", annotation=None)],
        [Variable(name="list_3", value="['f', 'o', 'o']", variable_type="global variable", annotation=None)],
        [Variable(name="list_4", value="list('foo')", variable_type="global variable", annotation=None)],
        [Variable(name="dict_1", value="{'hello': 'world'}", variable_type="global variable", annotation=None)],
        [Variable(name="tuple_1", value="tuple((1, 2, 3))", variable_type="global variable", annotation=None)],
        [Variable(name="tuple_2", value="1, 2, 3", variable_type="global variable", annotation=None)],
        [Variable(name="numpy_array_1", value="np.zeros(3, 2)", variable_type="global variable", annotation=None)],
        [Variable(name="path_1", value="Path('path/to/file')", variable_type="global variable", annotation=None)],
        [Variable(name="path_2", value="Path().cwd()", variable_type="global variable", annotation=None)],
    ],
}
METHOD_TEST_CASES = {
    "input_values": method,
    "expected_values": [
        Method(name="nothing", arguments=[], decorators=[]),
        Method(
            name="one_variable",
            arguments=[Variable(name="a", value=None, variable_type="method argument", annotation=None)],
            decorators=[],
        ),
        Method(
            name="one_variable_and_type",
            arguments=[Variable(name="a", value=None, variable_type="method argument", annotation="int")],
            decorators=[],
        ),
        Method(name="decorators", arguments=[], decorators=["staticmethod", "helloworld"]),
    ],
}
ARGUMENT_TEST_CASES = {
    "input_values": method,
    "expected_values": [
        [Variable(name="a", annotation=None, value=None, variable_type="method argument")],
        [Variable(name="a", value=None, variable_type="method argument", annotation=None)],
        [Variable(name="a", value=None, variable_type="method argument", annotation="int")],
        [None],
    ],
}
CLASS_TEST_CASES = {
    "input_values": _class,
    "expected_values": [
        Class(
            name="Foo",
            bases=["Base"],
            class_variables=[
                Variable(name="CONST_1", value="0", variable_type="class variable", annotation=None),
                Variable(name="CONST_2", value="'A'", variable_type="class variable", annotation="str"),
            ],
            methods=[
                Method(
                    name="__init__",
                    arguments=[
                        Variable(name="self", value=None, variable_type="method argument", annotation=None),
                        Variable(name="a", value=None, variable_type="method argument", annotation="int"),
                        Variable(name="b", value=None, variable_type="method argument", annotation="str"),
                    ],
                ),
                Method(
                    name="base",
                    arguments=[
                        Variable(name="self", value=None, variable_type="method argument", annotation=None),
                        Variable(name="d", value=None, variable_type="method argument", annotation=None),
                        Variable(name="c", value=0.99, variable_type="method argument", annotation="float"),
                    ],
                ),
            ],
        )
    ],
}
IMPORT_FROM_TEST_CASES = {
    "input_values": import_from,
    "expected_values": [
        [Import(module="module_example", component="import_example")],
        [Import(module="import_module_1.import_module_2", component="import_1")],
        [
            Import(module="import_module_1.import_module_2.import_module_3", component="import_1"),
            Import(module="import_module_1.import_module_2.import_module_3", component="import_2"),
            Import(module="import_module_1.import_module_2.import_module_3", component="import_3"),
        ],
        [
            Import(module="imports", component="import_1"),
            Import(module="imports", component="import_2"),
        ],
        [Import(module="import_example", component="component_example", asname="component_alias")],
    ],
}
IMPORT_TEST_CASES = {
    "input_values": _import,
    "expected_values": [
        [Import(module="module")],
        [Import(module="module_1.module_2")],
        [Import(module="module_1", asname="alias_1")],
    ],
}
