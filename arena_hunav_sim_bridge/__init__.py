import os
from abc import ABC

import attrs

from ament_index_python import get_package_share_directory


@attrs.define
class BaseNode(ABC): ...

BT_REF_DOC_PATH = os.path.join(
    get_package_share_directory("arena_hunav_sim_bridge"),
    "HuNavSim_BT_Reference_Structured.json"
)
CHROMA_DB_PATH = os.path.join(
    get_package_share_directory("arena_hunav_sim_bridge"),
    "chroma"
)

__all__ = [
    "BaseNode",
    "BT_REF_DOC_PATH",
    "CHROMA_DB_PATH",
]