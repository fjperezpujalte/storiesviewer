from storiesviewer_backend.database.storage_interface import StorageInterface
from storiesviewer_backend.database.storage_mongodb import MongoDBStorage
#from storiesviewer_backend.database.file_storage import FileStorage
from storiesviewer_backend.config import settings

class StorageFactory:
    """Factory class to create storage instances based on configuration"""
    
    @staticmethod
    async def create_storage(storage_type: str = None) -> StorageInterface:
        """Create storage instance based on type or environment variable"""
        if storage_type is None:
            storage_type = settings.STORAGE_TYPE
        
        if storage_type.lower() == "mongodb":
            storage = MongoDBStorage(
                connection_string=settings.MONGODB_URL,
                database_name=settings.MONGODB_DATABASE
            )
            await storage.connect()
            return storage
        #elif storage_type.lower() == "file":
            #return FileStorage(storage_file=settings.STORAGE_FILE)
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")