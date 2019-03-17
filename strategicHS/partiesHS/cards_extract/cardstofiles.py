import os  # way of using operating system dependent functionality
import json

folder = os.getcwd()
with open(os.path.join(folder,"cards.json")) as f:
    carddata = json.load(f, encoding='windows-1252')
    for i, card in enumerate(carddata):
        with open(os.path.join(folder, str(i)+".json"), "w+") as f2:
            json.dump(card, f2)
