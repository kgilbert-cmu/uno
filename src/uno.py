import card
import string

def gameOver(hands):
	if 1 in map(len, hands):
		print "Someone has UNO"
	if 0 in map(len, hands):
		return True
	else:
		return False

def printHand(cards):
	print "\nYour hand is:"
	for i in xrange(0, len(cards)):
		print "(%s)" % i, cards[i].color, cards[i].value
		
def main(players=2, firstHand=5):
	deck = card.Deck(52)
	game = deck.deal(players, firstHand)
	[MRC] = deck.draw(1)
	while MRC.color == "Black":
		[MRC] = deck.draw(1)
	while not gameOver(game):
		print "The top of the deck is: ", MRC.color, MRC.value
		printHand(game[0])
		play = raw_input("\nType a number to select a card, or 'D' to draw. Which card will you play?  ")
		if play in ["quit", "Quit", "QUIT", "q", "Q"]:
			return None
		if play in ["draw", "Draw", "DRAW", "d", "D"]:
			game[0].extend(deck.draw())
			continue
		if play.isdigit():
			play = int(play)
		else:
			continue
		if not play < len(game[0]):
			print "\n \nThat was NOT a card in your hand. Please select again. \n \n"
			continue
		if game[0][play].playable(MRC):
			MRC = game[0][play]
			deck.discard.add(game[0][play])
			game[0] = game[0][:play] + game[0][play+1:]
			if MRC.color == "Black":
				wild_card_message = "Black means wild card! What color do you want?  "
				invalid_choice_message = "You can pick Red, Blue, Green, or Yellow.  "
				inp = string.capwords(raw_input(wild_card_message))
				while not inp in card.colors or inp == "Black":
					inp = string.capwords(raw_input(invalid_choice_message))
				MRC.color = inp
			if MRC.value in ["+4", "+2"]:
				print "Draw!"
			if MRC.value == "Skip":
				print "Skipped!"
			if MRC.value == "Reverse":
				print "Reversed!"
		else:
			print "\n \nThat card can't be played now. \n \n"
	print "Game over."
	
if __name__ == "__main__":
    main(1)