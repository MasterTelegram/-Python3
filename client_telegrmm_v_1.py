
print ('[+] Старт программы чтения каталога')
import iz_func
import telebot

# Remember to use your own values from my.telegram.org!
api_id       = 192804
api_hash     = '1b40d1d01f8922b384d44e29d32f6acf'
phone_number = '+79033671563'   # Купинов Вадим
#phone_number = '+79058839468'   # Юля 
print ('    [+] Пользователь:',phone_number)

namebot = "@Help_client_bot" 
token,about = iz_func.get_token (namebot)
bot   = telebot.TeleBot(token) 
user_id = '399838806'
namebot = 'web' 

def send_message_bot (message_out,catalog):
    import telebot  
    namebot = "@Help_client_bot" 
    token,about = iz_func.get_token (namebot)
    bot   = telebot.TeleBot(token)    
    #user_id = '399838806'
    #catalog = -1001262596993 
    bot.send_message(catalog,message_out,parse_mode='HTML',disable_web_page_preview = True)

def send_new_message (message,catalog,chat_title,chat_username,chat_id,find_w,sender_username):
    print ('[1]')
    message_out = ''
    message_out = message_out + '🤵 <b>Новое сообщение</b> от @' +str(sender_username) +'\n'
    message_out = message_out + '⭐ <i>'+str(find_w)+'</i>' + '\n'    
    message_out = message_out + '' + '\n'
    message_out = message_out + message + '\n'
    message_out = message_out + '' + '\n'
    message_out = message_out + 'Сообщение: https://t.me/'+chat_username +'/'+str(chat_id)+ '\n'
    message_out = message_out + 'Описание : ' +chat_title   + '\n'
    bot.send_message(catalog,message_out,parse_mode='HTML',disable_web_page_preview = True)

def load_key (namebot,user_id):
    list_key = []
    db,cursor = iz_func.connect (namebot)
    sql = "select id,key_name from tel_key where namebot = '{}' and user_id = '{}'".format(namebot,user_id);
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,key_name = row
        list_key.append(key_name)
    return list_key   

def find_key (mess,list_key):
    find = ''
    label = 'не найден'
    for line in list_key:
        if mess.upper().find(line.upper()) != -1:
            label = 'найден'
            find = find + " " +line
            print ('        [+]',line)
    return label,find    

def select_word (mess,word):
    mess = mess.replace(str(word),'<b>'+str(word)+'</b>')
    mess = '==>'+mess 
    return mess

def list_send_grup (user_id):
    db,cursor = iz_func.connect (namebot)
    sql = "SELECT id,receiver_id,sender_id FROM tel_resend where user_id = "+str(user_id)+""    
    cursor.execute(sql)
    data = cursor.fetchall()
    list_grup = []
    for rec in data: 
        id,receiver_id,sender_id = rec
        list_grup.append([receiver_id,sender_id])
    return list_grup

def get_user_send ():
    import time
    db,cursor   = iz_func.connect (namebot)
    timestamp = int(time.time())
    sql = "select DISTINCT user_id from secret_key where  user_id <> '' and begin_t  < "+str(timestamp)+" and end_t > "+str(timestamp)+" ORDER BY begin_t DESC "
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []
    for rec in data: 
        user_id = rec[0]
        list.append(user_id)
    return list   

 
#<b>bold</b>, <strong>bold</strong>
#<i>italic</i>, <em>italic</em>
#<a href="URL">inline URL</a>
#<code>inline fixed-width code</code>
#<pre>pre-formatted fixed-width code block</pre>

###############################  Отправляем сообщение информационному боту ######################
catalog = user_id   
message_out = ''
message_out = message_out + '🙋 <b>Информация</b>'+'\n'
message_out = message_out + ''+'\n'
message_out = message_out + 'Старт программы: <i>Читаем группы</i>'+'\n'
message_out = message_out + ''+'\n'
message_out = message_out + '<code>Создать телеграмм бота: </code>'
message_out = message_out + '<a href="www.3dot14.ru">Наш сайт</a>'+'\n'
send_message_bot (message_out,catalog)  
#################################################################################################


list_key  = load_key (namebot,user_id)
list_grup = list_send_grup (user_id)

from telethon import TelegramClient, events
session = 'session_{}.load_catalog_№2'.format(phone_number)
client = TelegramClient(session,api_id=192804,api_hash=api_hash)
@client.on(events.NewMessage)
async def my_event_handler(event):
    print ('[+] Сообщение:',event.id)    
    try:
        sender_id_user    = ''
        sender       = await event.get_sender()
        sender_id_user    = sender.id
    except Exception as e:    
        print ('    [+] error send message',e)   
        pass     
    try:
        sender_username = ''
        sender_username = sender.username
    except Exception as e:    
        print ('    [+] error send message',e)     
        pass   
    try:
        sender_phone = ''   
        sender_phone = sender.phone 
    except Exception as e:    
        print ('    [+] error send message',e)        
        pass
    print ('    [+] sender id:',sender_id_user,', phone:',sender_phone,',username',sender_username)
    try:
        raw_text     = ''
        raw_text     = event.raw_text
    except Exception as e:    
        print ('    [+] error send message',e)
        pass
    print ('    [+] text:',raw_text[0:120].replace('\n',''))
    try:
        chat         = ''
        chat_id      = ''
        chat_title   = ''
        chat_username = ''
        chat         = await event.get_chat ()
        chat_id      = event.chat_id
        chat_title   = chat.title
        chat_username = chat.username        
    except Exception as e:    
        print ('    [+] error send message',e)
        pass
    print ('    [+] chat   id:',chat_id,  ', title:',chat_title)


    
    ########################################################## Поиск слова в тексте ################################################################
    if phone_number == '+79033671563':
        label_find,find_w = find_key (raw_text,list_key) 
        if label_find == "найден":
            print ('        [+] Наденые слова:{}'.format(find_w))
            #if 'а' in raw_text:        
            if chat_id != -1001262596993 and chat_id != 518663502:
                print ('        [+] Отправка сообщения')
                message_out = select_word (raw_text,str(find_w))
                await send_new_message (message_out,-1001262596993,chat_title,chat_username,event.id,find_w,sender_username)
    else:
        pass            
    #################################################################################################################################################





    ######################################################## Пересылка сообщения в бота ###########################################################
    if phone_number == '+79033671563':
        message_in = event.message
        namebot = "@bb_cf_bot"
        #for grup in list_grup:
        #    receiver_id,sender_id = grup
        if int(chat_id) == int('-1001338061911') or int(chat_id) == int('-1001491230343') :   ### Группа исходник тестовый 1С Криптобиржа
        #if int(chat_id) == int('1274206412'):
            print ('        [+] Проверка на переадресацию. Берем из группы:',chat_id,", Отправляем в боту:",namebot)            
            token = '1162451457:AAE2GGLzsWh2UXjHTn_CUayEyrWfpoFv60s'
            bot   = telebot.TeleBot(token)
            
            message_out = raw_text
            users = get_user_send ()
            print ('[+]-1------------------------------------------------------------------------------------------------')
            print ('[+]',users)            
            for user in users:
                user_id = user
                try:
                    send_answer = iz_func.bot_send (user_id,message_out,'',bot,namebot)
                    print ('    [+] Отправка',user_id,send_answer)
                except:
                    pass    
            print ('[+]-2-----------------------------------------------------------------------------------------------')
            user_id     = '399838806'
            bot.send_message(user_id,message_out,parse_mode='HTML')
            print ('[+] Моя отправка -->')
            print ('[+]-3-----------------------------------------------------------------------------------------------')
        #        #catalog = int(receiver_id)       ### Группа получатель
        #        #await client.send_message(catalog,message_in)
    else:
        pass            
    #################################################################################################################################################







    ######################################################## Пересылка сообщения в группу ###########################################################
    if phone_number == '+79033671563':
        message_in = event.message
        for grup in list_grup:
            receiver_id,sender_id = grup
            if int(chat_id) == int(sender_id):   ### Группа исходник тестовый 1С Криптобиржа
                print ('        [+] Проверка на переадресацию. Берем из группы:',sender_id,", Отправляем в группу:",receiver_id)
                catalog = int(receiver_id)       ### Группа получатель
                await client.send_message(catalog,message_in)
    else:
        pass            
    #################################################################################################################################################





    ###################################################### Поиск контакта и отправка сообщения ######################################################
    if phone_number == '+79033671563':
        db,cursor = iz_func.connect (namebot)
        try:
            label = 'No' 
            sql = "select id,sender_name from tel_sender where sender_name = '"+str(sender_username)+"' limit 1"
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                label = 'Yes' 

            if label == 'No':
                sql = "INSERT INTO tel_sender (`sender_name`,`sender_id`,`sender_phone`,`chat_title`) VALUES ('{}','{}','{}','{}')".format (sender_username,sender_id_user,sender_phone,chat_title)
                cursor.execute(sql)
                db.commit() 
        except Exception as e:    
            print ('    [+] error send message',e)            
    #################################################################################################################################################    





    ############################################################ Стандартные ответы чата ############################################################
    if phone_number == '+79033671563':
        if 'Привет' in raw_text:
            await event.reply('Добрый день !')
    else:
        pass        
    #################################################################################################################################################


client.start()
client.run_until_disconnected()
