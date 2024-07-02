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

    assert not set(fields.keys()).difference(
        {'id', 'username'}), 'fields must have either `id` or `username`'

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
    data = '''
1060980276 Kypban_M
714469639 Nika_Teen
874710843 hedgefo9
242506828 a_rymsh
116847835 d3pre5s
472209097 saprykinzxc
584923809 dbrkv
624396776 somebodyoncetldme
398291221 XoTTaB_FEFU
5112869599 ydmubhnqlt
1328906598 dmhd6219
816288709 chuprakova_s
768378675 ArtMGreen
348215185 ArtemBeresnev
1062302151 NTGtpl
353729601 free_birb
813772333 polarnighty
832064720 Kalanod
504063699 all_lyuk
385651422 rattysed
950903717 ruslan_o_clock
474268454 bumerang_2002
856115257 alinarhi
922037409 VScdr
869175467 SerSemyon
254642858 Noyesy
786133828 AnnaParulava
270901888 xantMEs
735735897 LTDigor
883204715 mayatin
576242505 eugengold
5417820497 DJGVan
1059025803 Kopololo
495674371 pravietis13
1100137873 mangocandle
896690360 Kris_Di2
894762751 KotDimos
472220668 Sergey140146659
908239984 angelika782345
709067322 strange_creator
906627313 ivanvet31
1103638534 dikiydinozavrik
260169909 unrlight
5610718700 Alnik_main
1053480782 waldemarspev
1055951940 HeavenBreaker
837968643 just_c1own
1819382 n0str
1114622938 Maxgum
421693192 matthew_nekirov
1771605793 SideArket
1147185372 Confffetti
1179217992 r0ntet
1301004601 llirikh
739596935 QzeaQ
1572576417 aiserov
182848386 sh4grath
470414515 eronary
255282233 necentt
575498549 eugen_iv
820044741 GR4NDS0N162
726948626 sofa0m
569508334 v_oxel
406626750 lordwhy
948448546 krokodidla
947015140 kks02
461929482 dear_cheap
295354694 pnqke
1127658763 Slaves2288
1269919601 Gr1shania
350811144 yorxx
509837572 Michael_kab
746890692 Vadim_tynyanov
608882946 Nooth1ng
540243534 sfnurkaev
1012818905 op1alex
1875499689 PetrAhtimirov
894194983 DimPerch
1220563746 echo100
698428475 elanchao
325329939 skymefactor
123007986 sergeyparamoshkin
401015471 ocelot432
901211804 VladArche
1561693542 kilka_bez_hvosta
1922747693 che_bu_rek1
1067405597 yutory
1016268936 nosnic
366840995 catssme
434888843 introvertess
702644841 maryshca
433787687 dmitriykutcenko
1022354872 Said_magnat
674249340 hatka_bobrikov
1188099800 fefemf10
1052500389 dmtandivanson
311695878 izvinistb
981309471 tNabuki
644731352 polar_jabka
605007653 fleshrazer
193304673 sm1rk
487507300 all_ko
1019384270 Ekats3529
326525586 Rustikhak
490845126 va_vak
463929963 spxps
349781736 kidavspb
489002991 dmitriienin
825916003 frog_plus_plus
1020966030 Katalinaaaaaaa
557765162 nikaov7
1826432277 ananasovoe_bezumstvo
1854599443 dmitrievamarina
228319424 kaaamoon
585148553 gosh_rivgosh
1028003717 uu060k
'''
    # return [int(i.split()[0]) for i in data.split('\n')]
    return [193304673]


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
        username = (await client.get_users(user_ids)).username
        await app.send_message("me", f"@{username}")

        # data = await parse_user_statuses(app, user_ids)
        print('\n'.join(str(user) for user in data))

        e = time()

        print(e - s)


if __name__ == '__main__':
    env = dotenv_values('../../.env')
    api_id = env['api_id']
    api_hash = env['api_hash']

    asyncio.run(main(api_id, api_hash))
