import requests
import os
from dotenv import load_dotenv

import log_util

logger = log_util.get_logger()
load_dotenv()

HOST = os.getenv("HOST")
DEVICE_ID = os.getenv("DEVICE_ID")

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

	except Exception as e:
		logger.error(e)
		pass

	if 200 >= response.status_code < 300:
		logger.info("Request successful")
		# TODO: Light green LED
	else:
		logger.info("Request failed with status " + str(response.status_code))
		# TODO: Light red LED