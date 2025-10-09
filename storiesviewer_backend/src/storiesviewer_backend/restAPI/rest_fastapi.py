from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from storiesviewer_backend.restAPI.rest_interface import RestInterface
import uvicorn
from typing import List, Optional
import uuid
from storiesviewer_backend.model import Keypoint, MapCreate, MapResponse, Story
from contextlib import asynccontextmanager
from storiesviewer_backend.database.storage_interface import StorageInterface
from storiesviewer_backend.database.storage_factory import StorageFactory
from fastapi import APIRouter

class RestFastAPI(RestInterface):
    def __init__(self):
        self.router = APIRouter(prefix="")

    @staticmethod
    async def root():
        return {"message": "Maps API is running"}

    # Maps endpoints
    @staticmethod
    async def create_map(map_data: MapCreate):
        """Create a new map"""
        try:
            map_obj = storage.create_map(map_data)
            return map_obj
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_all_maps():
        """Get all maps"""
        return storage.get_all_maps()

    @staticmethod
    async def get_map(map_id: str):
        """Get a specific map by ID"""
        map_obj = storage.get_map(map_id)
        if not map_obj:
            raise HTTPException(status_code=404, detail="Map not found")
        return map_obj

    @staticmethod
    async def delete_map(map_id: str):
        """Delete a map by ID"""
        success = storage.delete_map(map_id)
        if not success:
            raise HTTPException(status_code=404, detail="Map not found")
        return {"message": "Map deleted successfully"}


    # Keypoints endpoints
    @staticmethod
    async def add_keypoint(map_id: str, keypoint: Keypoint):
        """Add a keypoint to a map"""
        success = storage.add_keypoint(map_id, keypoint)
        if not success:
            raise HTTPException(status_code=404, detail="Map not found")
        return {"message": "Keypoint added successfully"}

    @staticmethod
    async def delete_keypoint(map_id: str, keypoint_id: str):
        """Delete a keypoint from a map"""
        success = storage.delete_keypoint(map_id, keypoint_id)
        if not success:
            raise HTTPException(status_code=404, detail="Map or keypoint not found")
        return {"message": "Keypoint deleted successfully"}

    # Stories endpoints
    @staticmethod
    async def add_story(map_id: str, story: Story):
        """Add a story to a map"""
        success = storage.add_story(map_id, story)
        if not success:
            raise HTTPException(status_code=404, detail="Map not found")
        return {"message": "Story added successfully"}

    @staticmethod
    async def delete_story(map_id: str, story_id: str):
        """Delete a story from a map"""
        success = storage.delete_story(map_id, story_id)
        if not success:
            raise HTTPException(status_code=404, detail="Map or story not found")
        return {"message": "Story deleted successfully"}

    def run(self):

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            global storage
            storage = await StorageFactory.create_storage()
            yield
            await storage.close()


    
        app = FastAPI(title="StoriesViewer Map API", description="API for managing maps of StoriesViewer", 
                version="0.1.0", lifespan=lifespan)

        self.router.add_api_route("/", RestFastAPI.root, methods=["GET"])
        self.router.add_api_route("/maps", RestFastAPI.create_map, methods=["POST"])
        self.router.add_api_route("/maps", RestFastAPI.get_all_maps, methods=["GET"])
        self.router.add_api_route("/maps/{map_id}", RestFastAPI.get_map, methods=["GET"])
        self.router.add_api_route("/maps/{map_id}", RestFastAPI.delete_map, methods=["DELETE"])
        self.router.add_api_route("/maps/{map_id}/keypoints", RestFastAPI.add_keypoint, methods=["POST"])
        self.router.add_api_route(
            "/maps/{map_id}/keypoints/{keypoint_id}",
            RestFastAPI.delete_keypoint,
            methods=["DELETE"],
        )
        self.router.add_api_route("/maps/{map_id}/stories", RestFastAPI.add_story, methods=["POST"])
        self.router.add_api_route(
            "/maps/{map_id}/stories/{story_id}",
            RestFastAPI.delete_story,
            methods=["DELETE"],
        )

        #include the router in the application
        app.include_router(self.router)

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        uvicorn.run(app, host="0.0.0.0", port=8000)
        