import ast
import itertools
from typing import Dict, List, Union
from pathlib import Path
from collections import defaultdict

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

    target = source.read_text()
    module = ast.parse(target)

    script_entries = _parse_module(module=module)

    return Script(
        name=source.name,
        imports=script_entries["imports"],
        global_variables=script_entries["global_variables"],
        methods=script_entries["methods"],
        classes=script_entries["classes"],
    )


def _parse_tree(source) -> List:
    module = ast.parse(source=source)
    container_entry = _parse_module(module=module)
    return list(itertools.chain(*[container_entry[key] for key in container_entry.keys()]))


def _parse_module(module: ast.Module) -> Dict:
    container_entry = defaultdict(list)
    for branch in module.body:

        if isinstance(branch, ast.Import):
            container_entry["imports"].extend(
                parse_ast_import(
                    ast_import=branch
                )
            )

        if isinstance(branch, ast.ImportFrom):
            container_entry["imports"].extend(
                parse_ast_import_from(
                    ast_import_from=branch
                )
            )

        if isinstance(branch, ast.Assign):
            container_entry["global_variables"].extend(
                parse_ast_assign(
                    assignments=branch,
                    variable_type="global variable",
                )
            )

        if isinstance(branch, ast.AnnAssign):
            container_entry["global_variables"].append(
                parse_ast_ann_assign(
                    annotate_assignment=branch,
                    variable_type="global variable",
                )
            )

        if isinstance(branch, ast.FunctionDef):
            container_entry["methods"].append(
                parse_ast_function_def(method=branch)
            )

        if isinstance(branch, ast.ClassDef):
            container_entry["classes"].append(
                parse_ast_class_def(branch=branch)
            )

    return container_entry


def parse(source: Union[str, Path]) -> Union[List[Script], Script]:
    if isinstance(source, (str, Path)) is False:
        raise ValueError("Source can not be parsed.")

    if Path(source).exists():
        source = Path(source).absolute()
        if source.is_dir():
            raise NotImplementedError(
                "Schema for directory and project not yer implemented."
            )
        elif source.is_file():
            if source.suffix != ".py":
                raise ValueError(f"Expecting a Python file. Got a {source.suffix}-file.")
            return _parse_python_script(source=Path(source))
        else:
            raise Exception("File can not be parsed.")
    else:
        return _parse_tree(source=source)
