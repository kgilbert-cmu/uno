import card
import string
import random
import copy

def finish(hands):
	scores = map(len, hands)
	results = sorted(zip(range(1, len(scores)+1), scores), key=lambda (p,scores): scores)
	for (x,s) in results:
		if s == 0:
			print "Player %i won." % x
		else:
			print "Player %i had %i cards left." % (x,s)

def gameOver(hands):
	if 0 in map(len, hands):
		return True
	else:
		return False

def printHand(cards, top_card):
	print "\nYour hand is:"
	for i in xrange(0, len(cards)):
		playable = "\t<---" if cards[i].playable(top_card) else ""
		print "(%s)" % i, cards[i].color, cards[i].value, playable
		
def main(humans=1, computers=3, firstHand=7):
	players = humans + computers
	deck = card.Deck()
	game = deck.deal(players, firstHand)
	[MRC] = deck.draw()
	while MRC.color == "Black":
		[MRC] = deck.draw(1)
	turn = 0
	step = 1
	while not gameOver(game):
		# for i in xrange(0, len(game)):
			# if len(game[i]) == 1:
				# print "Player %i has UNO" % (i + 1)
		print "\nIt is Player %i's turn and Player %i is next." % ((turn + 1), ((turn + step) % players + 1))
		print "\n The top of the deck is: ", MRC.color, MRC.value
		if turn >= humans:
			plays = zip(range(len(game[turn])), [c.playable(MRC) for c in game[turn]])
			plays = [i for (i, tf) in plays if tf]
			if len(plays) == 0:
				play = 'draw'
			else:
				play = str(random.choice(plays))
				print " Player %i plays %s" % (turn + 1, game[turn][int(play)].printCard())
		else:
			printHand(game[turn], MRC)
			play = raw_input("\nType a number to select a card, or 'D' to draw. Which card will you play?  ")
		if play == "help":
			print "\nThe game supports quit, help, auto, draw, ?, next, and card indices."
			continue
		if play in ["quit", "Quit", "QUIT", "q", "Q"]:
			return None
		if play == "auto":
			humans = 0
			computers = computers + 1
		if play == 'd':
			game[turn].extend(deck.draw())
			continue
		if play == "draw":
			if len(game[turn]) == 1:
				print "Player %i had to draw cards." % (turn + 1)
			while True not in [c.playable(MRC) for c in game[turn]]:
				game[turn].extend(deck.draw())
			continue
		if play == "?":
			for i in xrange(0, players):
				if len(game[i]) > 1:
					print "Player %i has %s cards remaining." % (i+1, len(game[i]))
				else:
					print "Player %i has UNO." % (i+1)
		if play == "next":
			print "\n Player %i is next" % ((turn + step) % players + 1)
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
			deck.discard.add(copy.deepcopy(game[turn][play]))
			game[turn] = game[turn][:play] + game[turn][play+1:]
			if MRC.color == "Black":
				if gameOver(game):
					continue
				wild_card_message = "Black means wild card! What color do you want?  "
				invalid_choice_message = "You can pick Red, Blue, Green, or Yellow.  "
				if turn >= humans:
					colors = [c.color for c in game[turn] if c.color != "Black"]
					inp = random.choice(colors)
				else:
					inp = string.capwords(raw_input(wild_card_message))
					while not inp in card.colors or inp == "Black":
						inp = string.capwords(raw_input(invalid_choice_message))
				MRC.color = inp
			if MRC.value in ["+4", "+2"]:
				if gameOver(game):
					continue
				print "Player %i must draw!" % ((turn + step) % players + 1)
				poor_sap = (turn + step) % players
				if "4" in MRC.value:
					game[poor_sap].extend(deck.draw(4))
				else:
					game[poor_sap].extend(deck.draw(2))
			if MRC.value == "Skip" or MRC.value == "+4":
				if gameOver(game):
					continue
				print "\n Player %i got skipped!" % ((turn + step) % players + 1)
				turn = (turn + step*2) % players
				continue
			if MRC.value == "Reverse":
				if gameOver(game):
					continue
				step = step * -1
				print "Reversed! It is now Player %i's turn." % ((turn + step) % players + 1)
			turn = (turn + step) % players
		else:
			print "\n \nThat card can't be played now. \n"
	print "\nGame over."
	print ""
	finish(game)
	
if __name__ == "__main__":
    main(1,3)
