import pygame, ctypes, os, json

import Classes,deathscreen,Endscreen,Functions,Interactables,Inventorymenu,Main,mainmenu,PauseMenu,Procedural_Generator,settings,Shop

pygame.init()
pygame.mixer.init()

user32 = ctypes.windll.user32

screen = pygame.display.set_mode((user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)))

try:
    os.mkdir('./Saves')
except:
    pass

try:
    open('./Saves/Leaderboard.Dungeon', 'x')

    with open('./Saves/Leaderboard.Dungeon', 'w') as f:
        leaderboard_blank_json = {
            "Leaderboard": []
        }

        json.dump(leaderboard_blank_json, f, indent=2)
        f.close()
except:
    pass
try:
    open('./Saves/Save.Dungeon', 'x')

    with open('./Saves/Save.Dungeon', 'w') as f:
        Save_blank_Json = {
            "MostRecentSave": "None",
            "Saves": {}
        }
        json.dump(Save_blank_Json, f, indent=2)
        f.close()
except:
    pass




mainmenu.splash(screen, screen.get_size())