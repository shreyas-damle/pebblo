from fastapi import APIRouter, Depends

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.service.prompt_gov import PromptGov
from pebblo.app.service.prompt_service import Prompt
from pebblo.app.utils.handler_mapper import get_handler


config_details = var_server_config_dict.get()


class App:
    """
    Controller Class for all the api endpoints for App resource.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def discover(data: dict, discover_obj=Depends(lambda: get_handler(handler_name='discover'))):
        # "/app/discover" API entrypoint
        # Execute discover object based on a storage type
        response = discover_obj.process_request(data)
        return response

    @staticmethod
    def loader_doc(data: dict, discover_obj=Depends(lambda: get_handler(handler_name='discover'))):
        # "/loader/doc" API entrypoint
        # Execute loader doc object based on a storage type
        response = discover_obj.process_request(data)
        return response

    @staticmethod
    def prompt(data: dict):
        # "/prompt" API entrypoint
        prompt_obj = Prompt(data=data)
        response = prompt_obj.process_request()
        return response

    @staticmethod
    def promptgov(data: dict):
        # "/prompt/governance" API entrypoint
        prompt_obj = PromptGov(data=data)
        response = prompt_obj.process_request()
        return response
