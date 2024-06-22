try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import FastAPI
from shapely import Point, LineString, Polygon

from pydantic import BaseModel
from pydantic_shapely.annotations import GeometryField


app = FastAPI()


class Test(BaseModel):
    """Test class for a feature which supports GeoJSON serialization.
    """
    geometry: Annotated[
        LineString | Polygon,
        GeometryField(),
    ]
    
    name: str = "Hello World"
    answer: int = 42



@app.get("/")
async def root() -> Test:
    return Test(geometry=Point(0,0))

