import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Ваш токен доступа
TOKEN = 'YOUR_ACCESS_TOKEN'

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, 'YOUR_GROUP_ID')
vk = vk_session.get_api()

# Список пользователей, сообщения которых будут удаляться
users_to_delete = ['USER_ID_1', 'USER_ID_2']

# Список запрещенных слов
banned_words = ['banword1', 'banword2']

def delete_messages_from_user(user_id, chat_id):
    messages = vk.messages.getHistory(peer_id=chat_id, count=200)['items']
    for message in messages:
        if message['from_id'] == user_id:
            vk.messages.delete(message_ids=message['id'], delete_for_all=True)

def contains_banned_words(text):
    for word in banned_words:
        if word in text:
            return True
    return False

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        chat_id = event.object.message['peer_id']
        user_id = event.object.message['from_id']
        message_text = event.object.message['text'].lower()
        
        # Проверка на наличие пользователя в списке и наличие запрещенных слов
        if user_id in users_to_delete or contains_banned_words(message_text):
            vk.messages.delete(message_ids=event.object.message['id'], delete_for_all=True)
