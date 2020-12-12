from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hcode, quote_html, hbold
from loguru import logger

from onbot.core.config import ADMIN, GID
from onbot.core.loader import dp
from onbot.core.tools import get_question, get_var
from onbot.keyboard.inline import change_answer
from onbot.models import User, Question


@dp.message_handler(commands="start")
async def start(message: types.Message):
    user = message.from_user
    await message.answer(f"Assalomu alaykum {user.full_name}")
    u = await User.get_or_none(uid=user.id)
    if not u:
        await User.create(
            uid=user.id,
            name=user.full_name,
            uname=user.username
        )
    if not user.id == ADMIN:
        await dp.bot.send_message(ADMIN, f"{user.full_name} {user.id} {user.username}")


@dp.message_handler(Text(equals=["a", "b", "c", "d"], ignore_case=True))
async def catch_answer(message: types.Message):
    # user = await dp.bot.get_chat_member(GID, user_id=message.from_user.id)
    # if not user:
    #     return False
    try:
        if not message.reply_to_message:
            return False
        msg = message.reply_to_message
        if not msg.text:
            return False
        text = get_question(msg.text)
        if not text:
            return False
        var = get_var(message.text, msg.text)
        if not var:
            return False
        question = await Question.get_or_none(question=text)
        if not question:
            await Question.create(question=text, answer=var)
        else:
            answer = question.answer
            if not answer == var:
                await question.update_from_dict(
                    {"temp_answer": var}).save()
                markup = change_answer(question.id)
                text = f"<b>Oldingi javob: </b><i>{quote_html(answer)}</i>\n"
                text += f"<b>Hozirgi javob: </b><i>{quote_html(var)}</i>\n"
                await message.reply(text, reply_markup=markup, disable_web_page_preview=True)
    except Exception as e:
        await dp.bot.send_message(ADMIN, hcode(e))


@dp.message_handler(Text(contains="Select one:"))
@dp.message_handler(Text(contains="Выберите один ответ:"))
async def catch_question(message: types.Message):
    # user = await dp.bot.get_chat_member(GID, user_id=message.from_user.id)
    # if not user:
    #     return False
    try:
        text = get_question(message.text)
        if text:
            question = await Question.get_or_none(question=text)
            if question:
                await message.reply(
                    f"<b>{quote_html(question.answer)}</b>",
                    disable_web_page_preview=True
                )
    except Exception as e:
        await dp.bot.send_message(ADMIN, hcode(e))


@dp.message_handler(commands="count")
async def count_(message: types.Message):
    # user = await dp.bot.get_chat_member(GID, user_id=message.from_user.id)
    # if not user:
    #     return False
    count = await Question.all().count()
    await message.reply(hbold(str(count)))


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_chat(message: types.Message):
    for i in message.new_chat_members:
        if i.username == "oraliqnazoratbot":
            if not message.chat.id == GID:
                await dp.bot.leave_chat(message.chat.id)
                await dp.bot.send_message(ADMIN, str(message.chat.id))


@dp.callback_query_handler(Text(startswith="cans"))
async def update_answer(query: types.CallbackQuery):
    # user = await dp.bot.get_chat_member(GID, user_id=query.from_user.id)
    # if not user:
    #     return False
    b_ = (query.from_user.id == ADMIN)
    b = (query.message.reply_to_message.from_user.id == query.from_user.id)
    if b or b_:
        action = query.data.split("_")[1]
        if action == "d":
            await query.answer("Bekor qilindi!")
        elif action == "u":
            qid = int(query.data.split("_")[2])
            question = await Question.get_or_none(id=qid)
            temp = question.temp_answer
            await question.update_from_dict(
                {"answer": temp}
            ).save()
            await query.answer("Yangilandi✅")
        await query.message.delete()
    else:
        await query.answer("Bu xabar sizga emas!")
        return False


@dp.message_handler(commands="ans")
async def answer_(message: types.Message):
    try:
        if not message.reply_to_message:
            return False
        msg = message.reply_to_message
        text = get_question(msg.text)
        if not text:
            return False
        question = await Question.get_or_none(question=text)
        if not question:
            return False
        answer = question.answer
        await msg.reply(hbold(answer), disable_web_page_preview=True)
        await message.delete()
    except Exception as e:
        await dp.bot.send_message(ADMIN, hcode(e))
