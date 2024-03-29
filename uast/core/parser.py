import ast
from pathlib import Path
from typing import List, Union

from uast.core.ast_parsers import (
    parse_ast_assign,
    parse_ast_import,
    parse_ast_class_def,
    parse_ast_ann_assign,
    parse_ast_import_from,
    parse_ast_function_def,
)
from uast.core.containers.containers import (
    Script,
)

__all__ = [
    "parse",
]


def _parse_python_script(source: Path) -> Script:
    """
    The method reads the contents of the Python script file specified by the `source` path,
    parses it, and extracts script information including imports,
    global variables, methods, and classes. The extracted information is encapsulated into a Script object,
    which is returned.

    :param source: The path to the Python script file.
    :type source: Path

    :return: A Script object representing the script extracted from the file.
    :rtype: Script
    """
    target = source.read_text()
    module = ast.parse(target)

    return Script(
        name=source.name,
        content=_parse_module(module=module),
    )


def _parse_tree(source: str) -> List:
    """
    The method takes either the source code or an already parsed AST and extracts a list of container from it.

    :param source: The source code or AST to parse.
    :type source: Any

    :return: A list of parsed entries extracted from the AST.
    :rtype: List
    """
    module = ast.parse(source=source)
    return _parse_module(module=module)


def _parse_module(module: ast.Module) -> List:
    """
    The method takes an AST module and extracts various types of entries from it,
    including imports, global variables, methods, and classes.

    :param module: The AST module to parse.
    :type module: ast.Module

    :return: A list containing parsed entries extracted from the AST.
    :rtype: List
    """
    content = []
    for branch in module.body:
        if isinstance(branch, ast.Import):
            content.extend(parse_ast_import(ast_import=branch))
        elif isinstance(branch, ast.ImportFrom):
            content.extend(parse_ast_import_from(ast_import_from=branch))
        elif isinstance(branch, ast.Assign):
            content.extend(
                parse_ast_assign(
                    assignments=branch,
                    variable_type="global variable",
                )
            )
        elif isinstance(branch, ast.AnnAssign):
            content.append(
                parse_ast_ann_assign(
                    annotate_assignment=branch,
                    variable_type="global variable",
                )
            )
        elif isinstance(branch, ast.FunctionDef):
            content.append(parse_ast_function_def(method=branch))
        elif isinstance(branch, ast.ClassDef):
            content.append(parse_ast_class_def(branch=branch))
    return content


def parse(source: Union[str, Path]) -> Union[List[Script], Script]:
    """
    The method parses the specified source, which can be either a file or a directory, and extracts script information.
     - If the source is a file, it is expected to be a Python script file (.py), and the script information is
        extracted using the `_parse_python_script` function.
     - If the source is a directory, a schema for parsing directories and projects is not yet implemented, so a
        NotImplementedError is raised.
     - If the source does not exist or cannot be parsed, appropriate exceptions are raised.

    :param source: The source file or directory to parse.
    :type source: Union[str, Path]

    :return: Either a list of Script objects (if source is a directory) or a single Script object (if source is a file).
    :rtype: Union[List[Script], Script]

    :raises ValueError: If the source is not a string or a Path object.
    :raises ValueError: If the source file has an unsupported file extension.
    :raises NotImplementedError: If the source is a directory or a project (schema not yet implemented).
    :raises Exception: If the source file cannot be parsed.
    """
    if isinstance(source, (str, Path)) is False:
        raise ValueError("Source can not be parsed.")

    if Path(source).exists():
        source = Path(source).absolute()
        if source.is_dir():
            raise NotImplementedError("Schema for directory and project not yer implemented.")
        elif source.is_file():
            if source.suffix != ".py":
                raise ValueError(f"Expecting a Python file. Got a {source.suffix}-file.")
            return _parse_python_script(source=Path(source))
        else:
            raise Exception("File can not be parsed.")
    else:
        return _parse_tree(source=source)
