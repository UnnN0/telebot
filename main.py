import telebot
from telebot import types
from config import TOKEN, announcement_channel, chat_id, text570, text_katok

chat_id = announcement_channel

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    #Меню с кнопками
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="Подать заявку", callback_data="req")
    button2 = telebot.types.InlineKeyboardButton(text="Авторизация", callback_data="auth")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Добро пожаловать, это бот по приему заявок компании "Ресур Плюс"\nВыберите действие кнопками ниже.\nАвторизация доступна только сотрудникам компании.', reply_markup=keyboard)

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "auth":
        bot.send_message(call.message.chat.id, 'Введите пароль для авторизации')
    elif call.data == "req":
        bot.send_message(call.message.chat.id, "Для оформления заявки введите Ваше имя")
        bot.register_next_step_handler(call.message, ask_phone)
    
    elif call.data == "help":
        keyboard = telebot.types.InlineKeyboardMarkup()
        main = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='back')
        keyboard.add(main)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= 'Список доступных команд:\n/start - открыть главное меню\nОстальное управление происходит путем нажатия на кнопки внутри сообщений бота.', reply_markup=keyboard)
    elif call.data == "auth321":
        bot.send_message(call.message.chat.id, 'Авторизация успешно завершена')

        #Кнопки после кривой авторизации
        keyboard = telebot.types.InlineKeyboardMarkup()
        main = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='back')
        keyboard.add(main)
        
        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=keyboard)
    elif call.data == "version":
        keyboard = telebot.types.InlineKeyboardMarkup()
        main = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='back')
        keyboard.add(main)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Версия бота: 1.0', reply_markup=keyboard)
    elif call.data == "free":
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Case 570ST", callback_data="case570")
        button2 = telebot.types.InlineKeyboardButton(text="Грунтовый каток", callback_data="katok")
        keyboard.add(button1, button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= 'Выберите технику, о наличии которой желаете сообщить.', reply_markup=keyboard)
    elif call.data == "katok":
        with open('image\katok.jpg', 'rb') as photo:
            bot.send_photo(announcement_channel, photo=photo, caption= text570) 
        keyboard = telebot.types.InlineKeyboardMarkup()
        main = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='back')
        keyboard.add(main)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= 'Сообщение отправлено в канал', reply_markup=keyboard)  
    elif call.data == "case570":
        with open('image\Case 570ST.jpg', 'rb') as photo:
            
            bot.send_photo(announcement_channel, photo=photo, caption= text570)
        keyboard = telebot.types.InlineKeyboardMarkup()
        main = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='back')
        keyboard.add(main)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= 'Сообщение отправлено в канал', reply_markup=keyboard)
    elif call.data == 'back':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Помощь", callback_data="help")
        button2 = telebot.types.InlineKeyboardButton(text="Версия", callback_data="version")
        button3 = telebot.types.InlineKeyboardButton(text="Рассылка", callback_data="free")
        keyboard.add(button1, button2, button3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=  'Главное меню', reply_markup=keyboard)
    elif call.data == 'main':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Подать заявку", callback_data="req")
        button2 = telebot.types.InlineKeyboardButton(text="Авторизация", callback_data="auth")
        keyboard.add(button1, button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=  'Добро пожаловать, это бот по приему заявок компании "Ресур Плюс"\nВыберите действие кнопками ниже.\nМодерация доступна только сотрудникам компании.', reply_markup=keyboard)
       



    #Обработка кнопок статуса заявок
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == "active":
        new_keyboard = types.InlineKeyboardMarkup()
        button_active = types.InlineKeyboardButton(text="Статус: Активно⌛", callback_data="active_status")
        button_done = types.InlineKeyboardButton(text="Выполнено", callback_data="done")
        new_keyboard.row(button_active, button_done)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=new_keyboard)
        bot.answer_callback_query(callback_query_id=call.id, text="Заявка активна")
    elif call.data == "done":
        new_keyboard = types.InlineKeyboardMarkup()
        button_done = types.InlineKeyboardButton(text="Статус: Выполнено✅", callback_data="done_status")
        new_keyboard.row(button_done)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=new_keyboard)
        bot.answer_callback_query(callback_query_id=call.id, text="Заявка выполнена")
def ask_phone(message): #Запрос номера\текста
    name = message.text
    bot.send_message(message.chat.id, "Введите Ваш номер телефона:")
    bot.register_next_step_handler(message, ask_free_text, name)
def ask_free_text(message, name):
    phone = message.text
    # Создание пользовательской клавиатуры с одной кнопкой
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton(text="Оставить поле пустым")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Введите текст заявки, он может быть произвольным. Либо нажмите на кнопку 'Оставить поле пустым'", reply_markup=keyboard)
    bot.register_next_step_handler(message, send_to_channel, name, phone )
def send_to_channel(message, name, phone):
    if message.text == "Оставить поле пустым":
        text = "Не указано"
    else:
        text = message.text

 
    keyboard = types.InlineKeyboardMarkup()
    button_active = types.InlineKeyboardButton(text="Активно", callback_data="active")
    button_done = types.InlineKeyboardButton(text="Выполнено", callback_data="done")
    keyboard.row(button_active, button_done)

    bot.send_message(announcement_channel, 
                     text=f"Поступила новая заявка!\n\nИмя: {name} \nНомер телефона: {phone} \nТекст заявки: {text}",
                     reply_markup=keyboard)
    keyboard = telebot.types.InlineKeyboardMarkup()
    main = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='main')
    keyboard.add(main)
    bot.send_message(message.chat.id,"Заявка отправлена! Спасибо за обращение, ожидайте звонка.", reply_markup=keyboard)
@bot.message_handler(func=lambda message: True)
def message(message):
    # Проверяем, является ли сообщение запросом пароля на авторизацию
    if message.text == "321":
        bot.send_message(message.chat.id, 'Авторизация успешно завершена')
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Помощь", callback_data="help")
        button2 = telebot.types.InlineKeyboardButton(text="Версия", callback_data="version")
        button3 = telebot.types.InlineKeyboardButton(text="Рассылка", callback_data="free")
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=keyboard)
        


bot.polling()