from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import overload, Union

from multibase_dataclass import Multibase 


ROOT = Path("./tmp")


@dataclass(frozen=True)
class File:
    name: str
    content: Multibase


def write_file(parent_folder: Path, file: File):
    # TODO: use atomic writes with a tempfile
    with open(file.name, "wb") as file_handler:
        file_handler.write(file.content.decode())


def safe_mkdir(dir_path: Union[str, Path]):
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True, exist_ok=True)


@overload
def get(key: Path) -> Multibase: ...

@overload
def get(key: Mapping) -> dict: ...

def get(key: Path) -> Multibase:
    if isinstance(key, Mapping):
        # TODO: get with deeply nested json should return a new json
        pass
    if isinstance(key, Path):
        full_path = key
        if full_path.is_file():
            with open(full_path, "rb") as file_handler:
                file_content = file_handler.read()
            encoded = Multibase.encode("base64", file_content)
            return encoded
        raise ValueError(f"Key {full_path} could not be found.")


def put(obj, prefix: Path = ROOT):
    if isinstance(obj, Mapping):
        for key, val in obj.items():
            safe_mkdir(prefix / key)
            put(val, prefix / key)
    if isinstance(obj, Sequence):
        for inner_obj in obj:
            put(inner_obj, prefix)
    if isinstance(obj, File):
        write_file(prefix, obj)


