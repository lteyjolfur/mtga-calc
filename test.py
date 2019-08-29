from mtga.set_data import all_mtga_cards
from mtga.models.card import Card

print(all_mtga_cards.count)
from getpass import getuser
import json

#class cardOwned:
#    card = Card()
#    owned = 0



filePath ="C:/Users/"+getuser()+"/AppData/LocalLow/Wizards Of The Coast/MTGA/output_log.txt"
filePos = 0;
print(filePath)
try:
    log = open(filePath,'r')
except:
    print("error : log not found")
logContents = log.read();
#preconName = "<== Deck.GetPreconDecks(3)"
#preconStart = logContents.find(preconName)+len(preconName)+1
#print(logContents[preconStart])
#preconEnd = logContents.find('[UnityCrossThreadLogger]',preconStart)
#print(logContents[preconStart+1:preconEnd])
#precon = json.loads(logContents[preconStart:preconEnd])

collectionName = "<== PlayerInventory.GetPlayerCardsV3("
collectionStart = logContents.find(collectionName)
collectionStart = logContents.find(')',collectionStart)+1
collectionEnd = logContents.find('[UnityCrossThreadLogger]',collectionStart)
print(logContents[collectionStart+1:collectionEnd])
collection = json.loads(logContents[collectionStart:collectionEnd])
print (collection.items())
print(len(collection))

validCards = 0
for key, value in collection.items():
    try:

        tempCard = all_mtga_cards.find_one(key)
        #print(tempCard.card_type)
        if(tempCard.rarity!= "Basic"):
            #print(tempCard.pretty_name + " " + tempCard.set + " x" + str(value) )
            validCards = validCards + 1
    except ValueError as e:
        pass
print("total count = "+str(all_mtga_cards.total_count))
print(all_mtga_cards.total_count - (len(collection)- validCards))
print(all_mtga_cards.lookup[1])
print(all_mtga_cards.count(1))
print("valid cards = " + str(validCards))
var = input("Press enter to quit")



#for i in precon:
#    print(i['description'])
#json.parse(logContents())



#s=log.readline()
#print(s)
#s=log.readline()
#print(s)



