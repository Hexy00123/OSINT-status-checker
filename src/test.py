from telethon import TelegramClient
import asyncio
from dotenv import dotenv_values
from time import time

env = dotenv_values('../.env')
api_id = env['api_id']
api_hash = env['api_hash']
chat_ids = eval(env['chat_ids'])
client = TelegramClient('session', api_id, api_hash)

# Add a delay between requests to avoid rate limits
REQUEST_DELAY = 0.5


async def get_user_data(user):
    await asyncio.sleep(REQUEST_DELAY)
    return await client.get_entity(user)


async def main():
    async with client:
        users = await client.get_participants(entity=chat_ids[0])
        usernames = [f'@{user.username}' for user in users]

        while True:
            start = time()
            users_data = await asyncio.gather(*[get_user_data(user) for user in usernames])
            end = time()
            print(end - start)


if __name__ == '__main__':
    asyncio.run(main())
