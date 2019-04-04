from Deck_Parser import *
from itertools import combinations as combi
from time import sleep

class Aggregator:

    def __init__(self, training_list, rank = 3):
        self._tdecks = training_list

        #Deck combinations a list of list of lists
        #Top list is the list of decks
        #Second list is the list of ranks in a given deck (rank 1 = 0, rank 2 = 1....). len(second list) returns highest rank
        #Third list elements are different card combinations of a given rank. Rank 1 is single cards Rank 2 is doubles...
        self._deck_combinations = self._contruct_combinations(rank)
        self._card_collective = self._construct_collective()

        self._combo_struct = self._define_struct(self._deck_combinations)

        for key, value in self._combo_struct.items():
            if value > 1:
                print(key, value)


    @property
    def deck_combinations(self):
        return self._deck_combinations
    
    #begins ranking the combinations in each individual deck
    def _define_struct(self, deck_combinations):
        combinations = []

        for deck in deck_combinations:
            for i, rank in enumerate(deck):
                for combo in rank:
                    if i == 0:
                        print(combo[0])
                    combinations.append(combo)

        struct = dict((x, 0) for x in combinations)
        for combo in combinations:
            if len(combo) == 1:
                print(combo[0])
                struct[combo[0]] += 1
        return struct

    def _check_tuples(self, check, against):
        pass
    
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
        #DECK COMBOS IS A LIST OF TUPLES OF LISTS
        #TOP LIST IS A LIST OF TUPLES CONTAINING COMBOS
        #THE TUPLES HOLD THE COMBINATIONS. THE ELEMENTS OF THE TUPLE ARE LISTS
        #EACH LIST IN THE TUPLE IS A SINGLE CARD. ELEMENT 0 IS ITS OCCURENCE (1,2,3,4...) AND ELEMENT 1 IS THE CARD NAME

    #returns a list of all unique cards used in all the decks
    #Note: the first instance of a card in a deck IS DISTINCT from the second/third/fourth instance in a deck
    #second instance is distinct from third/fourth and so on
    #The deck parser already took care of distinguishing the copies of cards in the decklists
    #this construct will be whittled down to the final decklist, including lands
    def _construct_collective(self):
        card_collective = []
        for deck in self._tdecks:
            card_collective = card_collective + deck
        return list(set(tuple(card) for card in card_collective))

if __name__ == '__main__':
    parser = Training_Deck_Parser()
    training_decks = parser.get_trainingdecks()
    b = Aggregator(training_decks)

