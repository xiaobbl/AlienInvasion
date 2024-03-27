import pygame
import Scenes
import Settings

pygame.init()
pygame.display.set_caption("AlienInvasion")
setting = Settings.Settings()
scenelist = dict()
screen = pygame.display.set_mode((1280, 720))
scenelist["GameScene"] = Scenes.GameScene()
scenelist["EndScene"] = Scenes.EndScene()
scenelist["StartScene"] = Scenes.StartScene()
scenelist["SettingScene"] = Scenes.SettingScene()
scenemanager = Scenes.SceneManager(scenelist["StartScene"], scenelist, screen, setting)
clock = pygame.time.Clock()
while True:
    scenemanager.input(pygame.event.get())
    scenemanager.update()
    pygame.display.update()
    clock.tick(60)
