#!/usr/bin/python
"""Main script for Game Simulator."""

import asyncio
import logging
import sys
import random

rooms = ["Bedroom", "Office", "Bathroom", "Kitchen", "Garage", "Back Patio", "Living Room", "Fancy Room"]
players = ["Player 1", "Player 2", "Player 3", "Player 4"]
assignment = ["Crew", "Crew", "Crew", "Imposter"]
positions = {}

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def draw_card():
    room = rooms.pop(0)
    return room
    logging.info(room)

def move_to_room(player, room):
    # if player in positions:
    #     positions[player] = room
    # else:
    #     positions[player] = room

    positions[player] = room



def main():
    logging.info("Enter players.")
    logging.info(players)

    logging.info("Shuffle Cards")
    random.shuffle(rooms)
    logging.info(rooms)

    logging.info("Make Assignments")
    random.shuffle(assignment)
    logging.info(assignment)

    for player in players:    
        room = draw_card()
        move_to_room(player, room)

    logging.info("Positions after Turn")
    logging.info(positions)


    logging.info("Remaining Cards")
    logging.info(rooms)

    


if __name__ == "__main__":
    logging.info("Starting script")
    

    main()
    
    