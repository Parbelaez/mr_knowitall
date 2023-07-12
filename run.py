import random
import gspread
from time import sleep
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
    """
    Create a pseudo-random number between 1 and 6
    to emulate the rolling of dices.
    """
    loading = [
        "[        ]",
        "[>       ]",
        "[>>      ]",
        "[>>>     ]",
        "[>>>>    ]",
        "[>>>>>   ]",
        "[>>>>>>  ]",
        "[>>>>>>> ]",
        "[>>>>>>>>]",
        "[ >>>>>>>]",
        "[  >>>>>>]",
        "[   >>>>>]",
        "[    >>>>]",
        "[     >>>]",
        "[      >>]",
        "[       >]",
        "[        ]",
        "[       <]",
        "[      <<]",
        "[     <<<]",
        "[    <<<<]",
        "[   <<<<<]",
        "[  <<<<<<]",
        "[ <<<<<<<]",
        "[<<<<<<<<]",
        "[<<<<<<< ]",
        "[<<<<<<  ]",
        "[<<<<<   ]",
        "[<<<<    ]",
        "[<<<     ]",
        "[<<      ]",
        "[<       ]"
        ]
    for i in range(100):
        print(loading[i % len(loading)], end="\r")
        sleep(0.025)
        i += 1
    # trunk-ignore(bandit/B311)
    dice_1 = random.randint(1,6)
    # trunk-ignore(bandit/B311)
    dice_2 = random.randint(1,6)
    return [dice_1, dice_2]

def create_players():
    players = []
    num_of_players = 0
    valid_data = False
    
    while valid_data is False:
        num_of_players = input("Please,enter the number of players (1 to 4): ")
        try:
            int(num_of_players)
            if int(num_of_players) < 1 or int(num_of_players) > 4:
                raise ValueError(
                    f'Please, enter a number between 1 and 4. You privided {num_of_players}'
                    )
            else:
                for player_n in range(0, int(num_of_players)):
                    players.append(input(f'Please, enter the name of player {player_n+1}: '))
                valid_data = True
        except ValueError as e:
            print(f'Invalid data: {e}, please try again.\n')
    return players

def get_question(dices,category):
    category_sheet = SHEET.worksheet(category)
    # trunk-ignore(bandit/B311)
    question = category_sheet.row_values(random.randint(2,11))
    print(f'{question[0]}\n\n',
          'Your answer options are:\n\n',
          f'A: {question[1]}\n',
          f'B: {question[2]}\n',
          f'C: {question[3]}\n',
          f'D: {question[4]}\n',)

def start_timer():
    print('You have 10 seconds to answer')

def main():
    category = ['General Knowledge','Art','History','Geography','Sports','Math']
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
          "\t6. Math (for which you will have 10s)\n\n",
          "- If your answer is correct, you will get the points from dice 2.\n",
          "- If your answer a math question correctly in less than 5 seconds, you will get double the points.\n",
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
            print("\033c")
            print(f'Dice 1: {dices[0]} , Dice 2: {dices[1]}')
            print(f'Category: {category[dices[0]-1]} and you will be able to get {dices[1]} points.\n')
            get_question(dices,category[dices[0]-1])
            start_timer()

main()