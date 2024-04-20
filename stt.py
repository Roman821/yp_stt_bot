from math import ceil
from functools import cache

from requests import post

from get_logger import get_logger
from settings import STT_API_KEY, STT_FOLDER_ID, STT_SECONDS_IN_BLOCK, STT_URL, STT_LANGUAGE


class STT:

    def __init__(self):
        self.logger = get_logger('main')

    @staticmethod
    @cache
    def get_seconds_blocks(duration: float | int) -> int:
        return ceil(duration / STT_SECONDS_IN_BLOCK)

    def ask(self, audio: bytes) -> tuple[bool, str]:
        """Returns a bool (True if success, else False) and a string (error message or STT result)"""

        error_message = 'Произошла ошибка, пожалуйста, повторите попытку или обратитесь в поддержку'

        try:
            response = post(
                STT_URL,
                headers={
                    'Authorization': f'Api-Key {STT_API_KEY}',
                },
                params={
                    'lang': STT_LANGUAGE,
                    'folderId': STT_FOLDER_ID,
                },
                data=audio,
            )

        except Exception as e:

            self.logger.error(f'An exception occurred while requesting STT answer: {e}')

            return False, error_message

        response_status_code = response.status_code

        if response_status_code != 200:

            self.logger.error(f'Incorrect STT answer status code: {response_status_code}')

            return False, error_message

        return True, response.json()['result']


stt = STT()
