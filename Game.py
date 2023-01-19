from Deck import CardDeck
from Deck import Card
from Deck import Res


class Game():
    def __init__(self):
        self.coal = 0
        self.oil = 0
        self.steel = 0
        self.tool = 0
        self.coin = 0
        # Cards are stored in a dictionary, definition of each key is a list of two integers
        #       The first int is the number of those cards the player has
        #       The second int is the number of those cards that are advanced
        self.cards = {} # Format: {Card(enum string) : [isUsed, isAdvanced]...}
        self.collected = [] # List of all cards that have been collected from . You will never be able to own these cards
        # Every time a card is played, lastCard is updated. This is used in UnplayLastCard()
        self.lastCard = None
        self.lastCardAdvancement = []
        self.lastTrade1 = 0
        self.lastTrade2 = 0

        self.TurnInProgress = False

    def AdvanceCard(self, card, undo = False):
        if not card in self.cards.keys():
            return False
        if self.cards[card][1] == 1 - undo:
            print("Tried to advance {} but it was already advanced!".format(card))
            return False
        if self.IsPersonalCard(card):
            print("Cannot advance {} because it is a personal card".format(card))
            return False
        self.cards[card][1] = 1 - undo
        return True

    def SetLastCard(self, Card):
        self.lastCard = Card

    def ClearLastCard(self):
        self.lastCard = None

    def PlayCardBase(self, *args, **kwargs):
        for arg in args:
            # Make sure this card is in their hand
            if not arg in self.cards:
                print('Tried to play {} but it is not in your hand! Skipping...'.format(arg))
                continue
            if self.cards[arg][0]:
                print('Tried to play {} but it has already been played. Skipping...'.format(arg))
                continue
            # Mark the card as played
            self.cards[arg][0] = True
            # Determine if it is a personal card or not, then play the card
            status = False
            if self.IsPersonalCard(arg):
                status = self.PersonalCard(arg, **kwargs)
            else:
                status = self.Card(arg, **kwargs)
            if status:
                self.SetLastCard(arg)

    def UndoLastCardBase(self):
        if self.lastCard == None:
            print("No last card found.")
        if self.IsPersonalCard(self.lastCard):
            status = self.UnplayPersonalCard(self.lastCard)
        else:
            status = self.Card(self.lastCard, undo=True)
        if status:
            self.cards[self.lastCard][0] = False

        # Check if there are any cards that were advanced
        # print('unplaying card {}, lastCardAdvance: {}'.format(self.lastCard, self.lastCardAdvancement))
        # for i in range(len(self.lastCardAdvancement)):
        #     self.cards[self.lastCardAdvancement[i]][1] = False
        #     print('Undoing advancement of card {}'.format(self.lastCardAdvancement[i]))
        self.lastCardAdvancement = []
        self.lastTrade1 = 0
        self.lastTrade2 = 0
        return status

    def Collect(self, card, count):
        '''
        Call this when you are collecting resources from a given card
        :param card: Card ID
        :param count: The number of times to perform the transation
        :return:
        '''
        if self.TurnInProgress:
            print("You cannot collect from a card if your turn is in progress.")
            return
        if card in self.cards.keys():
            print("You cannot collect resources from a card that is in your hand.")
            return
        if count > 3:
            count = 3
        # Validate the transaction
        for i in range(count):
            if not self.Trade(CardDeck[card]['ResourceSource'], CardDeck[card]['ResourceValue']):
                print("Insufficient funds on transaction {}".format(i))
                return
            else:
                self.collected.append(card)
        print('Collection Complete...')

    def PayResource(self, Source, undo=False):
        if not undo:
            if self.oil >= Source.oil and self.coal >= Source.coal and self.tool >= Source.tool and self.steel >= Source.steel:
                self.oil -= Source.oil
                self.coal -= Source.coal
                self.tool -= Source.tool
                self.steel -= Source.steel
                self.coin -= Source.coin
                return True
        else:
            self.oil += Source.oil
            self.coal += Source.coal
            self.tool += Source.tool
            self.steel += Source.steel
            self.coin += Source.coin
            return True
        return False

    def Trade(self, Source, Value):
        if self.PayResource(Source):
            self.oil += Value.oil
            self.coal += Value.coal
            self.tool += Value.tool
            self.coin += Value.coin
            self.steel += Value.steel
            self.PrintTransaction(Source, Value, True)
            return True
        self.PrintTransaction(Source, Value, False)
        return False

    def CollectFromCard(self, card):
        self.Collect(card)

    def Card(self, card, undo=False, **kwargs):
        '''
        Perform the trades on a regular card
        :param card: Card ID
        :param kwargs: 'trade1', 't1', 'trade2 or 't2' being equal to int
        :return:
        '''
        if not card in self.cards.keys():
            return False
        # Get the first transaction count
        trade1 = CardDeck[card]['PrimaryCount']
        t1Args = ['t', 't1', 'T', 'T1', 'trade', 'trade1', 'Trade1', 'Trade']
        pSource = CardDeck[card]['PrimarySource']
        pValue = CardDeck[card]['PrimaryValue']
        if undo: # If we are unduing a card, switch the source and value so the trade goes backward
            pSource = pValue
            pValue = CardDeck[card]['PrimarySource']
        for a in t1Args:
            if a in kwargs.keys():
                trade1 = kwargs[a]
                break
        if undo:
            trade1 = self.lastTrade1
        # Validate the first trade
        self.lastTrade1 = 0
        for i in range(trade1):
            if not self.Trade(pSource, pValue):
                break
            else:
                self.lastTrade1 += 1

        # Check if the card is advanced
        if self.cards[card][1] == False:
            # Card is not advanced, return
            return True

        trade2 = CardDeck[card]['AdvancedCount']
        t2Args = ['t2', 'T2', 'trade2', 'Trade2']
        aSource = CardDeck[card]['AdvancedSource']
        aValue = CardDeck[card]['AdvancedValue']
        if undo:
            aSource = aValue
            aValue = CardDeck[card]['AdvancedSource']
        for a in t2Args:
            if a in kwargs.keys():
                trade2 = kwargs[a]
                break
        if undo:
            trade2 = self.lastTrade2
        # Validate the trade
        self.lastTrade2 = 0;
        for i in range(trade2):
            if not self.Trade(aSource, aValue):
                break
            else:
                self.lastTrade2 += 1
        return True

    def PersonalCard(self, card, **kwargs):
        '''
        Perform the trades on a personal card
        :param card: Card ID
        :param kwargs: 'trade' or 't' being equal to a number will perform that many trades (but clamped at the limit)
                                    If not specified, do the max.
                        'advance' or 'a' or 'adv' being equal to a list of card IDs will advance each card in order until resources run out
        :return:
        '''
        if not card in self.cards.keys():
            print('Tried to play personal card {} but it is not in your hand!'.format(card))
            return False
        # Add the tool
        self.tool += 1
        # Determine specs of first trade
        trade1 = CardDeck[card]['PrimaryCount']
        tradeArgs = ['t', 't1', 'T', 'T1', 'trade', 'trade1', 'Trade1', 'Trade']
        for a in tradeArgs:
            if a in kwargs.keys():
                trade1 = kwargs[a]
                break
        pSource = CardDeck[card]['PrimarySource']
        pValue = CardDeck[card]['PrimaryValue']

        self.lastTrade1 = 0
        # Validate the first trade
        for i in range(trade1):
            if not self.Trade(pSource, pValue):
                break
            else:
                self.lastTrade1 += 1

        # do card advancements
        adv = []
        advArgs = ['a', 'adv', 'advance', 'A', 'Adv', 'Advance']
        for a in advArgs:
            if a in kwargs.keys():
                adv=kwargs[a]
                break
        # Validate the trades
        for i in range(len(adv)):
            if self.IsCardAdvanced(adv[i]):
                print("You tried to advance {} but it is already advanced!".format(adv[i]))
            else:
                if self.PayToAdvance(CardDeck[card]['AdvancedSource'], adv[i]):
                    self.lastCardAdvancement.append(adv[i])
                    print("Card {} is now advanced!".format(adv[i]))
                    print('Advanced cards: {}'.format(self.lastCardAdvancement))
        return True

    def UnplayPersonalCard(self, card, **kwargs):
        # Prep to undo first trade
        pValue = CardDeck[card]['PrimarySource']
        pSource = CardDeck[card]['PrimaryValue']
        self.ShowRes()
        for i in range(self.lastTrade1):
            self.Trade(pSource, pValue)

        # Undo one transaction for each card in the lastCardAdvanced list
        for i in range(len(self.lastCardAdvancement)):
            self.ShowRes()
            self.Trade(Res(), CardDeck[card]['AdvancedSource'])
            self.ShowRes()
            self.cards[self.lastCardAdvancement[i]][1] = False

        # Get rid of the tool
        self.tool -= 1
        return True

    def PayToAdvance(self, Source, Card, undo=False):
        advance = self.AdvanceCard(Card, undo)
        if advance:
            if self.PayResource(Source, undo):
                self.PrintAdvance(Source, Card, True)
                return True
            else:
                self.cards[Card][1] = False # Funds were insufficient, changing status back
                self.PrintAdvance(Source, Card, False)
                return False
        return False

    def clamp(self, tradeCount, tradeLimit):
        if tradeCount < 0:
            tradeCount = 0
        if tradeCount > tradeLimit:
            return tradeLimit
        else:
            return tradeCount

    def Validate(self, **kwargs):
        coalArgs = ['coal', 'c', 'Coal']
        steelArgs = ['steel', 's', 'Steel']
        oilArgs = ['oil', 'o', 'Oil']
        toolArgs = ['tool', 't', 'Tool']
        for a in coalArgs:
            if a in kwargs.keys():
                val = kwargs[a]
                if val < self.coal:
                    return False
        for a in steelArgs:
            if a in kwargs.keys():
                val = kwargs[a]
                if val < self.steel:
                    return False
        for a in oilArgs:
            if a in kwargs.keys():
                val = kwargs[a]
                if val < self.oil:
                    return False
        for a in toolArgs:
            if a in kwargs.keys():
                val = kwargs[a]
                if val < self.tool:
                    return False
        return True

    def ValidateTransaction(self, Source, Count = 1):
        if Source.IsNotEmpty():
            if Source.oil * Count < self.oil:
                return False
            if Source.coal * Count < self.coal:
                return False
            if Source.steel * Count < self.steel:
                return False
            if Source.tool * Count < self.tool:
                return False
        return True

    def IsCardAdvanced(self, Card):
        if not Card in self.cards.keys():
            return False
        return self.cards[Card][1]

    def IsPersonalCard(self, card):
        return 'p' in card.value

    def TransactionString(self, Data):
        data = '['
        hasFirst = False
        if Data.oil:
            if hasFirst:
                data = data + ', '
            data = data + 'oil: {}'.format(Data.oil)
            hasFirst = True
        if Data.coal:
            if hasFirst:
                data = data + ', '
            data = data + 'coal: {}'.format(Data.coal)
            hasFirst = True
        if Data.steel:
            if hasFirst:
                data = data + ', '
            data = data + 'steel: {}'.format(Data.steel)
            hasFirst = True
        if Data.tool:
            if hasFirst:
                data = data + ', '
            data = data + 'tool: {}'.format(Data.tool)
        if Data.coin:
            if hasFirst:
                data = data + ', '
            data = data + 'coin: {}'.format(Data.coin)
            hasFirst = True

        return data + ']'

    def PrintTransaction(self, Source, Value, Approved):
        approvedStr = "COMPLETE"
        if not Approved:
            approvedStr = "DENIED"
        outStr = 'Performing Trade: Paying:{}, Receiving:{}, Status:{}'.format(
            self.TransactionString(Source),
            self.TransactionString(Value),
            approvedStr)
        print(outStr)

    def PrintAdvance(self, Source, Card, Approved):
        approvedStr = "COMPLETE"
        if not Approved:
            approvedStr = "DENIED"
        outStr = "Performing Card Advancement: Paying:{}, Card To Advance:{}, Status:{}".format(
            self.TransactionString(Source), Card, approvedStr)
        print(outStr)

    def ShowRes(self):
        print('Coal: {}, Steel: {}, Oil: {}, Tool: {}, Coin: {}'.format(self.coal, self.steel, self.oil, self.tool, self.coin))

    def ShowResources(self):
        self.ShowRes()