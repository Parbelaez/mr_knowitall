import random
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mr_knowitall')

def throw_dices():
    dice_1 = random.randint(1,6)
    dice_2 = random.randint(1,6)
    return [dice_1, dice_2]

def create_players():
    players = []
    num_of_players = 0
    while int(num_of_players) < 1 or int(num_of_players) > 4:
        num_of_players = input("Please,enter the number of players (1 to 4): ")
        if int(num_of_players) < 1 or int(num_of_players) > 4:
            print("Please, enter a number between 1 and 4")
        else:
            for player_n in range(0, int(num_of_players)):
                players.append(input(f'Please, enter the name of player {player_n+1}: '))
    return players

def main():
    print("Welcome to the Mr. Know-it-all game!\n",
          "\n",
          "In this game, your knowledge on General Facts, History, Geography, art, and sports will be evaluated.\n\n",
          "RULES OF THE GAME:\n\n",
          "- Throw the dices on each turn.\n",
          "- Dice 1 will determine the category of the question:\n",
          "\t1. General Knowledge\n",
          "\t2. Art\n",
          "\t3. History\n",
          "\t4. Geography\n",
          "\t5. Sports\n",
          "\t6. Random (selected from all the previous ones)\n\n",
          "- If your answer is correct, you will get the points from dice 2.\n",
          "- The game is won when any of the players reaches 100 points.\n\n")

    players = create_players()
    print("Ok. Let's play!")
    while True:
        for player_num in range(len(players)):
            print(f'It is {players[player_num]} turn.')
            y_key = ""
            while  y_key != "y":
                y_key = input('Press "y" to throw the dices: ')
            dices = throw_dices()
            print(f'Dice 1: {dices[0]} , Dice 2: {dices[1]}')

main()