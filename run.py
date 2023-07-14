import random
import gspread
from time import sleep, gmtime, strftime
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

def create_players():
    """
    Create the players and insert them in the sheet.
    The players are created using the input data from the user
    and getting the timestamp of the creation.
    The results will be updated in the calculate_score function.
    """
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
                    player_name = input(f'Please, enter the name of player {player_n+1}: ')
                    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    player = {
                        "name" : player_name,
                        "creation_timestamp" : timestamp
                    }
                    players.append(player)
                    data = [player_name,timestamp,0,0,0,0,0,0,0,0,0,0,0,0]
                    SHEET.worksheet('players').append_row(data)
                valid_data = True
        except ValueError as e:
            print(f'Invalid data: {e}, please try again.\n')
    return players

def throw_dices():
    """
    Create a pseudo-random number between 1 and 6
    to emulate the rolling of dices.
    """
    #Create the art of the throwing of the dices process
    #This animation is a modification of https://stackoverflow.com/questions/7039114/waiting-animation-in-command-prompt-python

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

def get_question(dices,category):
    """
    Use the dice 1 result to select the category.
    On the sheet, the correct result is always at the first column,
    therefore the answers are shown in random order.
    """
    category_sheet = SHEET.worksheet(category)
    # trunk-ignore(bandit/B311)
    question = category_sheet.row_values(random.randint(2,11))
    #Creates a list of unordered numbers from a 1 to 4 range
    one_to_four = random.sample([1,2,3,4],4)
    options = {
        'option_' + str(one_to_four[0]) : 'A',
        'option_' + str(one_to_four[1]) : 'B',
        'option_' + str(one_to_four[2]) : 'C',
        'option_' + str(one_to_four[3]) : 'D'
    }
    #Dictionary needes to translate the option into a correct answer
    print(f'{question[0]}\n\n',
          'Your answer options are:\n\n',
          f'A: {question[one_to_four[0]]}\n',
          f'B: {question[one_to_four[1]]}\n',
          f'C: {question[one_to_four[2]]}\n',
          f'D: {question[one_to_four[3]]}\n',)
    #Returns the correct answer
    return (options['option_1'])

def get_answer(correct_answer):
    answer = ''
    options = ['a', 'b', 'c', 'd']
    while (not options.count(answer)):
        try:
            answer = input('Please, choose your answer (a, b, c, or d): ')
            if (options.count(answer)):
               if (answer.upper() == correct_answer):
                   print('Correct!')
                   return(True)
               else:
                   print('Sorry! Your answer was wrong.')
                   return(False)
            else:
                raise ValueError(
                    f'Please, enter an option from the list (a, b, c, d). You privided {answer}'
                    )
        except ValueError as e:
            print(f'Invalid data: {e}, please try again.\n')

# TODO: refactor... categories in a list and only 1 update routine

def calculate_score(category,correct,player,dice):
    """
    Take the category and looks for the previous score values for correct and incorrect.
    Sum the dice 2 result to the previous score.
    Calculate the new total and returns the value.
    """
    if(correct):
        match category:
            case 'General Knowledge':
                column = 3
            case 'Art':
                column = 5
            case 'History':
                column = 7
            case 'Geography':
                column = 9
            case 'Sports':
                column = 11
            case 'Math':
                column = 13
        previous_result = SHEET.worksheet('players').cell(player + 2, column).value
        if(previous_result is None):
            print(player + 2, column, dice)
            SHEET.worksheet('players').update_cell(player + 2, column, dice) #!deprecated in version 6.0.0 of gspread
        else:
            SHEET.worksheet('players').update_cell(player + 2, column, int(previous_result) + dice) #!deprecated in version 6.0.0 of gspread
        scores_row = SHEET.worksheet('players').row_values(player+2)
        new_total_correct = 0
        for i in range(3, len(scores_row), 2):
            new_total_correct += int(scores_row[i-1])
        return(new_total_correct)

    else:
        match category:
            case 'General Knowledge':
                column = 4
            case 'Art':
                column = 6
            case 'History':
                column = 8
            case 'Geography':
                column = 10
            case 'Sports':
                column = 12
            case 'Math':
                column = 14
        results_cell = column + str(player+2)
        previous_result = SHEET.worksheet('players').acell(results_cell).value
        if(previous_result is None):
            SHEET.worksheet('players').update(results_cell, dice) #!deprecated in version 6.0.0 of gspread
        else:
            SHEET.worksheet('players').update(results_cell, int(previous_result) + dice) #!deprecated in version 6.0.0 of gspread
    return(None)

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
    print("\nOk. Let's play!\n")
    while True:
        for player_num in range(len(players)):
            print(f'It is {players[player_num]["name"]} turn.')
            y_key = ""
            while  y_key != "y":
                y_key = input('Press "y" to throw the dices: ')
            dices = throw_dices()
            print("\033c")
            print(f'Dice 1: {dices[0]} , Dice 2: {dices[1]}')
            print(f'Category: {category[dices[0]-1]} and you will be able to get {dices[1]} points.\n')
            correct_answer = get_question(dices,category[dices[0]-1])
            #start_timer()
            correct = get_answer(correct_answer)
            new_score = calculate_score(category[dices[0]-1],correct,player_num, dices[1])
            print(new_score)
            if new_score >= 50:
                print(f'{players[player_num]["name"]}, you won! CONGRATULATIONS!\n')
                break

main()