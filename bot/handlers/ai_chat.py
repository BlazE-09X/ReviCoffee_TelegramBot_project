from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from ai.analysis import answer_manager_question
from bot.keyboards.main_menu import get_main_menu

router = Router()


class AIStates(StatesGroup):
    waiting_question = State()


@router.callback_query(F.data == "menu_ask_ai")
async def start_ai_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIStates.waiting_question)
    await callback.message.edit_text("Задай вопрос о данных ревизии (например: «где больше всего теряем деньги?»)")


@router.message(AIStates.waiting_question)
async def handle_ai_question(message: Message, state: FSMContext):
    await message.answer("Думаю...")
    answer = answer_manager_question(message.text)
    await message.answer(answer, reply_markup=get_main_menu())
    await state.clear()