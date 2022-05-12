from aiogram import types, Dispatcher
from create import dp, bot
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

global CHANNEL_ID
CHANNEL_ID = 511151694

class FSMClient(StatesGroup):
	model = State()
	color = State()
	male_female = State()
	size = State()
	photo = State()
	contact = State()
	# user_id = State()


# Start
async def cm_start(message : types.Message):
	await bot.send_message(message.from_user.id, 'Добро пожаловать!\
		\nБот от команды Vastl поможет вам создать футболку с Вашим уникальным дизайном.\
		\nПройдите небольшой опрос для формирования заказа', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Купить футболку')))
	

# Start buy
async def start_buy(message : types.Message):
	await FSMClient.model.set()
	await bot.send_message(message.from_user.id, 'Выберите модель футболки', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('1 - Classic'), KeyboardButton('2 - Oversize')).add(KeyboardButton('Отменить заказ')))
	await bot.send_photo(message.from_user.id, open("C:/Users/tihom/Desktop/PROJECTS/TSHIRT_BOT/all.jpg", 'rb'))


# Choose model
async def choose_model(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['model'] = message.text
		if data['model'] == '2 - Oversize':
			data['model'] == 'Oversize'
			await bot.send_message(message.from_user.id, 'Выберите цвет', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Белый'), KeyboardButton('Черный')).add(KeyboardButton('Отменить заказ')))
			await bot.send_photo(message.from_user.id, open("C:/Users/tihom/Desktop/PROJECTS/TSHIRT_BOT/claassic.jpg", 'rb'))


		elif data['model'] == '1 - Classic':
			data['model'] == 'Classic'
			await bot.send_message(message.from_user.id, 'Выберите цвет', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Белый'), KeyboardButton('Черный')).add(KeyboardButton('Отменить заказ')))
			await bot.send_photo(message.from_user.id, open("C:/Users/tihom/Desktop/PROJECTS/TSHIRT_BOT/oversize.jpg", 'rb'))


	await FSMClient.next()


# Choose color oversize
async def choose_color_oversize(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['color'] = message.text
		await FSMClient.next()
		await message.answer('Выберите пол', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Мужской'), KeyboardButton('Женский')).add(KeyboardButton('Отменить заказ')))


# Choose male\female
async def choose_male_female(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['male_female'] = message.text
	await FSMClient.next()
	await message.answer('Выберите размер', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(KeyboardButton('S'), KeyboardButton('M'), KeyboardButton('L')).add(KeyboardButton('Отменить заказ')))
	

# Choose size
async def choose_size(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['size'] = message.text
	await FSMClient.next()
	await message.answer('Прикрепите фото рисунка, который хотите вышить')

async def send_photo(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['photo'] = message.photo[0].file_id
	await FSMClient.next()
	await message.answer('Оставьте свои контакты Telegram, чтобы мы могли связаться с Вами')

async def get_contact(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['contact'] = str(message.text)
	await state.finish()
	try:
		await bot.send_photo(CHANNEL_ID, data['photo'], f"НОВЫЙ ЗАКАЗ\
													\nМодель футболки - {data['model']}\
													\nЦвет - {data['color']}\
													\nПол - {data['male_female']}\
													\nРазмер - {data['size']}\
													\nКонтакты - {data['contact']}")
		await bot.send_message(message.from_user.id, f"Ваш заказ успешно создан!\nМодель футболки - {data['model']}\
													\nЦвет - {data['color']}\
													\nПол - {data['male_female']}\
													\nРазмер - {data['size']}\
													\n\nОжидайте... Наш дизайнер свяжется с Вами в ближайшее время!", reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Купить футболку')))
	except:
		await bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте еще раз')


# Cancel
async def cancel_handler(message : types.Message, state:FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await bot.send_message(message.from_user.id, 'Заказ успешно отменён!\
		\nЖдём Вас снова\
		\nБот от команды Vastl поможет вам создать футболку с Вашим уникальным дизайном.\
		\nПройдите небольшой опрос для формирования заказа', reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Купить футболку')))




def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(cm_start, commands = ['start'], state = None)
	dp.register_message_handler(cancel_handler, state="*", text = 'Отменить заказ')
	dp.register_message_handler(start_buy, text = 'Купить футболку')
	dp.register_message_handler(choose_model, state = FSMClient.model)
	dp.register_message_handler(choose_color_oversize, state = FSMClient.color)
	dp.register_message_handler(choose_male_female, state = FSMClient.male_female)
	dp.register_message_handler(choose_size, state = FSMClient.size)
	dp.register_message_handler(send_photo, content_types = ['photo'], state = FSMClient.photo)
	dp.register_message_handler(get_contact, state = FSMClient.contact)
