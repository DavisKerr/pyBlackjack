'''
The game of blackjack

TODO:
- Add a hand class and implement it in the game logic.
'''
import random

# Define card values.
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ("Two", "Three", "Four", "Five","Six", "Seven", "Eight", "Nine", 
           "Ten", "Jack", "Queen", "King", "Ace")

values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5,
           "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, 
           "Ten": 10, "Jack": 10, "Queen":10, "King": 10,
           "Ace":11}

class Card():
  '''
  Defines a card and its value.
  '''
  def __init__(self, rank, suit):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]
  
  def __str__(self):
    return f'{self.rank} of {self.suit}'

class Deck():
  '''
  Defines a deck of cards and common operations on them.
  '''

  def __init__(self):
    self.all_cards = []

    for suit in suits:
      for rank in ranks:
        self.all_cards.append(Card(rank, suit))
  
  def shuffle(self):
    random.shuffle(self.all_cards)

  def hit(self):
    return self.all_cards.pop()

class Player():
  '''
  Defines the player with number of chips and a name. 
  '''
  def __init__(self, name):
    self.name = name
    self.chips = 10

  def bet(self, bet_amount):
    if self.chips >= bet_amount and bet_amount > 0:
      self.chips -= bet_amount
      return bet_amount
    else:
      return -1

  def deposit(self, new_chips):
    self.chips += new_chips

  def __str__(self):
    return f'Player {self.name} has {self.chips} chips'


# Game Logic Functions

def getBet():
  is_valid = False
  userInput = ""
  while not is_valid:
    try:
      userInput = int(input("How much do you want to bet? "))
    except TypeError:
      print("Not a valid number. PLease enter a whole number of chips to bet.")
    except ValueError:
      print("Not a valid number. PLease enter a whole number of chips to bet.")
    else:
      is_valid = True
  return userInput

def getAction():
  is_valid = False
  userinput = ""
  while not is_valid:
    userInput = input("Would you like to hit or stay? ").lower()
    print(userInput)
    if userInput == "hit" or userInput == "stay":
      is_valid = True
    else:
      print("Please enter either 'hit' or 'stay'")
  return userInput

def printCards(cards):
  print("The cards are:")
  for card in cards:
    print(card)

def calculate_value(cards):
  elevens = []
  value = 0
  for card in cards:
    value += card.value
    if card.rank == "Ace":
      elevens.append(card)
  for ace in elevens:
    if value > 21:
      value -= 10
  return value
      



# Setup game:
game_on = True
player = Player("One")

print("")
print("")

# Game Loop
while game_on:
  print("")
  print("")

  # #Check for game over
  if player.chips <= 0:
    print('You ran out of money! Game over!')
    break

  # Inform the player how much money they have.
  print(player)

  # Set up Round:
  deck = Deck()
  deck.shuffle()
  dealer_hand = []
  player_hand = []
  bet = -1
  
  # Collect bet amount
  while bet < 0:
    bet = player.bet(getBet())
    if(bet == -1):
      print("Not enough Money to make that bet!")

  # Player Draws first. 
  print('Time for the first draw...')

  not_stopped = True

  playerValue = 0

  # Player draws until busting or staying. 
  while not_stopped:
    print("")
    print("")
    player_hand.append(deck.hit())
    printCards(player_hand)
    
    value = 0

    value = calculate_value(player_hand)
    print(f'Your Score: {value}')
    
    if(value > 21):
      print("BUST! Better luck next time!")
      playerValue = value
      break

    action = getAction()

    if action == "stay":
      not_stopped = False
      playerValue = value

  
  cpu_not_bust = True
  # Check to see if player busted.
  if playerValue > 21:
    cpu_not_bust = False
  else:
    print("")
    print("")
    print("Dealers turn:")

  # Dealer will draw until they win or bust.
  while cpu_not_bust:
    dealer_hand.append(deck.hit())
    
    value = 0

    for card in dealer_hand:
      value = calculate_value(dealer_hand)
    if value > 21:
      printCards(dealer_hand)
      print(f'Dealer value: {value}')
      print(f"Dealer Bust! You won {bet * 2} chips!")
      player.deposit(bet * 2)
      break

    if value >= playerValue:
      printCards(dealer_hand)
      print(f'Dealer won with {value}!')
      break

    

