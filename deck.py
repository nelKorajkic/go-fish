#import for support with randomizing
import random

#import for delay
import time

#import for clearing the screen for neatness
import os
import sys

#clear the screen for neatness
def clearScreen():
    if (sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin"):
        os.system('clear')
    if (sys.platform == "win32" or sys.platform == "win64"):
        os.system('cls')
    else:
        print("\n" * 100)

#A card object will hold suit as a string and rank as an int
# that changes into a string when called if it's a face card. "1=Ace"
class Card(object):
    face = 0
    #intiliazes the objects variables
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    #Used to return the rank of the card object
    def getRank(self):
        return self.rank
    #Used to return the suit of the card object
    def getSuit(self):
        return self.suit

    #Used to display the card as a string AND convert it to
    # a face name (Ace, Jack etc)
    def displayCard(self):
        if self.rank == 1:
            face = "Ace"
        elif self.rank == 11:
            face = "Jack"
        elif self.rank == 12:
            face = "Queen"
        elif self.rank == 13:
            face = "King"
        else:
            face = self.rank
        #Prints out the card attributes as a string
        print(face, 'of', self.suit)

# shuffles the deck
def shuffle(deck):
    random.shuffle(deck)
    return deck

#Function to add a number of cards to each player's hand
def drawHand(numToDraw, deck, Array):
    i = 0
    cardToAdd = 0
    count = 1
    while i  < numToDraw:
        remainingCards = len(deck)
        cardToAdd = deck.pop((remainingCards - 1) - i)
        Array.append(cardToAdd)
        i += 1
    return Array, cardToAdd, count


# Used to display each player's hand
def displayHand(handArray):
    numOfCards = len(handArray)
    i = 0
    while i < numOfCards:
        handArray[i].displayCard()
        i += 1

#this function is used for guessing the opposing players hand
# if it finds a match it will let the user know, then display the users new hand
#after all matches are added.
def compare(handArray1, handArray2, guess, identity):
    count = 0
    for ele in handArray2[:]:
        value = ele.getRank()
        if guess == value:
            handArray1.append(ele)
            handArray2.remove(ele)
            count += 1

    if count == 0:
        if identity == 0:
            print('Computer says: "GO FISH!"')
        if identity == 1:
            print('You say: "GO FISH!"')
    else:
        if identity == 0:
            print("The computer has the card(s) you're looking for...")
            print("You add the new card(s) to your hand...")
        if identity == 1:
            print("You have the cards the computer is looking for...")
            print("The computer adds the new card(s) to its hand...")
        time.sleep(1)

    return handArray1, handArray2, count

#made by Cuong Lai
def checkForBooks(bookCount, handArray):
    count = 0
    for ele in handArray[:]:
        if sum(p.getRank() == ele.getRank() for p in handArray) == 4:
            for i in handArray[:]:
                if ele.getRank() == i.getRank():
                    handArray.remove(i)
            bookCount += 1
            count += 1

    return bookCount, handArray, count

def rules():
    print("Welcome to Go Fish! Here's how to play:")
    print("1. You play against a computer. You both start with 7 cards.")
    print("2. You take turns asking the other player for a card. If they have it, they must give you every card of that value they have in their hand.")
    print("3. If they don't have the card, you must draw a card from the deck, or go fishing.")
    print("4. If a player gets 4 of the same card, they get a book (aka a point).")
    print("5. Once all books have been found, the game ends. Whoever has the most books wins.")
    print("Enjoy the game!\n")

#Easy mode made by Aaron
def easy(numToDraw, deck, playerHandArray, computerHandArray, numOfTurns, drawFromDeck, avgRequestsCorrect):
    # set number to deal the deck to player and computer
    numToDraw = 7

    # initialize variables
    playerBooks = 0
    computerBooks = 0
    combinedBooks = 0

    # deal deck to player and computer
    playerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, playerHandArray)
    computerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, computerHandArray)

    # set number to draw card when going fishing
    numToDraw = 1

    print("Deck is being shuffled....")
    time.sleep(1)
    print("You get your starting hand...\n")
    time.sleep(1)
    # while loop that tests if all the books have been found
    while (combinedBooks < 13):

        # displays users hand
        print("Your Hand Is: ")
        displayHand(playerHandArray)
        print("\n")
        time.sleep(2)

        print("\n----------YOUR TURN----------\n")
        # display if anyone has books
        print("You have " , str(playerBooks) , " books.")
        print("The computer has " , str(computerBooks) , " books.")
        print("There are", len(deck), "cards left in the deck.")

        # get combined book total
        combinedBooks = playerBooks + computerBooks

        # get user guess
        guess = getGuess(playerHandArray)

        # check if the users guess is in the computers hand
        playerHandArray, computerHandArray, matchCount = compare(playerHandArray, computerHandArray, guess, 0)

        # if not in computers hand draw a card
        if matchCount == 0:
            playerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, playerHandArray)
            avgRequestsCorrect += 1

        # check if there are any books in the players or computers hand
        playerBooks, playerHandArray, count = checkForBooks(playerBooks, playerHandArray)

        # if a player finds a book print:
        if count > 0:
            print("You found a book of " , guess , "'s")

        # get combined book total
        combinedBooks = playerBooks + computerBooks

        # if there are 13 books found break the loop
        if (combinedBooks == 13):
            break

        # get random card to guess from computers hand
        compHandLength = len(computerHandArray)
        randChoice = random.randint(0, (compHandLength - 1))
        compChoice = computerHandArray[randChoice].getRank()

        # displays to the user the computers choice
        print("\nComputer asks for a " , compChoice , "\n")

        # checks if computers choice is in users hand and acts accordingly
        computerHandArray, playerHandArray, matchCount = compare(computerHandArray, playerHandArray, compChoice, 1)

        # if not, draw card for computer hand
        if matchCount == 0:
            computerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, computerHandArray)

        # checks for books in player and computers hand
        computerBooks, computerHandArray, count = checkForBooks(computerBooks, computerHandArray)

        # if the computer finds a book
        if count > 0:
            print("Computer has found a book of " , compChoice , "'s")

        input("Press any key when you're ready for your next turn")

        clearScreen()

        numOfTurns += 1

    # if user wins the game
    if (playerBooks > computerBooks):
        print("You have bested the computer.")

    # if user loses the game
    else:
        print("The computer has bested you.")

#Hard mode, made by Cuong Lai
def hard(numToDraw, deck, playerHandArray, computerHandArray, numOfTurns, drawFromDeck, avgRequestsCorrect):
    playerBooks = 0
    computerBooks = 0

    combinedBooks = 0

    print("Deck is being shuffled....")
    time.sleep(1)
    print("You get your starting hand...\n")
    time.sleep(1)

    wentFishing = 0

    playerHandArray, playerCardDrawn, wentFishing = drawHand(numToDraw, deck, playerHandArray)

    computerHandArray, computerCardDrawn, wentFishing = drawHand(numToDraw, deck, computerHandArray)

    matchCount = 0
    correctInput = 0
    computerHandIndex = 0

    numToDraw = 1
    wentFishing = 0
    cardWasDrawn = 0

    while combinedBooks < 13:
        wentFishing = 0
        length = len(playerHandArray)

        print("Your hand is: ")
        displayHand(playerHandArray)
        time.sleep(2)

        if not playerHandArray:
            print("You don't have any cards... You draw a card.")
            playerHandArray, playerCardDrawn, wentFishing = drawHand(numToDraw, deck, playerHandArray)
            print("You drew a", playerCardDrawn.getRank())

        if wentFishing == 0:
            playerBooks, playerHandArray, count = checkForBooks(playerBooks, playerHandArray)
            computerBooks, computerHandArray, count = checkForBooks(computerBooks, computerHandArray)

            if count > 0:
                print("You or the computer already have a book!")
                time.sleep(1)
                print("==============================================")
                print("Your new hand is: ")
                displayHand(playerHandArray)
                print("\nThe computer's hand is: ")
                displayHand(computerHandArray)
                time.sleep(1)

            print("\n----------YOUR TURN----------")
            print("\nYou have", playerBooks, "books.")
            print("The computer has", computerBooks, "books.")
            print("There are", len(deck), "cards left in the deck.\n")

            flag = False
            tempArray = []
            while flag == False:
                guess = input("\nAsk if the computer has any... (integers only, 11 = Jack, 12 = Queen etc.): ")
                time.sleep(1)
                for ele in playerHandArray:
                    tempArray.append(ele.getRank())
                if guess.isdigit() == False:
                    print("Not an integer! Try again.")
                else:
                    guess = int(guess)
                    if guess in tempArray:
                        flag = True
                        playerHandArray, computerHandArray, matchCount = compare(playerHandArray, computerHandArray, guess, 0)
                        if matchCount > 0:
                            avgRequestsCorrect += 1
                            time.sleep(1)
                            playerBooks, playerHandArray, count = checkForBooks(playerBooks, playerHandArray)
                            if count > 0:
                                time.sleep(1)
                                if (guess == 1):
                                    guess = "Ace"
                                if (guess == 11):
                                    guess = "Jack"
                                if (guess == 12):
                                    guess = "Queen"
                                if (guess == 13):
                                    guess = "King"
                                print("\nYou got a book of all", guess,"'s!")
                            time.sleep(1)
                            print("\nYou have", playerBooks, "books.")
                            print("The computer has", computerBooks, "books.")
                            if guess == computerCardDrawn.getRank():
                                cardWasDrawn = 0
                        else:
                            playerHandArray, playerCardDrawn, wentFishing = drawHand(numToDraw, deck, playerHandArray)
                            time.sleep(1)
                            print("You draw a card from the deck... It's a", playerCardDrawn.getRank())
                            time.sleep(2)
                            playerBooks, playerHandArray, count = checkForBooks(playerBooks, playerHandArray)
                            if count > 0:
                                print("You got a book of", playerCardDrawn.getRank(), "'s by drawing a card from the deck!")
                                drawFromDeck += 1
                                time.sleep(1)
                    else:
                        print("That card is not in your hand! Try again.")
        combinedBooks = playerBooks + computerBooks


        print("==============================================")

        wentFishing = 0

        if combinedBooks < 13:

            print("Your hand is: ")
            displayHand(playerHandArray)
            if not computerHandArray:
                print("The computer doesn't have any cards... It draws a card.")
                computerHandArray, computerCardDrawn, wentFishing = drawHand(numToDraw, deck, computerHandArray)
                cardWasDrawn = 1
            if wentFishing == 0:
                print("\n----------COMPUTER'S TURN----------\n")
                time.sleep(1)
                if cardWasDrawn == 0:
                    if computerHandIndex >= len(computerHandArray):
                        computerHandIndex = 0
                    computerGuess = computerHandArray[computerHandIndex].getRank()
                    print("The computer asks for a", computerGuess)
                    time.sleep(2)
                    computerHandArray, playerHandArray, matchCount = compare(computerHandArray, playerHandArray, computerGuess, 1)
                    computerHandIndex += 1
                else:
                    if sum(p.rank == computerCardDrawn.getRank() for p in computerHandArray) == 1:
                        computerGuess = computerCardDrawn.getRank()
                        print("The computer asks for a", computerGuess)
                        time.sleep(2)
                        computerHandArray, playerHandArray, matchCount = compare(computerHandArray, playerHandArray, computerGuess, 1)
                    else:
                        if computerHandIndex >= len(computerHandArray):
                            computerHandIndex = 0
                        computerGuess = computerHandArray[computerHandIndex].getRank()
                        print("The computer asks for a", computerGuess)
                        time.sleep(2)
                        computerHandArray, playerHandArray, matchCount = compare(computerHandArray, playerHandArray, computerGuess, 1)
                        computerHandIndex += 1

                if matchCount > 0:
                    avgRequestsCorrect += 1
                    time.sleep(1)

                    computerBooks, computerHandArray, count = checkForBooks(computerBooks, computerHandArray)
                    if count > 0:
                        time.sleep(1)
                        print("\nThe computer got a book of all", computerGuess,"'s!")

                        time.sleep(1)
                        print("\nYou have", playerBooks, "books.")
                        print("The computer has", computerBooks, "books.")

                else:
                    computerHandArray, computerCardDrawn, wentFishing = drawHand(numToDraw, deck, computerHandArray)
                    cardWasDrawn = 1
                    time.sleep(1)
                    print("The computer draws a card from the deck...")
                    time.sleep(2)
                    computerBooks, computerHandArray, count = checkForBooks(computerBooks, computerHandArray)
                    if count > 0:
                        print("The computer got a book of", computerCardDrawn.getRank(), "'s by drawing a card from the deck!")
                        drawFromDeck += 1
                        time.sleep(1)

            combinedBooks = playerBooks + computerBooks

            input("Press any key when you're ready for your next turn")

            clearScreen()

            numOfTurns += 1

    if playerBooks > computerBooks:
        print("YOU WIN!")
    else:
        print("You lose! Better luck next time.")

    return numOfTurns, drawFromDeck, avgRequestsCorrect

def getGuess(playerHandArray):
    guess = input("Ask if the computer has any... (integers only, 11 = Jack, 12 = Queen etc.):")

    try:
        guess = int(guess)
    except:
        print("You can only enter in a number from 1 to 13!\n")
        guess = getGuess(playerHandArray)

    if (guess < 1 or guess > 13):
        print("You can only enter in a number from 1 to 13!\n")
        guess = getGuess(playerHandArray)

    for x in playerHandArray:
        if (guess == x.rank):
            return guess
    else:
        print("You can only ask for a number you already have at least one of!\n")
        guess = getGuess(playerHandArray)
        return guess


#Devious mode made by Ramy
def devious(numToDraw, deck, playerHandArray, computerHandArray, numOfTurns, drawFromDeck, avgRequestsCorrect):
    #at the begining of the game each player draws 7 cards
    numToDraw = 7

    #keep track of how many books each player has
    playerBooks = 0
    computerBooks = 0

    #once there are 13 total books then the game is over
    combinedBooks = 0

    print("Deck is being shuffled....")
    time.sleep(1)
    print("You get your starting hand...\n")
    time.sleep(1)
    #get the two players' hands
    #I added the cardToAdd here because the drawHand function returns that value - Cuong
    playerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, playerHandArray)
    computerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, computerHandArray)

    #after this point each player can only draw one card at a time
    numToDraw = 1

    #computer lies every third time they have the opportunity to give a card but says that it cant
    evil = 0

    while (combinedBooks < 13):
        #count how many books the players have and show user
        playerBooks, playerHandArray, count = checkForBooks(playerBooks, playerHandArray)
        print(" ".join(["You have", str(playerBooks), "books\nThe computer has", str(computerBooks), "books\n"]))
        print("There are", len(deck), "cards left in the deck.")

        combinedBooks = playerBooks + computerBooks

        #show the user their cards
        print("Your hand:")
        displayHand(playerHandArray)
        print("\n")

        time.sleep(2)
        print("\n----------YOUR TURN----------")



        if (combinedBooks == 13):
            break

        #player asks for card from computer
        #player goes first. Who says chivalry is dead?
        guess = getGuess(playerHandArray)

        #control variable for seeing if users guess matched computers hand
        match = False

        for x in computerHandArray:
            #changed .rank here to getRank() - Cuong
            if (guess == x.getRank()):
                if (evil == 2):
                    evil = 0
                    break
                print("You found a match!\n")
                computerHandArray.pop(computerHandArray.index(x))
                playerHandArray.append(x)
                evil = evil + 1
                match = True
                avgRequestsCorrect += 1
                #no break because the computer should give out ALL of the cards of that rank...unless evil == 3

        if (match == False):
            print("Go Fish\n")
            playerHandArray = drawHand(numToDraw, deck, playerHandArray)


        #pause for the user to read what happened during their turn
        time.sleep(2)

        ###now the computer gets to play. doesnt matter if the player got the card they wanted

        #computer picks a random card that they have
        guess = computerHandArray[random.randint(0, len(computerHandArray) - 1)].getRank()

        if (guess == 1):
            guess = "Ace"
        if (guess == 11):
            guess = "Jack"
        if (guess == 12):
            guess = "Queen"
        if (guess == 13):
            guess = "King"

        #tell the user what the computer picked
        print(" ".join(["My turn!\nI want a", str(guess),"\n"]))

        #control variable overwritten for computer's turn
        match = False

        for x in playerHandArray[:]:
            if type(x) == list:
                playerHandArray = x
                break

        for x in playerHandArray:
            #changed .rank here to .getRank() - Cuong
            if (guess == x.getRank()):
                print("You have one! Let me just take that from you.\n")
                playerHandArray.pop(playerHandArray.index(x))
                computerHandArray.append(x)
                match = True
                #no break because the user should give out ALL of the cards of that rank

        if (match == False):
            print("Aww man, you don't have one. I'll go fish.\n")
            #added cardToAdd here - Cuong
            computerHandArray, cardToAdd, wentFishing = drawHand(numToDraw, deck, computerHandArray)

        time.sleep(2)

        input("Press any key when you're ready for your next turn")

        clearScreen()

        #count total number of books
        combinedBooks = playerBooks + computerBooks

        numOfTurns += 1

    #end while loop

    if (playerBooks > computerBooks):
        print("Congrats! You won!")
    if (playerBook < computerBooks):
        print("Haha you lost!")


#Main will set up the game (sets up the deck and both player's hands.)
def main():
    #list for the suits
    suit = ["Clubs","Diamonds","Hearts", "Spades"]
    #list for the values of each card
    rank = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    #An array of the
    deck = []
    # this nested loop goes through the first list suit and for each suit goes through for each rank (13 times). This makes the ordered deck.
    j = -1
    for ele in suit:
        i = 0
        j += 1
        for ele in rank:
            deck.append(Card(rank[i], suit[j]))
            i += 1
    shuffle(deck)

    #sets up empty hands for the comp and player
    # makes the starting hand be 7 cards
    playerHandArray = []
    computerHandArray = []
    numToDraw = 7

    #flag that keeps track of the following loop
    flag = 0
    #this loop asks the user for a game difficulty and checks the input is correct.
    #it will set the flag to 1 if the input is correct, and the program continues.
    rules()
    while flag == 0:
        difficulty = input("Choose a difficulty:\n1. Easy\n2. Hard\n3. Devious\nEnter a number: ")
        if difficulty.isdigit() == False:
            print("Not an integer! Try again.")
            print("==============================================")
        else:
            difficulty = int(difficulty)
            if (difficulty == 1 or difficulty == 2 or difficulty == 3):
                flag = 1
            else:
                print("Must be a number between 1 and 3! Try again.")
                print("==============================================")

    numOfTurns = 0
    drawFromDeck = 0
    avgRequestsCorrect = 0

    #go to the corresponding function based on what they chose.
    if difficulty == 1:
        print("You chose easy mode.\n")
        numOfTurns, drawFromDeck, avgRequestsCorrect = easy(numToDraw, deck, playerHandArray, computerHandArray, numOfTurns, drawFromDeck, avgRequestsCorrect)
    elif difficulty == 2:
        print("You chose hard mode.\n")
        numOfTurns, drawFromDeck, avgRequestsCorrect = hard(numToDraw, deck, playerHandArray, computerHandArray, numOfTurns, drawFromDeck, avgRequestsCorrect)
    elif difficulty == 3:
        print("You chose devious mode.\n")
        numOfTurns, drawFromDeck, avgRequestsCorrect = devious(numToDraw, deck, playerHandArray, computerHandArray, numOfTurns, drawFromDeck, avgRequestsCorrect)

    print("\nSome statistics of interest:")
    print("Number of turns:", numOfTurns)
    print("Number of books acquired through drawing from the deck:", drawFromDeck)
    print("Percentage of correct guesses:", avgRequestsCorrect/numOfTurns)

main()
