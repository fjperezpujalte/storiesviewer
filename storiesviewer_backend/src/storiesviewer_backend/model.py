from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
import uuid

class Keypoint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str = Field(..., description="Keypoint content")

class Story(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str = Field(..., description="Story content")

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
    
