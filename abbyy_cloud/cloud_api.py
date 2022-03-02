import shutil

import requests
import json
from utils.env_variables import Endpoint, Auth

from logging import getLogger

logger = getLogger(__name__)


class ABBYYCloudAPI:
    """
    Call abbyy cloud ocr api with project id and pwd
    """
    image = None
    setting = None
    app_id = Auth.abbyy_appid
    app_pwd = Auth.abbyy_pwd
    cloud_api = Endpoint.abbyy_api

    def __init__(self, image, setting):
        self.image = image
        self.setting = setting

    def text_detection(self):
        url_params = {
            "language": self.setting.Language,
            "exportFormat": self.setting.OutputFormat
        }
        request_url = self.get_request_url("processImage")
        response = requests.post(request_url, data=self.image, params=url_params,
                                 auth=(self.app_id, self.app_pwd))
        task = self.decode_response(response.text)
        return task

    def get_task_status(self, task):
        if task.Id.find('00000000-0') != -1:
            # GUID_NULL is being passed. This may be caused by a logical error in the calling code
            logger.error("Null task id passed")
            return None
        url_params = {"taskId": task.Id}
        status_url = self.get_request_url("getTaskStatus")
        response = requests.get(status_url, params=url_params,
                                auth=(self.app_id, self.app_pwd), )
        task = self.decode_response(response.text)
        return task

    def decode_response(self, json_response):
        """ Decode json response of the server. Return Task object """
        # logger.debug("json_response:{}".format(json_response))
        response_value = json.loads(json_response)
        task = Task()
        task.Id = response_value["taskId"]
        task.Status = response_value["status"]
        if task.Status == "Completed":
            task.DownloadUrl = response_value["resultUrls"][0]
        return task

    def download_result(self, task, output_path):
        get_result_url = task.DownloadUrl
        if get_result_url is None:
            print("No download URL found")
            return

        file_response = requests.get(get_result_url, stream=True)
        with open(output_path, 'wb') as output_file:
            shutil.copyfileobj(file_response.raw, output_file)

    def get_request_url(self, url):
        return self.cloud_api.strip('/') + '/' + url.strip('/')


class Task:
    Status = "Unknown"
    Id = None
    DownloadUrl = None

    def is_active(self):
        if self.Status == "InProgress" or self.Status == "Queued":
            return True
        else:
            return False


class ProcessingSettings:
    Language = "Japanese, English"
    OutputFormat = "docx"
