# bot.py

import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import BOT_TOKEN, CHANNEL_USERNAME
from languages import languages
from keyboards import get_language_keyboard, get_main_menu
from states import VacancyForm

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Har foydalanuvchining tilini saqlaymiz
user_languages = {}

# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Step vakansiya \nTilni tanlang / Выберите язык / Choose language / Til saylań:",
        reply_markup=get_language_keyboard()
    )

# Til tanlanganda
@dp.message(F.text.in_([lang["lang_name"] for lang in languages.values()]))
async def select_language(message: types.Message):
    for code, lang in languages.items():
        if message.text == lang["lang_name"]:
            user_languages[message.from_user.id] = code
            await message.answer(lang["start_text"], reply_markup=get_main_menu(code))
            break

# Vakansiya qo‘shish jarayoni
@dp.message(F.text)
async def handle_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_languages:
        await message.answer("Avval /start buyrug‘ini yuboring va tilni tanlang.")
        return

    lang_code = user_languages[user_id]
    lang = languages[lang_code]

    # Agar "Vakansiya qo‘shish" bosilgan bo‘lsa
    if message.text == lang["add_vacancy"]:
        await state.update_data(vacancy_data=[])
        await state.update_data(current_index=0)
        await message.answer(f"{lang['fields'][0]}:")
        await state.set_state(VacancyForm.waiting_for_field)
        return

    # Agar FSM holatida bo‘lsa
    if await state.get_state() == VacancyForm.waiting_for_field.state:
        data = await state.get_data()
        current_index = data.get("current_index", 0)
        vacancy_data = data.get("vacancy_data", [])
        vacancy_data.append(message.text)
        current_index += 1

        await state.update_data(vacancy_data=vacancy_data, current_index=current_index)

        if current_index < len(lang["fields"]):
            await message.answer(f"{lang['fields'][current_index]}:")
        else:
            # Hamma ma'lumot to‘plandi
            text = "\n".join(
                [f"<b>{lang['fields'][i]}:</b> {vacancy_data[i]}" for i in range(len(lang["fields"]))]
            )

            await bot.send_message(
                CHANNEL_USERNAME,
                f"📢 <b>diqqat taza vakansiya!</b>\n\n{text}",
                parse_mode="HTML"
            )

            await message.answer(lang["done"], reply_markup=get_main_menu(lang_code))
            await state.clear()

# Asosiy ishga tushirish
async def main():
    print("🤖 Step Vakansiya bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
