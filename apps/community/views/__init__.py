# 文件说明：声明 Python 包，便于模块被项目导入。

from .building_view import BuildingCreateView, BuildingListView
from .community_view import CommunityCreateView, CommunityListView
from .house_view import HouseCreateView, HouseDeleteView, HouseListView, HouseUpdateView
from .unit_view import UnitCreateView, UnitListView

__all__ = [
    "BuildingCreateView",
    "BuildingListView",
    "CommunityCreateView",
    "CommunityListView",
    "HouseCreateView",
    "HouseDeleteView",
    "HouseListView",
    "HouseUpdateView",
    "UnitCreateView",
    "UnitListView",
]
