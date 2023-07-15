# Mr. Know-it-all Game

## Introduction

Mr. Know-it-all is a trivia game developed in Python in which the player(s) (up to 4) will answer questions on different topics until one of them reaches a specific score (set by the programmer).

![Mr. Know-it-all UI](./assets/images/mkia_welcome.png)

## Table of contents

- [Rules of the game](#rules-of-the-game)
- [Design](#design)
- [Flow Chart](#flow-chart)
- [User experience (UX)](#user-experience-ux)
  - [User Stories](#user-stories)
  - [Strategy](#strategy)
- [Structure](#structure)
- [Customizable Parameters](#customizable-parameters)
  - [Setting the winning score](#setting-the-winning-score)
  - [Adding new questions](#adding-new-questions)
  - [Leader board (top n)](#leader-board-top-n)

## Rules of the game

The players will throw the dice, and die 1 will determine the category:

    1 = General Knowledge
    2 = Art
    3 = History
    4 = Geography
    5 = Sports
    6 = Math

The second die will determine the points that the player will gain if answers correctly.

After each question, the turn will be passed to the next player.

The game will continue until one of the players get the score stated by the programmer in the [Setting the winning score section](#setting-the-winning-score).

## Design

The design of the game was based on CLI, therefore, one of the goals was to be as clear as possible, so the user would be always aware of how the interaction should take place, namely, what keys or characters should be inserted to play the game and navigate through its segments.

## Flow Chart

![Flow Chart](./assets/images/flowchart.png)

## User experience (UX)

### User Stories

- As a player, I want to:
  - Have clear indications on how to play.
  - Have an easy-to-understand UI.
  - Have the expected inputs from my side which are also non-case sensitive.
  - Display a leaders board, so I can know what the top 5 scores are.

- As a Game Administrator (programmer), I want to:
  - Be able to easily modify the question and their quantity.
  - Be able to easily modify the **winning score**.


### Strategy

## Structure

## Customizable parameters

### Setting the winning score

The winning_score variable at the beginning of the main function will set the number of points that a player should get to be declared as the winner.

![winning_score variable](./assets/images/winning_score.png)

The programmer can change this value according to his/her needs.

**NOTE:** when changing the winning_score variable, remember to update the [welcome.txt](./welcome.txt) file.

### Adding new questions

All new questions are stored in the Google Sheets file, but the file can grow as much as needed/wanted. The code is already adapted to have as many questions per category as the programmer wants.

<!-- trunk-ignore(markdownlint/MD046) -->
```Python
category_sheet = SHEET.worksheet(category)
nbr_of_rows = len(category_sheet.get_all_values())
question = category_sheet.row_values(random.randint(2,nbr_of_rows - 1))
```

### Leader board (top n)