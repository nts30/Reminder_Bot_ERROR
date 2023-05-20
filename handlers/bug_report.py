import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot_config import bot, config
from buttons import cancel_kb


class ReportAnswer(StatesGroup):
    send_answer = State()


class Report(StatesGroup):
    send_report = State()


bug_report_callback_info = CallbackData('report_answer', 'user_id')


async def start_bug_report(message: types.Message):
    await message.answer('Опишите проблему, с которой вы столкнулись', reply_markup=cancel_kb)
    await Report.send_report.set()


async def send_report(message: types.Message, state: FSMContext):
    send_report_answer = InlineKeyboardMarkup().add(
        InlineKeyboardMarkup(text='Ответить', callback_data=bug_report_callback_info.new(user_id=message.from_user.id))
    )
    await bot.copy_message(config.tg_bot.ADMIN_ID, message.from_user.id, reply_markup=send_report_answer)
    await message.reply('Спасибо за вашу помощь', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def get_answer(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data['user_id']

    await state.update_data(id=user_id)
    await state.update_data(message_id=callback_query.message.message_id)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Введите текст ответа')

    await state.get_state(ReportAnswer.send_answer.state)


async def send_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('id')
    message_id = data.get('message_id')

    await bot.delete_message(message.from_user.id, message_id)
    await bot.send_message(user_id, message.text)
    await state.finish()

def bug_report_register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bug_report, commands='bug_report')

    dp.register_message_handler(send_report, state=Report.send_report)

    dp.register_message_handler(send_report, state=ReportAnswer.send_answer)

    dp.register_callback_query_handler(get_answer, bug_report_callback_info.filter())

