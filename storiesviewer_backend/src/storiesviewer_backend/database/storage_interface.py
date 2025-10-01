from abc import ABC, abstractmethod
from typing import List, Optional

from storiesviewer_backend.model import MapCreate, Map, Keypoint, Story

class StorageInterface(ABC):
    """Abstract interface for storage operations using facade pattern"""
    
    @abstractmethod
    async def create_map(self, map_data: MapCreate) -> Map:
        """Create a new map"""
        pass
    
    @abstractmethod
    async def get_map(self, map_id: str) -> Optional[Map]:
        """Get a map by ID"""
        pass
    
    @abstractmethod
    async def get_all_maps(self) -> List[Map]:
        """Get all maps"""
        pass
    
    @abstractmethod
    async def delete_map(self, map_id: str) -> bool:
        """Delete a map by ID"""
        pass
    
    @abstractmethod
    async def add_keypoint(self, map_id: str, keypoint: Keypoint) -> bool:
        """Add a keypoint to a map"""
        pass
    
    @abstractmethod
    async def delete_keypoint(self, map_id: str, keypoint_id: str) -> bool:
        """Delete a keypoint from a map"""
        pass
    
    @abstractmethod
    async def add_story(self, map_id: str, story: Story) -> bool:
        """Add a story to a map"""
        pass
    
    @abstractmethod
    async def delete_story(self, map_id: str, story_id: str) -> bool:
        """Delete a story from a map"""
        pass
    
    @abstractmethod
    async def close(self):
        """Close database connection"""
        pass