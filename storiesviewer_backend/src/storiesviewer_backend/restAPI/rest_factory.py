from storiesviewer_backend.restAPI.rest_fastapi import RestFastAPI
from storiesviewer_backend.restAPI.rest_interface import RestInterface


class RestFactory:
    """Factory class to create storage instances based on configuration"""
    
    @staticmethod
    async def create_restapi(rest_type: str = None) -> RestInterface:
        if rest_type is None:
            rest_type = settings.STORAGE_TYPE
        
        if rest_type.lower() == "fastapi":
            rest = RestFastAPI()
            return rest
        else:
            raise ValueError(f"Unsupported storage type: {rest_type}")