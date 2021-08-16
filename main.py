#!/usr/bin/python
"""Main script for Game Simulator."""

import asyncio
import logging
import sys
import random

rooms = ["Bedroom", "Office", "Bathroom", "Kitchen", "Garage", "Back Patio", "Living Room", "Fancy Room"]
players = ["Player 1", "Player 2", "Player 3", "Player 4"]
assignment = ["Crew", "Crew", "Crew", "Imposter"]

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def draw_card():
    room = rooms.pop(1)
    return room
    logging.info(room)


def main():
    logging.info("Enter players.")
    logging.info(players)

    logging.info("Shuffle Cards")
    random.shuffle(rooms)

    logging.info("Make Assignments")
    random.shuffle(assignment)
    logging.info(assignment)

        
    room = draw_card()
    


if __name__ == "__main__":
    logging.info("Starting script")
    

    main()
    
    logging.info(rooms)