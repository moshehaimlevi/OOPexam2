from enum import Enum
from functools import wraps
import random

class Card:
    class CardSuit(Enum):
        SPADES = 1
        HEARTS = 2
        DIAMONDS = 3
        CLUBS = 4

    class CardRank(Enum):
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK = 11
        QUEEN = 12
        KING = 13
        ACE = 14

    def __init__(self, suit: 'Card.CardSuit', rank: 'Card.CardRank'):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def get_display_name(self):
        return f"{self._rank.name.title()} of {self._suit.name.title()}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self._rank == other._rank and self._suit == other._suit

    def __lt__(self, other):   # Less-than comparison
        if not isinstance(other, Card):
            return NotImplemented
        if self._rank.value != other._rank.value:
            return self._rank.value < other._rank.value
        return self._suit.value < other._suit.value

    def __gt__(self, other):        # Greater-than comparison, based on rank first, then suit
        if not isinstance(other, Card):
            return NotImplemented
        if self._rank.value != other._rank.value:
            return self._rank.value > other._rank.value
        return self._suit.value > other._suit.value

    def __hash__(self):
        return hash((self._suit, self._rank))

    def __str__(self):
        return self.get_display_name()

    def __repr__(self):
        return f"Card(suit={self._suit.name}, rank={self._rank.name})"


class Deck:          # Initializes a deck
    def __init__(self, shuffle=True):
        self._cards = self._generate_full_deck()
        if shuffle:
            self.shuffle()

    def _generate_full_deck(self):      # Generates a full deck of 52 cards
        return [
            Card(suit, rank)
            for suit in Card.CardSuit
            for rank in Card.CardRank
        ]

    @property
    def cards(self):
        return self._cards.copy()

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self):
        return self._cards.pop(0) if self._cards else None

    def add_card(self, card):
        self._cards.append(card)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):      # Allows indexing into the deck like a list
        return self._cards[index]

    def __iter__(self):       # Makes the deck iterable
        return iter(self._cards)

    def max(self):
        return max(self._cards, default=None)

    def min(self):
        return min(self._cards, default=None)

# Custom exception for detecting cheating in the deck
class DeckCheatingError(Exception):
    """Exception raised!!!! deck manipulation or cheating is suspected."""
    pass

# Decorator to validate a deck returned by a function for uniqueness
def fair_deck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, Deck):
            seen = set()
            for card in result:
                if card in seen:
                    raise DeckCheatingError(f"Cheating detected: duplicate card {card}")
                seen.add(card)
        return result

    return wrapper


def main():
    c1 = Card(Card.CardSuit.SPADES, Card.CardRank.ACE)
    c2 = Card(Card.CardSuit.HEARTS, Card.CardRank.KING)
    c3 = Card(Card.CardSuit.SPADES, Card.CardRank.ACE)
    c4 = Card(Card.CardSuit.DIAMONDS, Card.CardRank.EIGHT)

    print(c1)
    print(repr(c2))
    print("equal?", c1 == c3)
    print("(c2 > c1)?:", c2 > c1)
    print("Another card:", c4)
    print("Hash of c4:", hash(c4))


    deck = Deck()
    print("\nDeck details:")
    print("Deck cards:", len(deck))
    print("Max card:", deck.max())
    print("Min card:", deck.min())
    print("5 random cards")
    for i in range(5):
        print(deck[i])

    print(f"\nDeck size: {len(deck)} cards")


    pulled_card = deck.draw()
    print(f"\nPulled card: {pulled_card}")
    print(f"Deck size after draw: {len(deck)} cards")


    deck.add_card(pulled_card)
    print(f"Added card back: {pulled_card}")
    print(f"Deck size after adding back: {len(deck)} cards")

    index = 17
    card_at_index = deck[index]
    print(f"\nCard at index {index}: {card_at_index}")


    print("\n=== Iterating over deck ===")
    for card in deck:
        print(card)

if __name__ == "__main__":
    main()










