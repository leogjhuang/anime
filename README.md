# GitAnimeList

create a github repo anime with main.py.

main.py edits README.md and maintains a list of checkboxes for the anime that you input into the program.

instructions is in instructions.txt.

main.py outputs "Select an option below:" at start where the options are
[0] Exit program
[1] Add anime to README.md
[2] Save README.md
[3] Clear README.md

0 can exit the program at any point with a message "all unsaved progress will be lost. are you sure you want to exit?  (y/n)" whenever selected.

if 1 is selected in home screen:
[0] Go back to home screen
[1] Add anime titles on separate lines
[2] Turn "anime confirmation" on/off (default off)

1 allows you to enter the titles of anime that the program will use to compare with the entries on myanimelist.com. if a title has no matching entry, an error will pop up, notifying the user that no match was found and providing the options to skip or rename. once finished, there will be a warning that the added anime have not been saved yet along with the option to go back to home screen or go back to add anime screen.

2 will toggle anime confirmation, which will verify each title with up to 5 of its most relevant entries on myanimelist.com if it's toggled on.

if 2 is selected in home screen:
[0] Go back to home screen
[1] Save all added anime to README.md
[2] Turn "myanimelist link" on/off (default on)
[3] Turn "myanimelist rating" on/off (default off)
[4] Turn "mal rating sort" on/off (default on)

1 will add all anime added in this session to the current list in README.md. the program will overwrite the file, first adding the text from instructions.txt and then saving the anime list based on the given conditions. once finished, there will be the option to go back to home screen or go back to save anime screen.

2 will toggle myanimelist link, which will automatically add a hyperlink to the title of the anime when saving if it's toggled on.

3 will toggle myanimelist rating, which will automatically add the current rating to the title of the anime separated by a space when saving if it's toggled on.

4 will toggle mal rating sort, which will sort the anime by current rating starting with the highest first if it's toggled on. if it's toggled off, the anime list will be saved alphabetically.

if 3 is selected in home screen:
a message "all text in README.md will be lost. are you sure you want to clear?  (y/n)" will appear. the program will clear README.md and rewrite the instructions if y is selected. either way, you will be redirected back to the home screen.

extras:
add delete anime option
add different anime headers (watched, plan to watch)
add toggle to choose between english or japanese names or both
