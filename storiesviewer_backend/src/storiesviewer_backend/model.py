from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
import uuid


class Story(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str = Field(..., description="Story content")

class Keypoint(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()))
    name : str = Field(..., description="Descriptibve name of the keypoint on the map, it must be unique")
    point : Tuple[int, int] = Field(..., description="Location in the map of the keypoint in pixels")
    content: Optional[str] = Field(default_factory=str, description="Keypoint content")
    stories : Optional[List[Story]] = Field(default_factory=list, description="Stories associated to the keypoint")

class MapCreate(BaseModel):
    name: str = Field(..., description="Name of the map")
    image: str = Field(..., description="Image URL or path")
    dimensions: Tuple[int, int] = Field(..., description="Image dimensions (width, height)")
    keypoints: Optional[List[Keypoint]] = Field(default_factory=list)
    stories: Optional[List[Story]] = Field(default_factory=list)

class Map(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    image: str
    dimensions: Tuple[int, int]
    keypoints: List[Keypoint] = Field(default_factory=list)
    stories: List[Story] = Field(default_factory=list)

class MapResponse(BaseModel):
    id: str
    name: str
    image: str
    dimensions: Tuple[int, int]
    keypoints: List[Keypoint]
    stories: List[Story]
    
