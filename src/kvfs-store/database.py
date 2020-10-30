from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Union

from multibase_dataclass import Multibase 


ROOT = Path("./tmp")


class File:
    name: str
    content: Multibase


def write_file(parent_folder: Path, file: File):
    # TODO: use atomic writes with a tempfile
    with open(file.name, "wb") as file_handler:
        file_handler.write(file.content.decode())


def safe_mkdir(dir_path: Union[str, Path]):
    # make sure it's a Path instance
    # check if exists
    # create it if it doesn't
    pass


def get(full_path: Path) -> Multibase:
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


