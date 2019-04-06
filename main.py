from Deck_Parser import *
from itertools import combinations as combi
import pandas as pd
from time import sleep
from output_log_mtga import personal_collection

class Aggregator(personal_collection):

    def __init__(self, training_list, rank=2):
        super(Aggregator, self).__init__()
        self._tdecks = training_list

        #Deck combinations a list of list of lists
        #Top list is the list of decks
        #Second list is the list of ranks in a given deck (rank 1 = 0, rank 2 = 1....). len(second list) returns highest rank
        #Third list elements are different card combinations of a given rank. Rank 1 is single cards Rank 2 is doubles...
        self._deck_combinations = self._contruct_combinations(rank)


        self._card_collective = self._construct_collective()
        self._combo_struct = self._define_struct(self._deck_combinations)
        self._decklist = (sorted(sorted(self._aggregate_decks(), key=lambda x:x[1]), key=lambda y: y[0]))
        exportdecklist = self.format_decklist(self._decklist)

        for x in exportdecklist:
            print(x)

        #print(sorted(sorted(self._card_collective, key=lambda x: x[0]), key=lambda x: x[1]))

    def format_decklist(self, decklist):
        decklist = [x[1] for x in decklist]
        singles = list(set(decklist))
        singles = dict((ele, 0) for ele in singles)
        for card in decklist:
            singles[card] += 1
        collection = self.arena_db
        decklistpd = collection[collection['card_name'].isin(list(set(decklist)))]
        exportlist = []
        for card in list(set(decklist)):
            if card in ['Plains', 'Mountain', 'Island', 'Forest', 'Swamp']:
                exportlist.append(str(singles[card])+" "+ self.return_land(card))
                continue
            card_info = decklistpd[decklistpd['card_name'] == card][['card_name','collector_number','set']]
            if card_info.empty:
                card_info = collection[collection['card_name'].str.contains(card)]
            card_info = card_info.iloc[0]
            name = card_info['card_name']
            set_ = card_info['set']
            if set_ == "dom":
                set_ = "dar"
            collector_number = card_info['collector_number']
            quantity = singles[card]
            exportlist.append(str(quantity)+" "+card+" "+"("+set_.upper()+")"+" "+collector_number)
        return exportlist



    def return_land(self, card):
        if card == 'Plains':
            return "Plains (M19) 263"
        if card == 'Mountain':
            return "Mountain (XLN) 275"
        if card == 'Island':
            return "Island (M19) 266"
        if card == 'Forest':
            return "Forest (M19) 280"
        if card == 'Swamp':
            return "Swamp (DAR) 258"

    @property
    def decklist(self):
        decklist = [x[1] for x in self._decklist]
        return sorted(decklist)

    @property
    def deck_combinations(self):
        return self._deck_combinations

    def _aggregate_decks(self):

        collective = self._card_collective
        combinations = list(self._combo_struct.keys())

        while len(collective) > 60:
            print(len(collective))
            score_card = dict((el, 0) for el in collective)
            for combo in combinations:
                if self._iscombo_incollective(combo, collective) is False:
                    continue
                for card in combo:
                    score_card[card] +=  self._combo_struct[combo] * (1. / (2**len(combo)))

            cutcard = self._return_lowest_card(score_card)
            collective.remove(cutcard)

        return collective

    def _return_lowest_card(self, scores):
        key_val_pairs = sorted(list(scores.items()), key=lambda x: x[1])
        return key_val_pairs[0][0]

    def _iscombo_incollective(self,combo, collective):

        for item in combo:
            if item not in collective:
                return False
        return True


    #begins ranking the combinations in each individual deck
    def _define_struct(self, deck_combinations):
        combinations = []

        for deck in deck_combinations:
            for i, rank in enumerate(deck):
                for combo in rank:
                    combinations.append(combo)

        struct = dict((x, 0) for x in combinations)
        for combo in combinations:
            struct[combo] = 1 + struct[combo]
        return struct

    def _contruct_combinations(self, rank):
        deck_combos = []

        for deck in self._tdecks:
            rank_combinations = []
            for i in range(1, rank+1):
                comb = combi(deck, i)
                comb = list(comb)
                rank_combinations.append(comb)
            deck_combos.append(rank_combinations)
        return deck_combos
        #DECK COMBOS IS A LIST OF LIST OF TUPLES OF TUPLES
        #TOP LIST IS A LIST OF TUPLES CONTAINING COMBOS
        #THE SECOND LIST HOLD THE COMBINATIONS. THE ELEMENTS OF THE TUPLE ARE LISTS
        #EACH TUPLE IN THE TUPLE IS A SINGLE CARD. ELEMENT 0 IS ITS OCCURENCE (1,2,3,4...) AND ELEMENT 1 IS THE CARD NAME

    #returns a list of all unique cards used in all the decks
    #Note: the first instance of a card in a deck IS DISTINCT from the second/third/fourth instance in a deck
    #second instance is distinct from third/fourth and so on
    #The deck parser already took care of distinguishing the copies of cards in the decklists
    #this construct will be whittled down to the final decklist, including lands
    def _construct_collective(self):
        card_collective = []
        for deck in self._tdecks:
            card_collective = card_collective + deck
        list_collective=[]
        card_collective = set(card_collective)
        return list(set(card_collective))

if __name__ == '__main__':
    parser = Training_Deck_Parser()
    training_decks = parser.get_trainingdecks()
    b = Aggregator(training_decks)

    #print(b.decklist)

