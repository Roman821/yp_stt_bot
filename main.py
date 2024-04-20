from random import choice

from telebot import TeleBot, types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

from stt import stt
from settings import BOT_TOKEN, SECONDS_BLOCKS_LIMIT_BY_USER, REQUEST_MAX_SECONDS
from database import SessionLocal, create_all_tables
from crud import UserCrud
from markups import TTS_INACTIVE_MARKUP, TTS_ACTIVE_MARKUP


class STTStates(StatesGroup):

    inactive = State()
    active = State()


def run_bot() -> None:

    bot = TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())

    bot.add_custom_filter(custom_filters.StateFilter(bot))

    def get_state_markup(message: types.Message) -> types.ReplyKeyboardMarkup:

        if bot.get_state(message.from_user.id) == STTStates.inactive.name:
            return TTS_INACTIVE_MARKUP

        else:
            return TTS_ACTIVE_MARKUP

    @bot.message_handler(commands=['help', 'start'])
    def help_handler(message: types.Message):

        reply_message = (
            'Привет, я - бот-speech-to-text (перевожу голос в текст), вот мои команды:\n'
            '/help или /start - список всех команд (ты уже тут)\n'
            '/start_stt - запуск перевода голоса в текст\n'
            '/stop_stt - остановка перевода голоса в текст\n'
            'P.S. На каждого пользователя есть лимит блоков секунд (по 15 секунд в каждом):'
            f' {SECONDS_BLOCKS_LIMIT_BY_USER}, без этого никак('
        )

        bot.reply_to(message, reply_message, reply_markup=get_state_markup(message))

    def ask_stt_safe_handler(message: types.Message) -> str:
        """
        Performs a safe request to STT, returning an STT answer or error message if a user exceeds the character limit
        """
        with SessionLocal() as db:

            user_crud = UserCrud(db)

            user = user_crud.get(telegram_id=message.from_user.id)

            if not user:
                user = user_crud.create(telegram_id=message.from_user.id)

            if user.seconds_blocks_spent > SECONDS_BLOCKS_LIMIT_BY_USER:
                return (
                    'Не удалось получить ответ от STT сервиса, к сожалению, вы превысили лимит блоков секунд на'
                    ' пользователя(('
                )

            voice: bytes = bot.download_file(bot.get_file(message.voice.file_id).file_path)
            message_seconds_blocks = stt.get_seconds_blocks(message.voice.duration)

            is_stt_success, stt_answer = stt.ask(voice)

            if is_stt_success:
                user_crud.update(user, seconds_blocks_spent=user.seconds_blocks_spent + message_seconds_blocks)

            return stt_answer + f'\n\nБлоков секунд потрачено: {message_seconds_blocks}'

    @bot.message_handler(state=STTStates.active, content_types=['voice'])
    def process_stt_message(message: types.Message):

        if message.voice.duration > REQUEST_MAX_SECONDS:

            bot.reply_to(
                message,
                f'Сообщение слишком длительное (больше, чем {REQUEST_MAX_SECONDS}), пожалуйста, укоротите его'
            )

            return

        stt_answer = ask_stt_safe_handler(message)

        bot.reply_to(message, stt_answer)

    @bot.message_handler(commands=['start_stt'])
    def start_stt(message: types.Message):

        bot.set_state(message.from_user.id, STTStates.active, message.chat.id)

        bot.reply_to(
            message,
            'Теперь все ваши голосовые сообщения будут переводиться в текст',
            reply_markup=TTS_ACTIVE_MARKUP,
        )

    @bot.message_handler(commands=['stop_stt'])
    def stop_stt(message: types.Message):

        bot.set_state(message.from_user.id, STTStates.inactive, message.chat.id)

        bot.reply_to(
            message,
            'Теперь все ваши голосовые сообщения НЕ будут переводиться в текст',
            reply_markup=TTS_INACTIVE_MARKUP,
        )

    @bot.message_handler(content_types=['text'])
    def unknown_messages_handler(message: types.Message):

        replies = (
            'О, круто!',
            'Верно подмечено!',
            'Как с языка снял',
            'Какой ты всё-таки умный',
            'По-любому что-то умное написал',
            'Как лаконично-то!',
        )

        help_message = (
            '\n\nЕсли ты хотел, чтобы я что-то сделал, то я не распознал твою команду, пожалуйста, сверься с /help'
        )

        bot.reply_to(message, choice(replies) + help_message, reply_markup=get_state_markup(message))

    bot.infinity_polling()


def main():

    create_all_tables()

    run_bot()


if __name__ == '__main__':
    main()
