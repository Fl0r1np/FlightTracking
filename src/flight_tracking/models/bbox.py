from dataclasses import dataclass
from typing import Tuple

@dataclass
class BoundingBox:
    """
    Class to represent a geographical bounding box.
    """
    lamin: float
    lomin: float
    lamax: float
    lomax: float

    def __post_init__(self):
        """Validate the bounding box coordinates after initialization."""
        if self.lamin >= self.lamax:
            raise ValueError(f"lamin ({self.lamin}) must be strictly less than lamax ({self.lamax}).")
        if self.lomin >= self.lomax:
            raise ValueError(f"lomin ({self.lomin}) must be strictly less than lomax ({self.lomax}).")

    @classmethod
    def from_tuple(cls, coords: Tuple[float, float, float, float]) -> "BoundingBox":
        """
        Alternate constructor to create a BoundingBox from a tuple of coordinates
        :param coords: A tuple of coordinates (lamin, lomin, lamax, lomax)
        :return: Returns a BoundingBox object
        """
        if len(coords) != 4:
            raise ValueError(f"Bounding box tuple must contain exactly 4 values, got {len(coords)}")
        return cls(*coords)

    @classmethod
    def from_string(cls, bbox_str: str) -> "BoundingBox":
        """
        Alternate constructor to create a BoundingBox from a comma-separated string.
        :param bbox_str: A comma-separated string of coordinates
        :return: Returns a BoundingBox object
        """
        # Parse the string
        coords = [float(x.strip()) for x in bbox_str.split(",")]

        if len(coords) != 4:
            raise ValueError(f"Bounding box string must contain exactly 4 values, got {len(coords)}")

        return cls(*coords)

    def get_value(self) -> Tuple[float, float, float, float]:
        """
        A method to get the bounding box value
        :return: Returns a tuple representing the bounding box value
        """
        return (self.lamin, self.lomin, self.lamax, self.lomax)

    def __str__(self) -> str:
        return f"({self.lamin}, {self.lomin}, {self.lamax}, {self.lomax})"
