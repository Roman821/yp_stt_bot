from telebot.types import ReplyKeyboardMarkup, KeyboardButton


_HELP_BUTTON = KeyboardButton(text='/help')


TTS_INACTIVE_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)

TTS_INACTIVE_MARKUP.add(_HELP_BUTTON)
TTS_INACTIVE_MARKUP.add(KeyboardButton(text='/start_stt'))


TTS_ACTIVE_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)

TTS_ACTIVE_MARKUP.add(_HELP_BUTTON)
TTS_ACTIVE_MARKUP.add(KeyboardButton(text='/stop_stt'))
