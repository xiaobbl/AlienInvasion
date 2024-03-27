import pygame


class Object:
    def __init__(self, x, y, path):
        self.image = path
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def crash(self, obj):
        return self.rect.colliderect(obj.rect)


class Bullet(Object):
    def __init__(self, x, y, path, bullet_speed):
        super().__init__(x, y, path)
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = bullet_speed

    def move(self):
        self.rect = self.rect.move(0, -self.speed)


class Player(Object):
    def __init__(self, x, y, path, bullet_break, health):
        super().__init__(x, y, path)
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.move_statue = ""
        self.health = health
        self.bullet_break = bullet_break
        self.b_break = 0
        self.on_fire = False
        self.bullet_set = []

    def move(self):
        if self.move_statue == "l" and self.rect.centerx > 30:
            self.rect = self.rect.move(-3, 0)
        elif self.move_statue == "r" and self.rect.centerx < 1250:
            self.rect = self.rect.move(3, 0)

    def fire(self, bullet_image):
        if self.on_fire and self.b_break % self.bullet_break == 1:
            self.bullet_set.append(
                Bullet(
                    self.rect.centerx - 5,
                    self.rect.centery - 10,
                    bullet_image,
                    10,
                )
            )
        elif (not self.on_fire) and self.b_break > self.bullet_break:
            self.b_break = 0
        self.b_break += 1


class Enemy(Object):
    def __init__(self, x, y, path, max_health):
        super().__init__(x, y, path)
        self.image = pygame.transform.scale(self.image, (150, 50))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.max_health = max_health
        self.health = max_health

    def move(self):
        self.rect = self.rect.move(0, 2)

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.health = self.max_health

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if self.health < self.max_health:
            rect1 = pygame.Rect(
                self.rect.bottomleft[0],
                self.rect.bottom,
                self.rect.bottomright[0] - self.rect.bottomleft[0],
                10,
            )
            rect2 = pygame.Rect(
                self.rect.bottomleft[0],
                self.rect.bottom,
                (self.rect.bottomright[0] - self.rect.bottomleft[0])
                * self.health
                // self.max_health,
                10,
            )
            pygame.draw.rect(screen, (128, 128, 128), rect1)
            pygame.draw.rect(screen, (0, 255, 0), rect2)


class Button:
    def __init__(self, message: str, centerx, centery, width, height):
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 30)
        self.text = self.font.render(message, True, (255, 255, 255))
        self.mouse_in = False
        self.lbuttondown = False
        self.rect = pygame.Rect(
            centerx - width // 2, centery - height // 2, width, height
        )
        self.centery = centery
        self.centerx = centerx
        self.width = width
        self.height = height

    def deal_mouse(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.lbuttondown = False
            return self.mouse_in
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            self.mouse_in = (
                abs(x - self.centerx) <= self.width // 2
                and abs(y - self.centery) <= self.height // 2
            )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.lbuttondown = event.button == 1
        return False

    def draw(self, screen: pygame.Surface):
        width = 12
        color = (211, 211, 211)
        if self.mouse_in:
            if self.lbuttondown:
                color = (128, 128, 128)
            else:
                color = (169, 169, 169)
            width = 14
        pygame.draw.rect(screen, (105, 105, 105), self.rect.inflate(width, width), 0, 6)
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text, self.text.get_rect(center=(self.centerx, self.centery)))

    def reset(self):
        self.lbuttondown, self.mouse_in = False, False
