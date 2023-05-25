
from enum import Enum
import os
import pickle
from random import randint
import re
import sys
from datetime import datetime


class Difficulty(Enum):
    EASY = 10
    MEDIUM = 20
    HARD = 30
class Score():
    def __init__(self, attempts:int = None, difficulty:Difficulty = None):
        self.score = 100 * (difficulty.value // attempts + 1) if attempts else 0
        self.difficulty = difficulty
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
class Player():
    _path = "data.bin"
    def __init__(self, username:str):
        self.username = username
        self._max_score = Score()
        self._index = None
        self.save()

    def set_score(self, score:Score):
        if score.score > self._max_score.score:
            self._max_score = score
            self.save()

    def get_score(self) -> Score:
        return self._max_score
    
    @staticmethod
    def get_all_players()-> list:
        if os.path.exists(Player._path):
            with open(Player._path, "rb") as file:
                return pickle.load(file)
        else:
            with open(Player._path, "wb") as file:
                pickle.dump([], file)
                return []

    def save(self):

        players = Player.get_all_players()
        if self._index != None:
            players[self._index] = self
        else:
            self._index = len(players)
            players.append(self)
        with open(self._path, "wb") as file:
            pickle.dump(players, file)
    
    @staticmethod
    def find_by_username(username: str):
        players = Player.get_all_players()
        filtered = [player for player in players if player.username == username] if players else []
        return filtered[0] if filtered else None

class GuestYourNumber:
    def __init__(self, player:Player , difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.player = player
    
    def run(self):
        os.system("cls")        
        self.number = randint(1, self.difficulty.value)
        attempts = 0
        win = False
        while not win:
            guess = input(f"Please write your guess (1-{self.difficulty.value}):")
            match = re.search("\d{1,"+f"{len(str(self.difficulty.value))}"+"}", guess)
            guess = int(match.group()) if match else 0
            attempts += 1
            if guess == self.number:
                win = True
            elif guess < self.number:
                print("Too low")
            else:
                print("Too high")
        current_score = Score(attempts, self.difficulty)
        self.player.set_score(current_score)
        print(f"You win with {attempts} attempts, your score is {current_score.score}")
        choice = input("Try again? (y/n): ")

        options = {
            "y": self.run
        }
        match = re.search("y", choice.lower())
        if match:
            options.get(match.group(), Menu().main)()
        Menu().main()

class Menu():
    def credits(self):
        os.system("cls")
        input(
            """
            *****************************************************
            **                   Credits                       **
            *****************************************************
            ** Developed by: Esteban Cabarcas                  **
            ** GitHub user: escahe                             **
            ** Date: 24-05-2023                                **
            ** Summary: Game developed as a practical exercise **
            **          during the Top Gun Lab program powered **
            **          by Team International                  **
            *****************************************************
            press enter to go back to main menu
            """
        )
        self.main()

    def main(self):
        os.system("cls")
        options = {
            "1": self.play,
            "2": self.leaderboard,
            "3": self.credits,
            "4": sys.exit
        }
        choice = input(
            """
            **************************************
            ** Welcome To Guess The Number Game **
            **************************************
            **          1. Play                 **
            **          2. Leaderboard          **
            **          3. Credits              **
            **          4. Exit                 **
            **************************************
            write the number of your choice:
            """
        )
        match = re.search("\d", choice)
        if match:
            options.get(match.group(), self.main)()
        self.main()

    def leaderboard(self):
        os.system("cls")
        players = Player.get_all_players()
        print(
            """
            ********************************************************
            **                 Top 10  Leaderboard                **
            ********************************************************
            | rank | username | score | diffic |      datetime     |
            """
        )
        if players:
            players.sort(key= lambda player: player.get_score().score, reverse=True)
            for i in range(len(players)):
                player = players[i]
                score = player.get_score()
                print(f"""            | {i+1}{" "*3 if i<10 else 2} | {player.username}{" "*(8-len(player.username))} | {score.score}{" "*(5-len(str(score.score)))} | {score.difficulty.name}{" "*(6-len(score.difficulty.name))} | {score.date_time} """
                )
                if i == 9:
                    break
        input(""" 
            press enter to go back to main menu:
            """
        )


    def play(self):
        os.system("cls")        
        username = input(
            """
            **************************************
            **             Entrance             **
            **************************************
            write your username:
            """
        )

        player = Player.find_by_username(username)
        if not player:
            player = Player(username)
        os.system("cls")
        choice = input(
            f"""
            **************************************
            **        Choose Difficulty         **
            **************************************
            **            1. Easy               **
            **            2. Medium             **
            **            3. Hard               **
            **************************************
            write the number of your choice:
            """
        )
        options = {
            "1": Difficulty.EASY,
            "2": Difficulty.MEDIUM,
            "3": Difficulty.HARD
        }
        difficulty = Difficulty.EASY        
        match = re.search("\d", choice)
        if match:
            difficulty = options.get(match.group(), difficulty)
        game = GuestYourNumber(player, difficulty)
        game.run()

if __name__ == "__main__":
    Menu().main()