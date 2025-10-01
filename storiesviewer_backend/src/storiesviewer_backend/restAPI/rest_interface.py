

from abc import ABC, abstractmethod

from storiesviewer_backend.model import Keypoint, Map, MapCreate, Story


class RestInterface(ABC):
    """Interface for the REST API service"""

    @abstractmethod
    async def root():
        "TODO"
        pass

    @abstractmethod
    async def create_map(map_data: MapCreate):
        """Create a new map"""
        pass

    @abstractmethod
    async def get_all_maps():
        """Get all maps"""
        pass

    @abstractmethod
    async def get_map(map_id: str) -> Map: 
        """Get a specific map by ID"""
        pass

    @abstractmethod
    async def delete_map(map_id: str):
        """Delete a map by ID"""
        pass


    @abstractmethod
    async def add_keypoint(map_id: str, keypoint: Keypoint):
        """Add a keypoint to a map"""
        pass

    @abstractmethod
    async def delete_keypoint(map_id: str, keypoint_id: str):
        """Delete a keypoint from a map"""
        pass


    @abstractmethod
    async def add_story(map_id: str, story: Story):
        pass

    @abstractmethod
    async def delete_story(map_id: str, story_id: str):
        pass

    @abstractmethod
    def run():
        pass
