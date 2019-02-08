import requests
import os
from dotenv import load_dotenv

import LED
import log_util

logger = log_util.get_logger()
load_dotenv()

HOST = os.getenv("HOST")
DEVICE_ID = os.getenv("DEVICE_ID")

RED_PIN = int(os.getenv("RED_PIN"))
GREEN_PIN = int(os.getenv("GREEN_PIN"))

while True:
        card_content = input()
        card_id = card_content[6:14]
        logger.info("Card swiped: " + card_id)

        try:
                response = requests.request(
                        "POST",
                        HOST + "/card_read",
                        data={
                                "device_id": DEVICE_ID,
                                "card_id": card_id
                        })
                if response and 200 >= response.status_code < 300:
                        logger.info("Request successful")
                        LED.ligh_led(GREEN_PIN, 1)
                else:
                        logger.info("Request failed with status " + str(response.status_code))
                        LED.light_led(RED_PIN, 1)
        except Exception as e:
                logger.error(e)
                LED.light_led(RED_PIN, 1)
        
