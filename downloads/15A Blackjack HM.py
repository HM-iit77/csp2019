import time
import random

class Card():
    index = 0
    number = 0
    suit = ""
    name = ""
    displayName = ""
    hasAce = False

#15A - Blackjack
# (will start immediately on run by default)
# This method covers both the player's and the dealer's turns (abstraction)
def blackJack(isDealer, pastScore, drawnCards):
    subject = ""
    if isDealer:
        subject = "The dealer's"
        print("It's the dealer's turn.")
    else:
        subject = "Your"
        print("Shuffling...")
        time.sleep(3)
        print("It's your turn.")
    time.sleep(1)
    currentScore = 0
    hasAce = False
    turnStand = False
    # special handling for beginning: draw two cards at once
    firstCard = drawCard(drawnCards)
    drawnCards.append(firstCard)
    hasAce = firstCard.hasAce
    secondCard = drawCard(drawnCards)
    drawnCards.append(secondCard)
    if hasAce == False:
        hasAce = secondCard.hasAce
    print(subject + " first two cards are " + firstCard.displayName + " and " + secondCard.displayName + ".")
    time.sleep(2)
    currentScore = firstCard.number + secondCard.number
    if hasAce == False:
        print(subject + " score is " + str(currentScore) + ".")
    # separate handles for having one or two aces
    # on the off-chance there are two aces, the score will be 2, since 11 + 11 = 22
    elif firstCard.hasAce and secondCard.hasAce:
        print(subject + " score is " + str(currentScore) + ".")
        hasAce = False
    # if there is one ace, report the score as two alternatives
    else:
        print(subject + " score is either " + str(currentScore) + " or " + str(currentScore + 10) + ".")
    if currentScore >= 21 or (hasAce and (currentScore + 10) == 21):
        turnStand = True
    elif isDealer:
        if currentScore >= 17 or (hasAce and (((currentScore + 10) >= 17) or ((currentScore + 10) >= 17)) or (currentScore > pastScore)):
            turnStand = True
    # Turn as long as dealer/player does not stand/go to or over 21
    time.sleep(1)
    while turnStand == False:
        if isDealer:
            print("The dealer hits.")
        else:
            choiceMade = False
            while choiceMade == False:
                print("Will you stand or hit?")
                time.sleep(1)
                print("stand")
                print("hit")
                choice = raw_input()
                if choice == "stand" or choice == "hit":
                    choiceMade = True
                else:
                    print("Please choose a valid decision.")
                    time.sleep(1)
            if choice == "stand":
                break
        time.sleep(1)
        drawnCard = drawCard(drawnCards)
        drawnCards.append(drawnCard)
        print(subject + " drawn card is " + drawnCard.displayName + ".")
        time.sleep(1)
        currentScore += drawnCard.number
        # update hasAce if none of the drawnCards have aces
        if hasAce == False:
            hasAce = drawnCard.hasAce
        # check a second time with the updated hasAce
        if hasAce == False:
            print(subject + " score is " + str(currentScore) + ".")
        else:
            # if the score is greater than 21 when Ace is 11, we will not consider it as an option.
            if (currentScore + 10) <= 21:
                print(subject + " score is either " + str(currentScore) + " or " + str(currentScore + 10) + ".")
                if (currentScore + 10) == 21:
                    turnStand = True
            else:
                print(subject + " score is " + str(currentScore) + ".")
                hasAce = False
        # loop will end if the player's score is at/over 21 or the dealer's score is at/above 17 OR the dealer's score is higher than the player's
        # the dealer stands at 17 or higher due to the risk of busting.  If a dealer busts, they will lose twice the bet in a normal Blackjack game
        if currentScore >= 21 or (isDealer and (currentScore >= 17 or currentScore > pastScore)):
                turnStand = True
        time.sleep(1)
    if currentScore == 21 or (hasAce and (currentScore + 10) == 21):
        if isDealer:
            print("The dealer got a Blackjack!  You lose!")
        else:
            print("Blackjack!  You win!")
    elif currentScore > 21:
        if isDealer:
            print("The dealer busted!  You win!")
        else:
            print("You busted!  You lose!")
    else:
        if hasAce:
            if isDealer:
                print("The dealer chose to stand at " + str(currentScore+10) + ".")
            else:
                print("You chose to stand at " + str(currentScore+10) + ".")
                blackJack(True, (currentScore+10), drawnCards)
        else:
            if isDealer:
                print("The dealer chose to stand at " + str(currentScore) + ".")
            else:
                print("You chose to stand at " + str(currentScore) + ".")
                blackJack(True, currentScore, drawnCards)
        if currentScore > pastScore or (hasAce and ((currentScore + 10) > pastScore)):
            print("The dealer has the higher score!  You lose!")
        elif currentScore == pastScore or (hasAce and ((currentScore + 10) == pastScore)):
            print("Your scores tied!  Nobody wins!")
        elif currentScore < pastScore or (hasAce and ((currentScore + 10) < pastScore)):
            print("You have the higher score!  You win!")
    decided = False
    while decided == False:
        print("Press y to play again.")
        choice = raw_input()
        if choice == "y":
            decided = True
    blackJack(False, 0, [])

def drawCard(drawnCards):
    # generate cards until a card that is not in play is created
    cardPicked = False
    while cardPicked == False:
        pickedCard = createCard()
        if len(drawnCards) == 0:
            cardPicked = True
        else:
            for drawnCard in drawnCards:
                if drawnCard.index == pickedCard.index:
                    return drawCard(drawnCards)
            cardPicked = True
    return pickedCard

def createCard():
    card = Card()
    card.index = random.randint(1, 52)
    # determine suit
    if card.index <= 13:
        card.suit = "Diamonds"
    elif card.index <= 26:
        card.suit = "Hearts"
    elif card.index <= 39:
        card.suit = "Spades"
    else:
        card.suit = "Clubs"
    # determine number
    if card.suit == "Clubs":
        card.number = card.index - 39
    elif card.suit == "Spades":
        card.number = card.index - 26
    elif card.suit == "Hearts":
        card.number = card.index - 13
    else:
        card.number = card.index
    # determine if card is special
    # most versions of Blackjack treat royalty cards as being worth 10
    # ace is worth either 1 or 11 depending on the state of the player's deck; will be calculated later
    if card.number == 11:
        name = "Jack"
        card.number = 10
    elif card.number == 12:
        name = "Queen"
        card.number = 10
    elif card.number == 13:
        name = "King"
        card.number = 10
    elif card.number == 1:
        name = "Ace"
        card.hasAce = True
    else:
        name = (str)(card.number)
    # determine card display name
    card.displayName = name + " of " + card.suit
    return card

blackJack(False, 0, [])