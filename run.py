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

def main():
    print("Welcome to the Mr. Know-it-all game!\n",
          "\n",
          "In this game, your knowledge on the General Facts, History, Geography, art, and sport will be evaluated.\n\n",
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
          "- The game is won when any of the players reaches 100 points.\n")

main()