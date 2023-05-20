import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from buttons import start_kb


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.set_state()
    if current_state is None:
        return

    logging.info(f'Cancelling state {current_state}')
    await message.reply('Ввод отменен', reply_markup=start_kb)
    await state.finish()


def other_register_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel, state='*', commands=['отмена', 'cancel'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
