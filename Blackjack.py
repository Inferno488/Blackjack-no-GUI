# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 20:05:35 2019
"""

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit
    

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_complete = ''
        for card in self.deck:
            deck_complete += "\n"+card.__str__()
        return 'The deck has: \n'+deck_complete

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces +=1
    
    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        

def take_bet(chips):
    while True:
        try:
            chips_bet = int(input('Please enter the amount you want to bet'))
        except ValueError:
            print('Sorry must be an integer')
        else:
            if chips_bet > chips.total:
                print('Sorry your bet cannot exceed '+chips.total)
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        choice = input('Player: Do you wish to hit or stand?')
        if choice.lower().startswith('h'):
            hit(deck,hand)
        elif choice.lower().startswith('s'):
            print("Player stands, Dealer's turn")
            playing = False
        else:
            print("Couldn't catch that, please try again")
            continue
        break
    
def show_some(player,dealer):
    print("\nDealer's hand")
    print('<card hidden>')
    print('',dealer.cards[1])
    print("Player's hand ",*player.cards,sep = '\n ')
    
def show_all(player,dealer):
    print("Dealer's hand",*dealer.cards,sep = '\n ')
    print("Value: ",dealer.value)
    print("Player's hand ",*player.cards,sep = '\n ')
    print("Value: ",player.value)
    
def player_busts(chips):
    print("Player loses")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer loses")
    chips.win_bet()
    
def dealer_wins(chips):
    print("Dealer wins")
    chips.lose_bet()
    
def push():
    print("Dealer and Player tie, its a push!")
    

while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    for deal in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
    
    player_chips = Chips()
    
    
    # Prompt the Player for their bet
    take_bet(player_chips)

    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    
    while playing:  # recall this variable from our hit_or_stand function
        
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts()
            break


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 21:
            hit(deck,dealer_hand)
    
        # Show all cards
        
        show_all(player_hand,dealer_hand)
        # Run different winning scenarios
        if (dealer_hand.value > 21):
            dealer_busts(player_chips)
        elif (dealer_hand.value > player_hand.value):
            dealer_wins(player_chips)
        elif (dealer_hand.value < player_hand.value):
            player_wins(player_chips)
        else:
            push()
        
    
    # Inform Player of their chips total 
    print("Player's winnings stand at ", player_chips.total)
    
    # Ask to play again
    new = input("Would you like to play again?")
    if(new.lower().startswith('y')):
        playing = True
        continue
    else:
        break
