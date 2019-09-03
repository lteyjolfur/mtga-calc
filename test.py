from mtga.set_data import all_mtga_cards
from mtga.models.card import Card
from getpass import getuser
import json
from prettytable import PrettyTable
debug = False


class CardOwned:
    card = Card()
    owned = 0


filePath = "C:/Users/" + getuser() + "/AppData/LocalLow/Wizards Of The Coast/MTGA/output_log.txt"
filePos = 0
try:
    log = open(filePath, 'r')
except FileNotFoundError:
    print("error : log not found")
logContents = log.read()


def log_parse_json(start, end):
    collectionStart = logContents.rfind(start)
    collectionStart = logContents.find(')', collectionStart) + 1
    collectionEnd = logContents.find(end + '\n', collectionStart)+1
    if debug:
        print(logContents[collectionStart:collectionEnd])
    collectionParsed = json.loads(logContents[collectionStart:collectionEnd])
    return collectionParsed


deckLists = log_parse_json("<== Deck.GetDeckListsV3(", ']')
collection = log_parse_json("<== PlayerInventory.GetPlayerCardsV3(", '}')


validCards = 0
cardCount = 0
sets = {}
rares = {}
setMaxNumber = {"M19": 280, "M20": 280, "DAR": 270, "GRN": 264, "RIX": 196, "RNA": 264, "WAR": 264, "XLN": 279}


def set_sort(dictionary, card, amount):
    if card.set not in dictionary:
        # print("new set "+card.set)
        dictionary[card.set] = [1, amount]
    else:
        lastValues = dictionary[card.set]
        dictionary[card.set] = [lastValues[0] + 1, lastValues[1] + amount]


def in_booster(card):
    if card.set != "ANA":
        if card.set_number < setMaxNumber[card.set]:
            return True
    return False


playerRares = 0
playerTotalRares = 0
cardList = {}
for key, value in collection.items():
    try:
        tempCard = all_mtga_cards.find_one(key)
        # print(tempCard.card_type)
        if tempCard.rarity != "Basic":
            # print(tempCard.pretty_name + " " + tempCard.set + " x" + str(value) )
            validCards = validCards + 1
            cardCount += value
            set_sort(sets, tempCard, value)
            cardList[key] = value
            if tempCard.rarity == "Rare":
                set_sort(rares, tempCard, value)
                playerRares = playerRares + 1
                playerTotalRares = playerTotalRares + value
    except ValueError as e:
        pass
cards = 0
cardsInSet = {}
raresInSet = {}
mythicsInSet = {}
totalRares = 0
totalMythics = 0
for i in all_mtga_cards.cards:
    if i.collectible is True:
        cards = cards + 1
        if i.rarity != "Basic":
            set_sort(cardsInSet, i, 4)
        if i.set != 'ANA':
            if i.rarity == "Rare" and in_booster(i):
                set_sort(raresInSet, i, 4)
                totalRares = totalRares + 1
            elif i.rarity == "Mythic Rare" and in_booster(i):
                set_sort(mythicsInSet, i, 4)

print("###########################", raresInSet)
print("###########################", mythicsInSet)

cards = cards - 50

# print("Total count = " + str(cards-50))
# print("valid cards = " + str(validCards))
# print(raresInSet)
# print(cardsInSet)
# print(cards)
tableTitles = ['Unique', 'ALL']
tableColumns = [["Owned Cards", "Total Cards", "Percentage"], [validCards, cards, "{0:.0%}".format(validCards / cards)]]
# ,[cardCount,cards * 4,"{0:.0%}".format(cardCount/(cards * 4))]
for keys in sets:
    tableTitles.append(keys)
    # keys[0]
tUnique = PrettyTable()
iterator = 0
for i in tableTitles:
    if i == tableTitles[0] or i == tableTitles[1]:
        pass
    else:
        tableColumns.append([sets[i][0], cardsInSet[i][0], "{0:.0%}".format(sets[i][0] / cardsInSet[i][0])])
    # print(tableColumns[iterator])
    tUnique.add_column(i, tableColumns[iterator])
    iterator = iterator + 1

print(tUnique)

tTotal = PrettyTable()
tableTitles[0] = 'Total'
tableColumns = [["Owned Cards", "Total Cards", "Percentage"],
                [cardCount, cards * 4, "{0:.0%}".format(cardCount / (cards * 4))]]
iterator = 0
for i in tableTitles:
    if i == tableTitles[0] or i == tableTitles[1]:
        pass
    else:
        tableColumns.append([sets[i][1], cardsInSet[i][1], "{0:.0%}".format(sets[i][1] / cardsInSet[i][1])])
    tTotal.add_column(i, tableColumns[iterator])
    iterator = iterator + 1
print(tTotal)

def format_percentage(num):
    return "{0:.0%}".format(num)

def get_percentage(num1, num2):
    return "{0:.0%}".format(num1 / num2)


def make_table(table_name, column1, player_cards, complete_cards, index):
    newTable = PrettyTable()
    tableTitles[0] = table_name
    print(tableTitles)
    _tableColumns = [["Owned Cards", "Total Cards", "Percentage"], column1]
    _iterator = 0
    for i in tableTitles:
        try:
            if i == tableTitles[0] or i == tableTitles[1]:
                pass
            else:
                num1 = player_cards[i][index]
                num2 = complete_cards[i][index]
                _tableColumns.append([num1, num2, get_percentage(num1, num2)])
            #print("flag")
            # print(_tableColumns[_iterator])
            newTable.add_column(i, _tableColumns[_iterator])
        except KeyError as error:
            print(error)
        _iterator = _iterator + 1
    print(newTable)


def make_table_with_title(table_title, column0, column1, dict1, dict2):
    newTable = PrettyTable()
    _tableColumns = [column0, column1]
    _iterator = 0
    for i in table_title:
       # print("iterator is = " + str(_iterator))
        try:
            if i == table_title[0] or i == table_title[1]:
                pass
            else:
                num1 = dict1[i][1]
                num2 = dict2[i][1]
                _tableColumns.append([num1, num2, get_percentage(num1, num2)])
            # print("flag_make")
            #print(_tableColumns)

            # print(_tableColumns[_iterator])
            newTable.add_column(i, _tableColumns[_iterator])
        except KeyError as error:
            print(error)
        _iterator = _iterator + 1
    print(newTable)


tableTitles.remove('ANA')
make_table("Rares Unique", [playerRares, totalRares, get_percentage(playerRares, totalRares)], rares, raresInSet,
           0)
make_table("Rares Total ", [playerTotalRares, totalRares * 4, get_percentage(playerTotalRares, totalRares * 4)], rares,
           raresInSet, 1)
# Gets The wishlist deck
wishList = {}
for i in deckLists:
    if i["name"] == "$WishList":
        # print(i["mainDeck"])
        iterator = 0
        while iterator < len(i["mainDeck"]):
            wishList[str(i["mainDeck"][iterator])] = i["mainDeck"][iterator+1]
            iterator = iterator + 2
# var = input("Press enter to quit")
# print(wishList)
wishListDuds = []
wishCards = 0
for key in wishList:
    if key in cardList:
        if wishList[key] <= cardList[key]:
            wishListDuds.append(key)
        else:
            wishList[key] = wishList[key] - cardList[key]
            wishCards = wishCards + wishList[key]
for i in wishListDuds:
    print(all_mtga_cards.find_one(i))
    wishList.pop(i)
#print(wishList)

wishListSet = {}

playerRareMythics = {}
for key, value in collection.items():
    try:
        tempCard = all_mtga_cards.find_one(key)
        if tempCard.rarity != "Basic":
            # validCards = validCards + 1
            # cardCount += value
            # set_sort(sets, tempCard, value)
            # cardList[key] = value
            if tempCard.rarity == "Rare" or tempCard.rarity == "Mythic Rare" and in_booster(tempCard):
                # playerRares = playerRares + 1
                # playerTotalRares = playerTotalRares + value
                playerRareMythics[tempCard.mtga_id] = value
    except ValueError as e:
        pass

rareMythicsList = {}
for i in all_mtga_cards.cards:
    if i.collectible is True and in_booster(i) is True:
        cards = cards + 1
        if i.set != 'ANA':
            if i.rarity == "Rare" or i.rarity == "Mythic Rare" and in_booster(i):
                rareMythicsList[i.mtga_id] = 4

print(rareMythicsList)


class CCardListData:

    def set_arrange(self,card,dictionary, amount):
        if card.set not in dictionary:
            dictionary[card.set] = amount
        else:
            dictionary[card.set] = dictionary[card.set] + amount

    def sort_data(self):
        for i in self.wishList:
            card = all_mtga_cards.find_one(i)
            if card.rarity == "Rare":
                self.rares = self.rares + self.wishList[i]
                self.set_arrange(card, self.raresDict, self.wishList[i])
            elif card.rarity == "Mythic Rare":
                self.mythics = self.mythics + self.wishList[i]
                self.set_arrange(card, self.mythicsDict, self.wishList[i])

    def __init__(self, wish_list):
        self.raresDict = {}
        self.mythicsDict = {}
        self.rares = 0
        self.mythics = 0
        self.wishList = wish_list
        self.sort_data()


WishListData = CCardListData(wishList)
CardData = CCardListData(rareMythicsList)
PlayerCardData = CCardListData(playerRareMythics)

for i in rareMythicsList:
    if i in playerRareMythics:
        rareMythicsList[i] = rareMythicsList[i] - playerRareMythics[i]

MissingCardData = CCardListData(rareMythicsList)




print("################################################")
print(WishListData.raresDict)
print(CardData.raresDict)



for i in wishList:
    set_sort(wishListSet, all_mtga_cards.find_one(i), wishList[i])
    card = all_mtga_cards.find_one(i)

#print(wishListSet)
tableTitlesRares = ["Rare Boosters", "All"]
tableTitlesWish = []
for i in tableTitles:
    if i in wishListSet:
        tableTitlesRares.append(i)
        tableTitlesWish.append(i)



#print(tableTitles)
#print(tableTitlesRares)
missingRaresSet = {}
for i in wishListSet:
    missingRaresSet[i] = [0, raresInSet[i][1] - rares[i][1]]
missingRares = totalRares * 4 - playerTotalRares
col0 = ["Wanted", "Total missing", "Percentage"]
col1 = [wishCards, missingRares, get_percentage(wishCards, missingRares)]
make_table_with_title(tableTitlesRares, col0, col1, wishListSet, missingRaresSet)


class Column:

    def __init__(self, _title, _wanted_rares, _total_rares, _wanted_mythics, _total_mythics):
        self.title = _title
        self.wantedRares = _wanted_rares
        self.totalRares = _total_rares
        self.wantedMythics = _wanted_mythics
        self.totalMythics = _total_mythics
        self.percentage = 0
        try:
            self.percentage = format_percentage((_wanted_rares/_total_rares)*0.88
                                                + (_wanted_mythics/_total_mythics) * 0.12)
        except TypeError:
            pass


    def get_title(self):
        return self.title

    def get_column(self):
        return[self.wantedRares, self.totalRares, self.wantedMythics, self.totalMythics, self.percentage]


class Table:
    table = PrettyTable()
    TitleColumn = Column("Booster %", "Wanted Rares", "Missing Rares", "Wanted Mythics",  "Missing Mythics")
    TitleColumn.percentage = "Percent"
    TotalColumn = Column("All", wishCards, missingRares, "Inserted Later", "Inserted Later")
    SetColumns = []
    prepared = False

    def __init__(self, set_list, wish_list_data, missing_data):
        #print(set_list)
        for i in set_list:
            self.SetColumns.append(Column(i, wish_list_data.raresDict[i], missing_data.raresDict[i],
                                          wish_list_data.mythicsDict[i], missing_data.mythicsDict[i]))
        self.TotalColumn.mythics = wish_list_data.mythics
        self.TotalColumn.wantedMythics = wish_list_data.mythics
        self.TotalColumn.totalMythics = missing_data.mythics

    def prepare_table(self):
        if not self.prepared:
            self.prepared = True
            self.table.add_column(self.TitleColumn.get_title(), self.TitleColumn.get_column())
            self.table.add_column(self.TotalColumn.get_title(), self.TotalColumn.get_column())
            iterator = 0
            while iterator < len(self.SetColumns):
                self.table.add_column(self.SetColumns[iterator].get_title(), self.SetColumns[iterator].get_column())
                iterator = iterator + 1

        else:
            print("ERROR - already Prepared")

    def print_table(self):
        if self.prepared:
            print(self.table)
        else:
            print("ERROR table not prepared")


BoosterTable = Table(tableTitlesWish, WishListData, MissingCardData)
BoosterTable.prepare_table()

BoosterTable.print_table()


tableColumns = []
for i in tableTitlesRares:
    tableColumns.append(Column(i, 1, 2, 3, 4))

for i in wishList:
    card = all_mtga_cards.find_one(i)
    wishList[i] = [all_mtga_cards.find_one(i), wishList[i]]

#newTable = PrettyTable()
#for i in tableColumns:
#    newTable.add_column(i.get_title(), i.get_column())
#print(newTable)



# TODO: use statistics to determine percentage
# TODO: fix makeTable
# TODO: Autoupdate for cards in set?
