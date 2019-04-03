import os, json, re
import pandas as pd, numpy as np


default_path = os.path.join(os.getcwd(), 'TrainingDecks.txt')

class Deck_Reader:
    def __init__(self, datapath=default_path):
        decks = []
        with open(datapath, 'r') as f:
            decklist = []
            for line in f:
                quantity = re.search(r"^\d{1,2}", line)
                card_name = re.search(r"\d+ ((.)*) \(", line)
                set_code = re.search(r"\((\w{3})\)", line)
                collector_code = re.search(r"\d{1,4}$", line)

                if card_name:
                    decklist.append([quantity.group(0),card_name.group(1),set_code.group(1),collector_code.group(0)])
                else:
                    print(decklist)
                    if len(decklist) > 0:
                        decks.append(decklist)
                    decklist = []





if __name__ == '__main__':
    d = Deck_Reader()



