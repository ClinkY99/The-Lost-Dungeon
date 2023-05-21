import pygame, sys, json

import Functions
import mainmenu
from Interactables import Button
from mainmenu import main_menu



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# main menu function controls, the other functions
def Death_screen(display, displaysize, enlargmentvalue, player):

    file = open('./Saves/Save.Dungeon')

    jsonFile = json.load(file)
    file.close()

    file = open('./Saves/Save.Dungeon', 'w')
    del jsonFile['Saves'][player.name]
    jsonFile["MostRecentSave"] = "None"
    json.dump(jsonFile, file, indent=4)
    file.close()

    file = open("./Saves/Leaderboard.Dungeon")
    jsonData = json.load(file)
    file.close()

    file = open('./Saves/Leaderboard.Dungeon', 'w')

    jsonData["Leaderboard"].append({
        'Name': player.name,
        'Score': player.XP,
        'Level': player.levelnum
    })
    json.dump(jsonData, file, indent=4)

    file.close()

    pygame.mouse.set_visible(True)

    paused = True
    # a different background for the darker gray areas of the screen
    background = pygame.Surface(displaysize)
    light_gray = ((84, 86, 86))
    background.fill(light_gray)

    # a different background for the darker gray areas of the screen
    background1 = pygame.Surface((500*enlargmentvalue[0], 430*enlargmentvalue[1]))
    Dark_gray = ((105, 105, 105))
    background1.fill(Dark_gray)
    background.set_alpha(75)

    # a different background for the darker gray areas of the screen
    Scoreboard = pygame.Surface((500*enlargmentvalue[0], 430*enlargmentvalue[1]))
    Scoreboard.fill(Dark_gray)
    Scoreboard.set_alpha(75)

    Scoreboard.blit(pygame.transform.scale(pygame.image.load('./Art/Menu/ScoreBoard.png').convert_alpha(), Scoreboard.get_size()), (0,0))

    ScoreboardTile = pygame.Surface((500*enlargmentvalue[0], int(43*enlargmentvalue[1])))
    ScoreboardTile.fill((0,0,0))
    ScoreboardTile.set_colorkey((0,0,0))

    while paused:
        display.blit(background, (0,0))
        display.blit(background1, (675*enlargmentvalue[0],150*enlargmentvalue[1]))

        file = open('./Saves/Leaderboard.Dungeon')

        jsonfile = json.load(file)

        leaderboard = sorted(jsonfile["Leaderboard"], key= lambda list : list['Score'], reverse=True)

        for index, data in enumerate(leaderboard):
            scoreboardinfo = ScoreboardTile.copy()

            rank = get_font(int(10*enlargmentvalue[0])).render(f'{index+1}', True, (255,255,255))
            scoreboardinfo.blit(rank, (0,0))

            name = get_font(int(10*enlargmentvalue[0])).render(f'{data["Name"]}',True, (255,255,255))
            scoreboardinfo.blit(name, (75*enlargmentvalue[0],0))

            score = get_font(int(10*enlargmentvalue[0])).render(f'{data["Score"]}',True, (255,255,255))
            scoreboardinfo.blit(score, (260*enlargmentvalue[0],0))

            levelnum = get_font(int(10*enlargmentvalue[0])).render(f'{data["Level"]}', True, (255, 255, 255))
            scoreboardinfo.blit(levelnum, (400 * enlargmentvalue[0], 0))

            Scoreboard.blit(scoreboardinfo, (0, Scoreboard.get_size()[1]/12*(index+1)))

        display.blit(Scoreboard, (75*enlargmentvalue[0],150*enlargmentvalue[1]))

        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(int(50*enlargmentvalue[0])).render("You Died", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640*enlargmentvalue[0], 100*enlargmentvalue[1]))
        display.blit(MENUtext, MENUrect)

# displaying the buttons on the main menu
        creditsbutton = Button(image=None, pos=(850*enlargmentvalue[0], 650*enlargmentvalue[1]),
                            text_input="Continue to credits", font=get_font(int(35*enlargmentvalue[0])), base_color="#d7fcd4", hovering_color="White")


        # display Statistics
        statstext = get_font(int(25*enlargmentvalue[0])).render("Statistics:", True, "#2debae")
        statsrect = statstext.get_rect(center=(850*enlargmentvalue[0], 175*enlargmentvalue[1]))
        display.blit(statstext, statsrect)
# putting the button on the screen and making it change color if hovered over
        for button in [creditsbutton]:
            button.changeColor(menumouseposition)
            button.update(display)

#Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if creditsbutton.checkForInput(menumouseposition):
                    Credits(display, displaysize)
                    main_menu(display, display.get_size())


        pygame.display.update()

def Credits(display, displaysize):
    Functions.FTB(display, 250)

    creditsscreen = pygame.transform.scale(pygame.image.load('./Art/Credits.png').convert_alpha(), displaysize)

    creditsscreen.set_alpha(0)

    for i in range(1, 1000):
        display.fill((0,0,0))
        display.blit(creditsscreen, (0,0))
        creditsscreen.set_alpha(i)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                mainmenu.main_menu(display, displaysize)

        pygame.display.update()
    mainmenu.main_menu(display, displaysize)

