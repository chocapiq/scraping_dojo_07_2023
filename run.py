import re
import json
from typing import List

import requests
from bs4 import BeautifulSoup
import jsonlines

from variables import Variables


class WebScraper(Variables):

    def __init__(self):
        super().__init__()
        self.proxy = super().PROXY
        self.input_url = super().INPUT_URL
        self.output_file = super().OUTPUT_FILE

    def data_extractor(self) -> List:
        """
        Extracts specific data from the HTML page contained within <script> tags.
        :return: List of all data found within <script> tag
        """

        response = requests.get(self.input_url)
        launch_page = response.text
        soup = BeautifulSoup(launch_page, "html.parser")
        return soup.find_all("script")

    def process_data(self) -> json:
        """
        Cleans the data and converts it to json format
        :return: json data
        """
        script_tags = self.data_extractor()
        json_data = json.dumps(dict())

        for script_tag in script_tags:
            script_content = script_tag.string
            try:
                if "data" in script_content:
                    script_content = script_content.split("=")[2]
                    script_content = re.split(r"(]);", script_content)
                    script_content = script_content[0] + script_content[1]
                    json_data = json.loads(script_content)
                    break
            except AttributeError:
                continue
            except TypeError:
                continue

        return json_data

    def save_data(self):
        """
        saves the data to .jsonl file in the same directory
        :return: None
        """
        json_data = self.process_data()
        with jsonlines.open(self.output_file, mode="w") as jsonl_writer:
            for data in json_data:
                text = data["text"]
                author = data["author"]["name"]
                tags = data["tags"]
                jsonl_writer.write({"text": text, "by": author, "tags": tags})


if __name__ == "__main__":
    webscraper = WebScraper()
    webscraper.save_data()
