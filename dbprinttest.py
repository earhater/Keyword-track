import asyncio
import datetime
import aiogram
import time
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import executor, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()

bot = aiogram.Bot(token='5357424511:AAF2TUW-N2a8Dpacjq0nKUlwrsfJYrTg56Q')
dp = Dispatcher(bot, storage=storage)
from db import Database
dbf = Database("./base.db")
from list import x as ggg

class UserState(StatesGroup):
    typer = State()
    coin = State()
    stage = State()


async def main(stager):
	keyboard = InlineKeyboardMarkup()
	y = dbf.select_coins_over_categories(0, 0, stager)
	ui = []
	for i in ggg.split("\n"):
		for ix in y:
			if ix[0] == i:
				ui.append(ix)

	print(ui)
	button12 = InlineKeyboardButton("НАЗАд", callback_data="back")
	keyboard.add(button12)
	return keyboard


@dp.message_handler(commands=['start'])
async def selectpart(message):#checking stage

	await bot.send_message(message.from_user.id, "временной отрезок (шаг 5 минут)", reply_markup=dbf.part_keyboard())
	await UserState.stage.set()


@dp.callback_query_handler(state=UserState.stage)#check coin
async def selectcoin(query: types.CallbackQuery,state:FSMContext):
	await state.update_data(stage=query.data)
	if query.data == 'back':
		await state.finish()
		await bot.send_message(query.from_user.id, "временной отрезок (шаг 5 минут)", reply_markup=dbf.part_keyboard())
		await UserState.stage.set()
	else:
		await bot.send_message(query.from_user.id, "Дальше позицию",reply_markup=dbf.gpt(query.data))
		await UserState.typer.set()


@dp.callback_query_handler(state=UserState.typer)#check type
async def selecttype(query: types.CallbackQuery,  state: FSMContext ):
	await state.update_data(coin=query.data)
	pos = InlineKeyboardMarkup()

	long = InlineKeyboardButton(text=f"long {dbf.count_signal(query.data, 'long',1)}", callback_data="long")
	short = InlineKeyboardButton(text=f"short {dbf.count_signal(query.data, 'short',1)}", callback_data="short")
	back = InlineKeyboardButton(text="Назад", callback_data="back")
	pos.add(short,long)
	pos.add(back)
	if query.data == 'back':
		await state.finish()
		await bot.send_message(query.from_user.id, "временной отрезок (шаг 5минут)", reply_markup=dbf.part_keyboard())
		await UserState.stage.set()
	else:
		await bot.send_message(query.from_user.id, query.data, reply_markup=pos)
		await UserState.coin.set()


@dp.callback_query_handler(state=UserState.coin )
async def select_types(query: types.CallbackQuery,  state: FSMContext):
	await state.update_data(typer=query.data)
	x = await state.get_data()
	lis = []
	print(x['typer'])
	y = dbf.select_coins_over_categories(x['coin'], x['typer'],x["stage"])

	if y != "ПУСТО :((":
		for row in y:
			print(str(row[2]) + str(x['stage']))
			if str(row[2]) == str(x['stage']):
				print(str(row[2]) + str(x['stage']))
				lis.append(row[0])
				lis.append("===============================================")
	else:
		lis.append("ПУСТО :((")


	await bot.send_message(query.from_user.id, lis)
	await state.finish()
	await bot.send_message(query.from_user.id, "временной отрезок (шаг 5минут)", reply_markup=dbf.part_keyboard())
	await UserState.stage.set()









if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)





