import random

colors = ["Red", "Yellow", "Blue", "Green", "Black"]
Color_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "+2", "Skip"]
Black_values = ['W', "+4"]
All_values = Color_values + Black_values

class Card:
	def __init__(self, color, value):
		self.color = color
		self.value = value
		
	def color(self):
		return self.color
		
	def value(self):
		return self.value
		
	def playable(self, MRC): # most-recent card
		if self.color == "Black":
			return True
		else:
			return MRC.color() == self.color or MRC.value() == self.value()
		
class Deck:
	def __init__(self, size):
		self.deck = []
		for x in xrange(0, size):
			c = random.choice(colors)
			if c == "Black":
				v = random.choice(Black_values)
			else:
				v = random.choice(Color_values)
			self.deck.append(Card(c,v))
			
	def draw(self, num):
		ret = []
		for x in xrange(0, num):
			ret.append(self.deck.pop())
		return ret
		
class Discard:
	def __init__(self):
		self.pile = []
	
	def add(self, card):
		self.pile.append(card)
		
	def restart(self):
		tmp = random.shuffle(self.pile)
		self.pile = []
		return tmp