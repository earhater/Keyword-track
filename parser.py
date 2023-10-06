import configparser

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from Exters import Managers
from db import Database
from list import x as keylist
import time
config = configparser.ConfigParser()
config.read("config.ini")
client = TelegramClient(config['Telegram']['username'], int(config['Telegram']['api_id']),
                        config['Telegram']['api_hash'])

client.start()
dbf = Database("./base.db")
mng = Managers()


async def valuener(target, listy, date,cc):
    for turple in listy:

        if len(turple) > 1:  # фильтруем пробелы
            x = turple in target  # есть ли монеты
            y = await mng.GetInWord(["Stop", "STOP", "СТОП", "стоп"], target)

            if x and y:  # проверяем
                print("sent")
                await dbf.add_signal(turple, target, await mng.TypeManager(target), date,cc)
                break

async def main_use(cc):
    async for dialog in client.iter_dialogs():
        try:
            channel = await client.get_entity(dialog.id)
            all_messages = []  # список всех сообщений
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=0,
                offset_date=None, add_offset=0,
                limit=50, max_id=0, min_id=0,
                hash=0))
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())


            for i in all_messages:
                heh = keylist.split('\n')

                await valuener(i["message"], heh,i['date'], cc)

        except Exception as e:
            print(e)
            pass
    print("Parsing executing stage finished!")

async def main(cc):
    await main_use(cc)


async def PartParser():
    cc = 0
    while cc != 10:
        with client:
            client.loop.run_until_complete(main())
        cc += 1
    print(cc)



while True:
    cc = 1
    while cc != 10:
        with client:
            client.loop.run_until_complete(main(cc))
        cc += 1
        print(cc)
        time.sleep(1)
    dbf.clr_table()
    print("Sucscess")
