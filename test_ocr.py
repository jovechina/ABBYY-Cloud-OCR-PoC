import time

import yaml
from logging import getLogger, config

from abbyy_cloud.cloud_api import ABBYYCloudAPI, ProcessingSettings
from utils.file_utils import FileUtils

logger = getLogger(__name__)


def main():
    logger.debug("main started")
    file_name = "D:/learning/tmp/test.jpg"
    image = FileUtils.load_image(file_name)
    settings = ProcessingSettings()
    settings.OutputFormat = "txt"
    cloud_api = ABBYYCloudAPI(image, settings)
    task = cloud_api.text_detection()

    logger.debug("Id = {}".format(task.Id))
    logger.debug("Status = {}".format(task.Status))

    while task.is_active():
        time.sleep(5)
        logger.debug(".")
        task = cloud_api.get_task_status(task)

    logger.debug("Status = {}".format(task.Status))

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            cloud_api.download_result(task, "D:/learning/tmp/test.txt")
            logger.debug("Result was written to {}".format("D:/learning/tmp/test.txt"))
    else:
        logger.debug("Error processing task")

    logger.debug("main completed")


if __name__ == '__main__':
    config.dictConfig(yaml.load(open("logging.yaml").read(), Loader=yaml.SafeLoader))
main()
