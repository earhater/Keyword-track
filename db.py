import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
class Database:
    def __init__(self, dbf):
        self.connection = sqlite3.connect(dbf)
        self.cursor = self.connection.cursor()

    async def add_signal(self, coin, msg, position, date,sent,):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'main' ('coin', 'msg','pos','hour','sent',) VALUES (?,?,?,?,?,)",
                                       (coin, msg.replace("\n", " "), position,date,sent))

    def select_coins_over_categories(self, key, typer, sent):
        with self.connection:
            if typer != 0:

                result = self.cursor.execute("SELECT msg,hour,sent,coin,pos FROM main WHERE coin=? AND pos=?", (key, typer)).fetchall()

                if result != None and result != [] :

                    return result
                else:
                    return "ПУСТО :(("
            else:
                result = self.cursor.execute("SELECT * FROM main").fetchall()

                if result != None and result != [] :
                    return result
                else:
                    return False

    def clr_table(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM main")



    def part_keyboard(self):

        with self.connection:
            c = self.cursor.execute("SELECT DISTINCT sent from main")
        coins = c.fetchall()
        keyboard = InlineKeyboardMarkup()
        row1, row2 = [], []

        for i in range(len(coins)):
            if i < len(coins) // 2:
                row1.append(
                    InlineKeyboardButton(text=f"{coins[i][0]}", callback_data=f"{coins[i][0]}"))
            else:
                row2.append(
                    InlineKeyboardButton(text=f"{coins[i][0]}", callback_data=f"{coins[i][0]}"))

        keyboard.row(*row1)
        keyboard.row(*row2)

        return keyboard

    def get_totalSignals(self,coin, sent):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(coin) FROM main WHERE coin=? AND sent=?", (coin,int(sent),)).fetchall()

    def gpt(self,sent):







        c = self.cursor.execute("SELECT coin, COUNT(*)  FROM main WHERE sent=? AND pos!='false' GROUP BY coin ORDER BY COUNT(*) DESC", (int(sent),))
        coins = c.fetchall()

        keyboard = InlineKeyboardMarkup()
        for coin in coins:
            button_text = f"{coin[0]} ({coin[1]})"
            button = InlineKeyboardButton(text=button_text, callback_data=coin[0])
            keyboard.add(button)

        return keyboard
    def count_signal(self, coin,type,sent):
        with self.connection:
            toret = []
            print(f"{coin} {type}")
            return self.cursor.execute("SELECT COUNT(*) FROM main WHERE coin=? AND pos=? AND sent=?", (coin,type,sent)).fetchall()
