from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="start_command")


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, ты в управлении ботом. \nДобро пожаловать")
