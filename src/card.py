import random

colors = ["Red", "Yellow", "Blue", "Green", "Black"]
Color_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "+2", "Skip"]
Black_values = ['W', "+4"]
All_values = Color_values + Black_values

class CardError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
         return repr(self.value)

class Card:
	def __init__(self, color, value):
		if color in colors:
			self.color = color
		else:
			print "Invalid color"
			raise CardError
		if color == "Black":
			if value in Black_values:
				self.value = value
		elif value in Color_values:
				self.value = value
		else:
			print "Invalid value"
			raise CardError
			
	def playable(self, MRC): # most-recent card
		if self.color == "Black":
			return True
		else:
			return MRC.color == self.color or MRC.value == self.value
			
	def printCard(self):
		return self.color + " " + self.value
		
class Discard:
	def __init__(self):
		self.pile = []
		
	def add(self, card):
		self.pile.append(card)
			
	def restart(self):
		random.shuffle(self.pile)
		tmp = self.pile
		self.pile = []
		return tmp
			
class Deck:	
	def __init__(self, size=52):
		self.deck = []
		for x in xrange(0, size):
			c = random.choice(colors)
			if c == "Black":
				v = random.choice(Black_values)
			else:
				v = random.choice(Color_values)
			self.deck.append(Card(c,v))
		self.discard = Discard()
			
	def remaining(self):
		return len(self.deck)
		
	def draw(self, num=1):
		ret = []
		while num > 0:
			if self.remaining() == 0:
				print "Restart deck..."
				print len(self.discard.pile)
				self.deck = self.discard.restart()
			ret.append(self.deck.pop())
			num = num - 1
		return ret
		
	def deal(self, num, size):
		ret = []
		for x in xrange(0, num):
			ret.append([])
		while size > 0:
			for i in xrange(0,num):
				[tmp] = self.draw()
				ret[i].append(tmp)
			size = size - 1
		return ret