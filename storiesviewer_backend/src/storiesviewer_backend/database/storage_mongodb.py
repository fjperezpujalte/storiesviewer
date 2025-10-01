from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from storiesviewer_backend.model import Map, MapCreate, Keypoint, Story
from storiesviewer_backend.database.storage_interface import StorageInterface
import uuid
import os

class MongoDBStorage(StorageInterface):
    """MongoDB implementation of storage interface"""
    
    def __init__(self, connection_string: str = None, database_name: str = "maps_db"):
        self.connection_string = connection_string or os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.database_name = database_name
        self.client = None
        self.db = None
        self.collection = None
    
    async def connect(self):
        """Initialize MongoDB connection"""
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        self.collection = self.db.maps
        
        # Create indexes for better performance
        await self.collection.create_index("id", unique=True)
        await self.collection.create_index("name")
    
    async def create_map(self, map_data: MapCreate) -> Map:
        """Create a new map"""
        map_obj = Map(
            name=map_data.name,
            image=map_data.image,
            dimensions=map_data.dimensions,
            keypoints=map_data.keypoints or [],
            stories=map_data.stories or []
        )
        
        # Convert to dict for MongoDB storage
        map_dict = {
            "id": map_obj.id,
            "name": map_obj.name,
            "image": map_obj.image,
            "dimensions": list(map_obj.dimensions),
            "keypoints": [{"id": kp.id, "content": kp.content} for kp in map_obj.keypoints],
            "stories": [{"id": story.id, "content": story.content} for story in map_obj.stories]
        }
        
        await self.collection.insert_one(map_dict)
        return map_obj
    
    async def get_map(self, map_id: str) -> Optional[Map]:
        """Get a map by ID"""
        map_data = await self.collection.find_one({"id": map_id})
        if not map_data:
            return None
        
        return self._dict_to_map(map_data)
    
    async def get_all_maps(self) -> List[Map]:
        """Get all maps"""
        maps = []
        async for map_data in self.collection.find():
            maps.append(self._dict_to_map(map_data))
        return maps
    
    async def delete_map(self, map_id: str) -> bool:
        """Delete a map by ID"""
        result = await self.collection.delete_one({"id": map_id})
        return result.deleted_count > 0
    
    async def add_keypoint(self, map_id: str, keypoint: Keypoint) -> bool:
        """Add a keypoint to a map"""
        keypoint_dict = {"id": keypoint.id, "content": keypoint.content}
        result = await self.collection.update_one(
            {"id": map_id},
            {"$push": {"keypoints": keypoint_dict}}
        )
        return result.modified_count > 0
    
    async def delete_keypoint(self, map_id: str, keypoint_id: str) -> bool:
        """Delete a keypoint from a map"""
        result = await self.collection.update_one(
            {"id": map_id},
            {"$pull": {"keypoints": {"id": keypoint_id}}}
        )
        return result.modified_count > 0
    
    async def add_story(self, map_id: str, story: Story) -> bool:
        """Add a story to a map"""
        story_dict = {"id": story.id, "content": story.content}
        result = await self.collection.update_one(
            {"id": map_id},
            {"$push": {"stories": story_dict}}
        )
        return result.modified_count > 0
    
    async def delete_story(self, map_id: str, story_id: str) -> bool:
        """Delete a story from a map"""
        result = await self.collection.update_one(
            {"id": map_id},
            {"$pull": {"stories": {"id": story_id}}}
        )
        return result.modified_count > 0
    
    async def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
    
    def _dict_to_map(self, map_data: dict) -> Map:
        """Convert MongoDB document to Map object"""
        keypoints = [Keypoint(**kp) for kp in map_data.get('keypoints', [])]
        stories = [Story(**story) for story in map_data.get('stories', [])]
        
        return Map(
            id=map_data['id'],
            name=map_data['name'],
            image=map_data['image'],
            dimensions=tuple(map_data['dimensions']),
            keypoints=keypoints,
            stories=stories
        )
