
import simplegui
import random
import tkinter as simplegui
#import PySimpleGUI as simplegui
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

in_play = False
outcome = ""
score = 0
result = ""

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        ret = ''
        for each in self.cards:
            ret += each.get_suit() + each.get_rank() + ' '
        return "Hand Contains " + ret

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces_count = 0
        for each_card in self.cards:
            if each_card.get_rank() == 'A':
                aces_count += 1               
            value += VALUES[each_card.get_rank()]
        
        if aces_count == 0:
            return value
        else:
            if value + 10 < 21:
                return value + 10
            else:
                return value
   
    def draw(self, canvas, pos):
        for each_card in self.cards:
            pos[0] += CARD_SIZE[0] + 20
            each_card.draw(canvas, pos)           
        
class Deck:
    def __init__(self):
        self.deck_cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
    
    def shuffle(self):
        random.shuffle(self.deck_cards)
    
    def deal_card(self):
        return self.deck_cards.pop()
    
    def __str__(self):       
        string = ''
        for each in self.deck_cards:
            string += str(each) + ' '
        return 'Deck Contains: ' + string

def deal():
    global outcome, in_play, result, score
    global player_hand, dealer_hand, deck
    
    print ('New Deal!')
    
    result = ''
    outcome = 'Hit or  Stand?'
    if in_play: 
        score -= 1
        print (result)
        
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    
    deck.shuffle()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    in_play = True

def hit():
    global in_play, outcome, result, score
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())

        
        if player_hand.get_value() > 21:
            outcome = 'New Deal?' 
            result = 'You Have Busted!'
            print ('Score:', player_hand.get_value())
            print (result,',', outcome)
            in_play = False
            score -= 1
       
def stand():
    global in_play, outcome, result, score
    print (result)
    while dealer_hand.get_value() < 17:
        if in_play:
            dealer_hand.add_card(deck.deal_card())       

    if dealer_hand.get_value() > 21:
        outcome = 'New Deal?'
        result = 'Dealer have busted'
        in_play = False
        score += 1
    elif dealer_hand.get_value() > player_hand.get_value():
        result = 'Dealer Wins'
        outcome = 'New Deal?'
        in_play = False
        score -= 1 # dealer wins
    elif player_hand.get_value() > dealer_hand.get_value():
        result = 'Player Wins'
        outcome = 'New Deal?'
        in_play = False
        score += 1
    elif player_hand.get_value() == dealer_hand.get_value():
        result = "It's a Tie, But Dealer wins!"
        outcome = 'New Deal?'
        in_play = False
        score -= 1
    
def draw(canvas):
    canvas.draw_text('Blackjack', [250,50], 35, 'Yellow')
    canvas.draw_text('Player', [5, 450], 25, 'Black')
    canvas.draw_text('Dealer', [5, 250], 25, 'Black')
    canvas.draw_text('Score: ' + str(score), [400, 90], 30, 'White', 'monospace')
    player_value = player_hand.get_value()
    canvas.draw_text(str(player_value), [5, 480], 20, 'Black', 'monospace')
    canvas.draw_text(outcome, [5, 150], 40, 'Yellow', 'monospace')
    canvas.draw_text(result, [5, 360], 30, 'White', 'monospace')

    player_hand.draw(canvas, [10,400])
    dealer_hand.draw(canvas, [10,200])
    
    if in_play:
        hole_center_canvas = [30 + CARD_SIZE[0] + CARD_CENTER[0], 249]
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, hole_center_canvas , CARD_BACK_SIZE)
    else:
        dealer_value = dealer_hand.get_value()
        canvas.draw_text(str(dealer_value), [5, 280], 20, 'Black', 'monospace')

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()