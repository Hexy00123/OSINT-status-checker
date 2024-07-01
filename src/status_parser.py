from telethon import TelegramClient
import asyncio
from dotenv import dotenv_values
from time import time

ENV_RELATIVE_PATH = 

class Parser(object):
    def __init__(self, api_id, api_hash, chat_ids, request_delay=0.5):
        self.chat_ids = chat_ids
        self.client = TelegramClient('session', api_id, api_hash)
        self.request_delay = request_delay

    async def get_usernames(self):
        async with self.client:
            users = await self.client.get_participants(entity=chat_ids[0])
            usernames = [f'@{user.username}' for user in users]
            return usernames

    async def get_user_data(self, user):
        return await self.client.get_entity(user)

    async def parse(self):
        async with self.client:
            usernames = await self.get_usernames()

            s = time()

            user_data = await asyncio.gather(*[self.get_user_data(user) for user in usernames])

            e = time()

            print(e - s)


if __name__ == '__main__':
    env = dotenv_values('../.env')

    api_id = env['api_id']
    api_hash = env['api_hash']
    chat_ids = eval(env['chat_ids'])

    parser = Parser(api_id, api_hash, chat_ids)

    asyncio.run(parser.parse())
