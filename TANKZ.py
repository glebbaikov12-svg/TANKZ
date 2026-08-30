import pygame, random 
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
player = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), (50, 50))
enemy = pygame.transform.scale(pygame.image.load("enemy.png").convert_alpha(), (50, 50))
x, y, dir = 275, 275, 0
bullets = []
score = 0
lives = 5
enemies = [[random.randint(50, 500), random.randint(50, 500)] for _ in range(3)]
enemy_bullets = []
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([x, y, dir]) 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and lives <= 0:
            x, y, dir = 275, 275, 0
            bullets, enemy_bullets, score, lives = [], [], 0, 3
            enemies = [[random.randint(50, 500), random.randint(50, 500)] for _ in range(3)]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: y -= 3; dir = 0
    if keys[pygame.K_s]: y += 3; dir = 1
    if keys[pygame.K_a]: x -= 3; dir = 2
    if keys[pygame.K_d]: x += 3; dir = 3
    for e in enemies:
        if e[0] < x: e[0] += 1
        if e[0] > x: e[0] -= 1
        if e[1] < y: e[1] += 1
        if e[1] > y: e[1] -= 1
        if random.randint(1, 100) < 2:
            enemy_bullets.append([e[0], e[1], 0 if e[1] < y else 1 if e[1] > y else 2 if e[0] < x else 3])
    for b in bullets[:]:
        if b[2] == 0: b[1] -= 6
        if b[2] == 1: b[1] += 6
        if b[2] == 2: b[0] -= 6
        if b[2] == 3: b[0] += 6
        if not (0 < b[0] < 600 and 0 < b[1] < 600):
            bullets.remove(b); continue   
        for e in enemies[:]:
            if abs(b[0]-e[0]) < 25 and abs(b[1]-e[1]) < 25:
                bullets.remove(b)
                enemies.remove(e)
                score += 10
                enemies.append([random.randint(50, 500), random.randint(50, 500)])
                break
    for b in enemy_bullets[:]:
        if b[2] == 0: b[1] -= 4
        if b[2] == 1: b[1] += 4
        if b[2] == 2: b[0] -= 4
        if b[2] == 3: b[0] += 4
        if not (0 < b[0] < 600 and 0 < b[1] < 600):
            enemy_bullets.remove(b); continue  
        if abs(b[0]-x) < 25 and abs(b[1]-y) < 25:
            enemy_bullets.remove(b)
            lives -= 1
    screen.fill((30, 30, 30))
    screen.blit(player, (x, y))
    for e in enemies: 
        screen.blit(enemy, (e[0], e[1])) 
    for b in bullets: 
        pygame.draw.circle(screen, (255, 255, 0), (int(b[0]), int(b[1])), 4)
    for b in enemy_bullets: 
        pygame.draw.circle(screen, (255, 0, 0), (int(b[0]), int(b[1])), 4)
    font = pygame.font.Font(None, 24)
    text = "Score: " + str(score) + "  Lives: " + str(lives)
    screen.blit(font.render(text, True, (255,255,255)), (10, 10))
    if lives <= 0:
        game_over_text = "GAME OVER - Press R"
        screen.blit(font.render(game_over_text, True, (255,0,0)), (200, 300))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
