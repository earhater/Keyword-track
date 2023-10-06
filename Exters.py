from db import Database
import datetime
dbf = Database("./base.db")
'''
#тут все просто. Гет** - проверка слова на вхождение. манагер просто собирает о объеденяет все.
# валуенер фильтрует на сигнал и собирает в бдшку. логика простейшая, и понять ее легко, по этому тут особо без комментов
'''

class Managers:
    async def GetInWord(self, listy, word):
        for i in listy:
            z = i in word
            if z:
                return True
                break

    async def GetShort(self, word):
        listy = ['short', 'SHORT', 'шорт', "Шорт", "ШОРТ", "Short", '(SHORT)', "(Short)", "SHORT"]
        for i in listy:
            x = i in word

            if x:
                return True
                break

    async def GetLong(self, word):
        listy = ['long', 'LONG', 'лонг', "Лонг", "ЛОНГ", "Long", '(LONG)', "(Long)", "LONG"]
        for i in listy:
            x = i in word

            if x:
                return True
                break

    async def TypeManager(self, word):
        long = await self.GetLong(word)
        short = await self.GetShort(word)

        if long:
            return "long"
        elif short:
            return "short"
        else:
            return "false"


