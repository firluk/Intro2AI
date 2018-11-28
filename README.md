# Intro to AI
## Primitive poker game AI

[Link to Project Plan](https://github.com/firluk/Intro2AI/projects/1)

#### Some class documentation:  
- **Suit** : provides a generator of card suits, and stores a dictionary of icons for suits
- **Card** : a class with suit and val properties. Has *to_string* method for easy output
- **Deck** : when instantiated, creates and shuffles a 52 card deck. you can then *draw_card* and see how much *cards_left*
- **Hand** : a helper class for **Player** - you can *add_card* and *clear_hand*
- **Player** : contains *name* and *hand*. **Player** can *draw_new_card_from_deck* and *take_card*
- **Game** : contains most game mechanics such as reseting the players hands and advancing the turn