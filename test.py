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
    if card.set_number < setMaxNumber[card.set]:
        return True
    return False


playerRares = 0
for key, value in collection.items():
    try:
        tempCard = all_mtga_cards.find_one(key)
        # print(tempCard.card_type)
        if tempCard.rarity != "Basic":
            # print(tempCard.pretty_name + " " + tempCard.set + " x" + str(value) )
            validCards = validCards + 1
            cardCount += value
            set_sort(sets, tempCard, value)
            if tempCard.rarity == "Rare" or tempCard.rarity == "Mythic Rare":
                set_sort(rares, tempCard, value)
                playerRares = playerRares + 1
    except ValueError as e:
        pass
cards = 0
cardsInSet = {}
raresInSet = {}
totalRares = 0
for i in all_mtga_cards.cards:
    if i.collectible is True:
        cards = cards + 1
        if i.rarity != "Basic":
            set_sort(cardsInSet, i, 4)
        if i.set != 'ANA':
            if (i.rarity == "Rare" or i.rarity == "Mythic Rare") and in_booster(i):
                set_sort(raresInSet, i, 4)
                totalRares = totalRares + 1

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
            newTable.add_column(i, _tableColumns[_iterator])
        except KeyError as error:
            print(error)
        _iterator = _iterator + 1
    print(newTable)


tableTitles.remove('ANA')
make_table("Rares Unique", [playerRares, totalRares, get_percentage(playerRares, totalRares)], raresInSet, cardsInSet, 0)
make_table("Rares Total ", [playerRares, totalRares * 4, get_percentage(playerRares, totalRares * 4)], raresInSet,
           cardsInSet, 1)

wishList = {}
for i in deckLists:
    if i["name"] == "$WishList":
        print(i["mainDeck"])
        iterator = 0
        while iterator != len(i["mainDeck"]):
            wishList[i["mainDeck"][iterator]] = i["mainDeck"][iterator+1]
            iterator = iterator + 2
# var = input("Press enter to quit")
for i in collection:
    pass

print(wishList)
