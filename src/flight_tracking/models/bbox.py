class BoundingBox:
    '''
    Class to represent a bounding box
    '''

    def __init__(self, lamin: float, lomin: float, lamax:float, lomax:float):
        self.lamin = lamin
        self.lomin = lomin
        self.lamax = lamax
        self.lomax = lomax

    @classmethod
    def from_tuple(cls, coords: tuple) -> BoundingBox:
        """
        Alternate constructor to create a BoundingBox from a tuple of coordinates
        :param coords: A tuple of coordinates
        :return: Returns a BoundingBox object
        """
        return cls(*coords)

    @classmethod
    def from_string(cls, bbox_str: str) -> BoundingBox:
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

    def get_value(self) -> tuple:
        """
        A method to get the bounding box value
        :return: Returns a touple representing the bounding box value
        """
        return (self.lamin, self.lomin, self.lamax, self.lomax)

    def __str__(self) -> str:
        return f"(${self.lamin}, ${self.lomin}, ${self.lamax}, ${self.lomax})"





