from random import randint
import sys
import pygame
from pygame.event import Event
import Objects
import Settings


class Scene:
    def __init__(self):
        pass

    def update(self, manager):
        pass

    def join_in(self, manager):
        pass

    def jump_out(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass

    def input(self, event: pygame.event.Event):
        pass


class SceneManager:
    def __init__(
        self,
        first_scene: Scene,
        SceneLists: dict,
        screen: pygame.Surface,
        setting: Settings.Settings,
    ):
        self.current_scene = first_scene
        self.scenelists = SceneLists
        first_scene.join_in(self)
        self.screen = screen
        self.setting = setting

    def jump_to(self, new_scene: Scene):
        self.current_scene.jump_out()
        new_scene.join_in(self)
        self.current_scene = new_scene

    def update(self):
        self.current_scene.update(self)
        self.current_scene.draw(self.screen)

    def input(self, list: list):
        for i in list:
            if i.type == pygame.QUIT:
                sys.exit(0)
            else:
                self.current_scene.input(i)


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.sp1 = pygame.image.load("image/spaceship1.png")
        self.sp2 = pygame.image.load("image/spaceship2.png")
        self.bl = pygame.image.load("image/bullet.png")
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 32)
        self.p = None
        self.score = 0
        self.e_list = []
        self.basic = 10.0
        self.back_to_menu = False

    def join_in(self, manager: SceneManager):
        self.p = Objects.Player(
            640,
            600,
            self.sp1,
            manager.setting.frame_per_bullet,
            manager.setting.player_health,
        )
        self.score = 0
        self.e_list = []
        self.basic = 10.0
        self.back_to_menu = False
        pygame.mouse.set_visible(False)

    def update(self, manager: SceneManager):
        for i in range(0, int(self.basic) - len(self.e_list)):
            self.e_list.insert(
                0,
                Objects.Enemy(
                    randint(20, 1160),
                    -50,
                    self.sp2,
                    manager.setting.enemy_health,
                ),
            )
        self.p.move()
        self.p.fire(self.bl)
        for i in range(0, len(self.p.bullet_set)):
            if not i < len(self.p.bullet_set):
                break
            self.p.bullet_set[i].move()
            if self.p.bullet_set[i].rect.bottom < 0:
                self.p.bullet_set.pop(i)
                i -= 1
                continue
            for j in self.e_list:
                if self.p.bullet_set[i].crash(j):
                    j.health -= 1
                    self.p.bullet_set.pop(i)
                    i -= 1
                    break

        for i in range(0, len(self.e_list)):
            self.e_list[i].move()
            if self.p.crash(self.e_list[i]):
                self.p.health -= 1
                self.e_list[i].reset(randint(20, 1160), -50)
            if self.e_list[i].rect.bottom > 770 or self.e_list[i].health <= 0:
                if self.e_list[i].health <= 0:
                    self.basic += manager.setting.difficulty_speed
                    self.score += 100
                self.e_list[i].reset(randint(20, 1160), -50)
        if self.p.health <= 0:
            self.draw(manager.screen)
            manager.jump_to(manager.scenelists["EndScene"])
        if self.back_to_menu:
            manager.jump_to(manager.scenelists["StartScene"])

    def draw(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        self.p.draw(screen)
        for i in self.e_list:
            i.draw(screen)
        for i in self.p.bullet_set:
            i.draw(screen)
        text = self.font.render(
            "分数："
            + f"{self.score}"
            + "\n血量："
            + f"{self.p.health if self.p.health > 0 else 0}",
            True,
            (0, 0, 0),
        )
        text2 = self.font.render("Esc返回主菜单", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.x = 0
        textRect.y = 0
        textRect2 = text2.get_rect()
        textRect2.y = 50
        screen.blit(text, textRect)
        screen.blit(text2, textRect2)

    def jump_out(self):
        self.e_list = []
        self.basic = 10.0
        self.back_to_menu = False
        pygame.mouse.set_visible(True)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.p.move_statue = "l"
            elif event.key == pygame.K_RIGHT:
                self.p.move_statue = "r"
            elif event.key == pygame.K_ESCAPE:
                self.back_to_menu = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.p.move_statue == "l":
                self.p.move_statue = ""
            elif event.key == pygame.K_RIGHT and self.p.move_statue == "r":
                self.p.move_statue = ""
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.p.on_fire = not self.p.on_fire


class EndScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 200)
        self.text = self.font.render("寄", True, (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 640
        self.textRect.centery = 360
        self.back_to_menu = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.text, self.textRect)

    def join_in(self, manager):
        self.back_to_menu = False
        return super().join_in(manager)

    def jump_out(self):
        self.back_to_menu = False
        return super().jump_out()

    def update(self, manager: SceneManager):
        if self.back_to_menu:
            manager.jump_to(manager.scenelists["StartScene"])

    def input(self, event: Event):
        if event.type == pygame.KEYDOWN:
            self.back_to_menu = event.key == pygame.K_ESCAPE
        return super().input(event)


class StartScene(Scene):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("image/spaceship1.png"), (100, 200)
        )
        self.rect = self.image.get_rect()
        self.rect.bottom = 250
        self.rect.centerx = 640
        self.start_button = Objects.Button("开始游戏", 640, 300, 600, 70)
        self.setting_button = Objects.Button("设置", 640, 420, 600, 70)
        self.jump_statue = None

    def draw(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        screen.blit(self.image, self.rect)
        self.start_button.draw(screen)
        self.setting_button.draw(screen)

    def input(self, event: pygame.event.Event):
        if self.start_button.deal_mouse(event):
            self.jump_statue = "start"
        elif self.setting_button.deal_mouse(event):
            self.jump_statue = "settings"

    def update(self, manager: SceneManager):
        if self.jump_statue == "start":
            manager.jump_to(manager.scenelists["GameScene"])
        elif self.jump_statue == "settings":
            manager.jump_to(manager.scenelists["SettingScene"])

    def jump_out(self):
        self.jump_statue = None
        self.start_button.reset()
        self.setting_button.reset()


class SettingScene(Scene):
    class _SettingUnit:
        def __init__(self, x, y, value, vbreak, min, max, message):
            self.value = value
            self.vbreak = vbreak
            self.min = min
            self.max = max
            self.x = x
            self.sub = (x + 200 + 20, y + 25)
            self.add = (self.sub[0] + 150 + 20, y + 25)
            self.add_button = Objects.Button("+", self.add[0], self.add[1], 40, 40)
            self.sub_button = Objects.Button("-", self.sub[0], self.sub[1], 40, 40)
            self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 30)
            self.change_statue = None
            self.text1 = self.font.render(message, True, (0, 0, 0))
            self.text2 = self.font.render(str(self.value), True, (0, 0, 0))
            self.rect1 = self.text1.get_rect()
            self.rect2 = self.text2.get_rect()

        def draw(self, screen: pygame.Surface):
            screen.blit(self.text1, self.rect1)
            screen.blit(self.text2, self.rect2)
            self.add_button.draw(screen)
            self.sub_button.draw(screen)

        def input(self, event: pygame.event.Event):
            if self.add_button.deal_mouse(event):
                self.change_statue = "+"
            elif self.sub_button.deal_mouse(event):
                self.change_statue = "-"
            else:
                self.change_statue = None

        def update(self):
            self.text2 = self.font.render(str(self.value), True, (0, 0, 0))
            self.rect2 = self.text2.get_rect()
            self.rect1.bottomleft = (self.x, self.rect1.bottom)
            self.rect1.centery = self.sub[1]
            self.rect2.centerx = (self.sub[0] + self.add[0]) // 2
            self.rect2.centery = self.sub[1]
            if not self.change_statue == None:
                new_value = eval(
                    str(self.value) + self.change_statue + str(self.vbreak)
                )
                self.change_statue = None
                if new_value < self.min:
                    self.value = self.min
                elif new_value > self.max:
                    self.value = self.max
                else:
                    self.value = new_value
            return self.value

        def reset(self):
            self.change_statue = None

    def __init__(self):
        super().__init__()
        self.back_button = Objects.Button("返回", 100, 50, 150, 50)
        self.health_module = None
        self.enemy_health_module = None
        self.bullet_break = None
        self.back_statue = False

    def draw(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        self.back_button.draw(screen)
        self.health_module.draw(screen)
        self.enemy_health_module.draw(screen)
        self.bullet_break.draw(screen)

    def input(self, event: pygame.event.Event):
        self.health_module.input(event)
        self.enemy_health_module.input(event)
        self.bullet_break.input(event)
        if self.back_button.deal_mouse(event):
            self.back_statue = True

    def update(self, manager: SceneManager):
        if self.back_statue:
            manager.jump_to(manager.scenelists["StartScene"])
        manager.setting.player_health = self.health_module.update()
        manager.setting.enemy_health = self.enemy_health_module.update()
        manager.setting.frame_per_bullet = self.bullet_break.update()

    def jump_out(self):
        self.back_statue = False
        self.back_button.reset()
        self.health_module.reset()
        self.enemy_health_module.reset()
        self.bullet_break.reset()

    def join_in(self, manager: SceneManager):
        self.health_module = self._SettingUnit(
            10, 100, manager.setting.player_health, 1, 1, 999, "玩家血量"
        )
        self.enemy_health_module = self._SettingUnit(
            10, 160, manager.setting.enemy_health, 1, 1, 10, "敌人血量"
        )
        self.bullet_break = self._SettingUnit(
            650, 100, manager.setting.frame_per_bullet, 1, 2, 20, "子弹间隔(帧)"
        )
