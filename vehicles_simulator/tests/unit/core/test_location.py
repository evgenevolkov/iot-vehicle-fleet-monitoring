from app.core.location import NavigationMap
from app.utils.schemas import MapSize


def test_instantiate_navigation_map():
    map_size = MapSize(
        x_size=1,
        y_size=1
    )
    nav_map = NavigationMap(
        map_size=map_size
    )

    assert nav_map.x_size == 1, (
        f"Exepected map instance x_size value to be 1, got {nav_map.x_size}"
    )
    assert nav_map.y_size == 1, (
        f"Exepected map instance y_size value to be 1, got {nav_map.x_size}"
    )
