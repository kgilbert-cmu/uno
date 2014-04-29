import card
import string

def gameOver(hands):
	if 1 in map(len, hands):
		#print "\n Someone has UNO"
		_ = 1
	if 0 in map(len, hands):
		return True
	else:
		return False

def printHand(cards, top_card):
	print "\nYour hand is:"
	for i in xrange(0, len(cards)):
		playable = "\t<---" if cards[i].playable(top_card) else ""
		print "(%s)" % i, cards[i].color, cards[i].value, playable
		
def main(players=2, firstHand=5):
	deck = card.Deck(52)
	game = deck.deal(players, firstHand)
	[MRC] = deck.draw(1)
	while MRC.color == "Black":
		[MRC] = deck.draw(1)
	turn = 0
	step = 1
	while not gameOver(game):
		print "\n The top of the deck is: ", MRC.color, MRC.value
		print "\nIt is Player %i's turn." % (turn + 1)
		printHand(game[turn], MRC)
		play = raw_input("\nType a number to select a card, or 'D' to draw. Which card will you play?  ")
		if play in ["quit", "Quit", "QUIT", "q", "Q"]:
			return None
		if play in ["draw", "Draw", "DRAW", "d", "D"]:
			game[turn].extend(deck.draw())
			continue
		if play == "?":
			for i in xrange(0, players):
				print "Player %i has %s cards remaining." % (i+1, len(game[i]))
		if play in ["next"]:
			print "\n Player %i is next" % ((turn + step*2) % players)
			continue
		if play.isdigit():
			play = int(play)
		else:
			continue
		if not play < len(game[turn]):
			print "\n \nThat was NOT a card in your hand. Please select again. \n \n"
			continue
		if game[turn][play].playable(MRC):
			MRC = game[turn][play]
			deck.discard.add(game[turn][play])
			game[turn] = game[turn][:play] + game[turn][play+1:]
			if MRC.color == "Black":
				if gameOver(game):
					continue
				wild_card_message = "Black means wild card! What color do you want?  "
				invalid_choice_message = "You can pick Red, Blue, Green, or Yellow.  "
				inp = string.capwords(raw_input(wild_card_message))
				while not inp in card.colors or inp == "Black":
					inp = string.capwords(raw_input(invalid_choice_message))
				MRC.color = inp
			if MRC.value in ["+4", "+2"]:
				print "Draw!"
				poor_sap = (turn + step) % players
				if "4" in MRC.value:
					game[poor_sap].extend(deck.draw(4))
				else:
					game[poor_sap].extend(deck.draw(2))
				MRC.value = "Skip"
			if MRC.value == "Skip":
				print "\n Player %i got skipped!" % ((turn + step*2) % players)
				turn = (turn + step*2) % players
				continue
			if MRC.value == "Reverse":
				print "Reversed!"
				step = step * -1
			turn = (turn + step) % players
		else:
			print "\n \nThat card can't be played now. \n"
	print "Game over."
	
if __name__ == "__main__":
    main(4)