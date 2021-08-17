#!/usr/bin/python
"""Main script for Game Simulator."""

import asyncio
import logging
import sys
import random

NUM_ROOM_CARDS = 2

rooms = ["Bedroom", "Office", "Bathroom", "Kitchen", "Garage", "Back Patio", "Living Room", "Fancy Room"]
deck = []
discard_pile = []
players = ["Player 1", "Player 2", "Player 3", "Player 4"]
cur_player_idx = 0
ghosts = []
assignment = ["Crew", "Crew", "Crew", "Imposter"]

positions = {}
imposter = None

card_log = []

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def create_deck(rooms):

    for _ in range(NUM_ROOM_CARDS):
        for room in rooms:
            deck.append(room)

def draw_card():
    card = deck.pop(0)
    discard_pile.append(card)
    card_log.append(card)
    return card

def move_to_room(player, room):
    positions[player] = room


def is_imposter(player):
    idx = players.index(player)
    return assignment[idx] == "Imposter"

def get_player_in_my_room(player):

    targets = []

    if player in positions:
        my_room = positions[player]

        for p, r in positions.items():
            if r == my_room and p != player:
                targets.append(p)

    return targets
        

def kill_player(player):
    if player not in ghosts:
        ghosts.append(player)
        positions[player] = "Grave"
        

def call_emergency_meeting():
    if imposter and len(players) > 1:
        positions[imposter] = "Space"

def take_action(player):

    if player in positions:

        targets = get_player_in_my_room(player)
        if len(targets) > 0:
            if is_imposter(player):
                if targets[0] != "Body":
                    logging.debug("Imposter taking action.")          
                    kill_player(targets[0])
                    imposter = player
                    logging.info(f"{player} killed {targets[0]}")
            else:
                if targets[0] == "Body":
                    logging.debug("Crew taking action.")
                    logging.info(f"{player} found a body!")
                    if len(ghosts) > 0:
                        call_emergency_meeting()

        else:
            logging.debug(f"No target in the room.") 

    else:
        logging.debug(f"{player} not in a room.")
    

def active_players():
    global cur_player_idx

    keep_searching = True
    while keep_searching:

        player = players[cur_player_idx]

        keep_searching = player in ghosts 

        # Increment index
        cur_player_idx = cur_player_idx + 1
        if cur_player_idx >= len(players):
            cur_player_idx = 0  

    yield player

def main():
    logging.debug("Enter players.")
    logging.debug(players)

    logging.debug("Create Deck")
    create_deck(rooms)
    logging.debug("Shuffle Cards")
    random.shuffle(deck)
    logging.info(deck)

    logging.debug("Make Assignments")
    random.shuffle(assignment)
    logging.info(assignment)

    logging.debug("Add body to game")
    move_to_room("Body", random.choice(rooms))


    turn_count = 0
    while len(deck) > 0:

        logging.debug(f"Turn {turn_count}")

        for player in active_players():   

            # Take Action
            take_action(player)

            room = draw_card()
            logging.info(f"{player} drew {room}.")
            move_to_room(player, room)

            # Take Action
            take_action(player)
        

        logging.debug("Positions after Turn")
        logging.debug(positions)


        logging.debug("Remaining Cards")
        logging.debug(deck)
        turn_count = turn_count + 1

        if imposter and (positions[imposter] == "Space"):
            break


    logging.info(f"Ghosts {ghosts}")

    if imposter and (positions[imposter] == "Space"):
        winner = "Crew!!"
    if (len(players) == (len(ghosts) + 1)):
        winner = "Imposter!!" 
    else:
        winner = "No Winner"

    logging.info(f"{winner} with: \nplayers: {players}\nassignments: {assignment}\ndeck: {card_log}\npositions:  {positions}\nghosts: {ghosts}\nimposter: {imposter}")
    



if __name__ == "__main__":
    logging.debug("Starting script")
    

    main()
    
    