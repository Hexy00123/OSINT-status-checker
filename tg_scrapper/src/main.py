from pyrogram import Client
from pyrogram.enums import UserStatus
from dotenv import dotenv_values
import asyncio
from time import time


async def parse_chat(client, chat_id: int, fields=None):
    """
    Usage:
    for user_data in await parse_chat(app, -1002197489255):
        print(user_data)
    """

    if fields is None:
        fields = {
            'id': True,
            'username': True,
        }

    assert not set(fields.keys()).difference({'id', 'username'}), 'fields must have either `id` or `username`'

    if 'id' not in fields:
        fields['id'] = False
    if 'username' not in fields:
        fields['username'] = False

    assert chat_id < 0, 'chat_ids must be negative'
    assert isinstance(fields['id'], bool), 'Fields type must be bool'
    assert isinstance(fields['username'], bool), 'Fields type must be bool'

    users_data = []

    async for user in client.get_chat_members(chat_id):
        user = user.user
        if len(fields) == 2:
            users_data.append({
                'id': user.id,
                'username': user.username,
            })
        elif 'username' in fields:
            users_data.append({
                'username': user.username,
            })
        else:
            users_data.append({
                'id': user.id,
            })
    return users_data


def get_user_ids() -> list[int]:
    data = '''users'''
    return [int(i.split()[0]) for i in data.split('\n')]


async def parse_user_statuses(client, user_ids: list[int]) -> list[dict[int: bool]]:
    """
    Usage:
    await parse_user_statuses(app, user_ids)
    """
    users = await client.get_users(user_ids)
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'status': user.status is UserStatus.ONLINE,
        })
    return users_data


async def main(api_id, api_hash):
    user_ids = get_user_ids()

    async with Client("my_account", api_id, api_hash) as app:
        s = time()

        data = await parse_user_statuses(app, user_ids)
        print('\n'.join(str(user) for user in data))

        e = time()

        print(e - s)


if __name__ == '__main__':
    env = dotenv_values('../../.env')
    api_id = env['api_id']
    api_hash = env['api_hash']

    asyncio.run(main(api_id, api_hash))
