from pyrogram import Client
from pyrogram.enums import UserStatus
from dotenv import dotenv_values
import asyncio
from time import time, sleep
from datetime import datetime


class Parser(object):
    def __init__(self, api_id, api_hash):
        self.client = Client("my_account", api_id, api_hash)
        self.user_ids = ['@Nooth1ng', '@sm1rk', '@fleshrazer', '@kks02', '@Alcor2026']

    async def parse_user_statuses(self, client, user_ids: list[int | str]) -> list[dict[int: bool]]:
        """
        Usage:
        await parse_user_statuses(app, user_ids)
        """
        users = await client.get_users(user_ids)
        users_data = []
        for user in users:
            users_data.append({
                'ts': str(datetime.now()),
                'user': {
                    'id': user.id,
                    'collection': 'User',
                },
                'is_online': user.status is UserStatus.ONLINE,
            })

        return users_data

    async def parse(self):
        async with self.client as app:
            data = await self.parse_user_statuses(app, self.user_ids)
            print('\n'.join(str(user) for user in data))


async def main(dotenv_path='../../.env'):
    env = dotenv_values(dotenv_path)
    api_id = env['api_id']
    api_hash = env['api_hash']
    parser = Parser(api_id, api_hash)
    await parser.parse()


if __name__ == '__main__':
    asyncio.run(main())
