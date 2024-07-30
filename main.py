import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Ваш токен доступа
TOKEN = 'YOUR_ACCESS_TOKEN'

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, 'YOUR_GROUP_ID')
vk = vk_session.get_api()

def delete_messages_from_user(user_id, chat_id):
    messages = vk.messages.getHistory(peer_id=chat_id, count=200)['items']
    for message in messages:
        if message['from_id'] == user_id:
            vk.messages.delete(message_ids=message['id'], delete_for_all=True)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        chat_id = event.object.message['peer_id']
        user_id = event.object.message['from_id']
        # Если пользователь, чьи сообщения нужно удалять, написал сообщение
        if user_id == 'ID_USER_TO_DELETE_MESSAGES':
            delete_messages_from_user(user_id, chat_id)
