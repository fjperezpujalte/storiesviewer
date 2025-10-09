import asyncio

from storiesviewer_backend.restAPI.rest_factory import RestFactory
from storiesviewer_backend.restAPI.rest_interface import RestInterface

if __name__ == "__main__":
    rest : RestInterface = asyncio.run(RestFactory.create_restapi())
    rest.run()