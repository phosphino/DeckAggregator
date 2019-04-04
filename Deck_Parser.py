import os, json, re
import pandas as pd, numpy as np

default_path = os.path.join(os.getcwd(), 'TrainingDecks.txt')


class Training_Deck_Parser:
    def __init__(self, datapath=default_path):
        self._trainingdecks = []
        # open training decks file and load data.
        # TRAINING DECKS IS A LIST OF LISTS OF LISTS
        # TOP LIST IS THE LIST OF ALL DECKS
        # 2ND LIST IS THE LIST OF CARDS IN THE DECK
        # 3RD lIST IS A LIST OF INFORMATION FOR EACH CARD IN THE DECK
        # KEY FOR THE 3RD LIST: 0: QUANTITY, 1: CARD NAME, 2: SET CODE, 3: COLLECTOR CODE

        # self._trainingdecks[0][0][0] IS THE QUANTITY OF THE FIRST CARD IN THE FIRST DECK
        # self._trainingdecks[0][0][1] IS THE CARD NAME OF THE FIRST CARD IN THE FIRST DECK
        with open(datapath, 'r') as f:
            decklist = []
            for line in f:
                quantity = re.search(r"^\d{1,2}", line)
                card_name = re.search(r"\d+ ((.)*) \(", line)
                set_code = re.search(r"\((\w{3})\)", line)
                collector_code = re.search(r"\d{1,4}$", line)

                if card_name:
                    decklist.append(
                        (int(quantity.group(0)), str(card_name.group(1)), str(set_code.group(1)), int(collector_code.group(0))))
                else:
                    if len(decklist) > 0:
                        self._trainingdecks.append(decklist)
                    decklist = []
        f.close()
        self._trainingdecks = self.expand_decks(self._trainingdecks)

    def get_trainingdecks(self):
        return self._trainingdecks

    # RETURNS A REVISED LIST OF DECKS
    # STILL A LIST OF LIST OF LISTS
    # THIRD LIST IS A CARD AND
    def expand_decks(self, decks):
        revised_decks = []
        for deck in decks:
            revised_deck = []
            for entry in deck:
                for i in range(entry[0]):
                    revised_deck.append((i + 1, entry[1]))
            revised_deck = sorted(revised_deck, key=lambda x: x[1])
            revised_deck = sorted(revised_deck, key=lambda x: x[0])
            revised_decks.append(revised_deck)
        return revised_decks




