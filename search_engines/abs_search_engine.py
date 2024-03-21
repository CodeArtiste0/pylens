from abc import ABC, abstractmethod
import requests

class AbsSearchEngine(ABC):
    @abstractmethod
    def send_image(self, image_url: str, langs: str):
        """
        Sends an image to the search engine.
        :param image: The image to be searched.
        :return: The search engine's response.
        """
        pass

    @abstractmethod
    def parse_results(self, response):
        """
        Parses the search engine's response to extract similar images.
        :param response: The response from the search engine.
        :return: A list of URLs of similar images.
        """
        pass

    def get_name(self) -> str:
        return self.__class__.__name__
