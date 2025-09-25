import pygame
import sys
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚡ Redox Quest: Battle of Ions ⚡")

# Colors
WHITE, BLACK, RED, GREEN, BLUE = (255,255,255), (0,0,0), (200,0,0), (0,200,0), (0,0,200)

# Font
font = pygame.font.SysFont("comicsans", 28)

# Load sounds
attack_sound = pygame.mixer.Sound("attack.wav")
shield_sound = pygame.mixer.Sound("shield.wav")
boss_sound = pygame.mixer.Sound("boss.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")

# Villains and questions
villains = [
    {"name": "Rust Beast 🦾", "question": "Oxidation state of Fe in Fe2O3?", "answer": "3", "hp": 3, "max_hp": 3},
    {"name": "Chlorine Phantom ☠️", "question": "Oxidation state of Cl in HClO4?", "answer": "7", "hp": 3, "max_hp": 3},
    {"name": "Permanganate Titan 💜", "question": "Oxidation state of Mn in KMnO4?", "answer": "7", "hp": 4, "max_hp": 4},
    {"name": "ElectroLord 👑", "question": "Balance: Cu²⁺ + Zn → Cu + Zn²⁺. Who is oxidized?", "answer": "Zn", "hp": 5, "max_hp": 5},
    {"name": "ElectroLord Ascended ⚡👑", "question": "Which species undergoes reduction in KMnO4 + HCl reaction?", "answer": "MnO4-", "hp": 7, "max_hp": 7}
]

# Game variables
current_villain = 0
hero_health = 10
xp = 0
user_input = ""
using_shield = False
boss_phase = False

def draw_health_bar(x, y, health, max_health, color):
    bar_width = 150
    bar_height = 20
    fill = (health / max_health) * bar_width
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))  
    pygame.draw.rect(screen, color, (x, y, fill, bar_height))  
    pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height), 2)  

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Hero stats
    health_text = font.render(f"❤️ Health: {hero_health}", True, RED)
    xp_text = font.render(f"⭐ XP: {xp}", True, GREEN)
    screen.blit(health_text, (20, 20))
    screen.blit(xp_text, (700, 20))

    # Game over
    if hero_health <= 0:
        lose_sound.play()
        msg = font.render("💀 You lost! Chemoria falls into darkness.", True, RED)
        screen.blit(msg, (200, 250))
        pygame.display.flip()
        pygame.time.delay(4000)
        break

    # Victory
    if current_villain >= len(villains):
        win_sound.play()
        msg = font.render("🎉 Victory! You saved Chemoria!", True, GREEN)
        screen.blit(msg, (200, 250))
        pygame.display.flip()
        pygame.time.delay(5000)
        break

    # Villain
    villain = villains[current_villain]
    v_text = font.render(f"⚔️ {villain['name']} (HP: {villain['hp']})", True, BLACK)
    screen.blit(v_text, (250, 100))
    q_text = font.render(f"👉 {villain['question']}", True, BLACK)
    screen.blit(q_text, (250, 150))
    input_text = font.render(f"Your Answer: {user_input}", True, BLUE)
    screen.blit(input_text, (250, 200))

    # Draw health bars
    draw_health_bar(250, 250, villain["hp"], villain["max_hp"], GREEN)

    # Display actions
    action_text = font.render("Press [1] Normal Attack | [2] Lightning Slash ⚡ | [3] Shield 🛡️", True, BLACK)
    screen.blit(action_text, (80, 500))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Normal Attack (Answer required)
                if user_input.strip() == villain["answer"]:
                    attack_sound.play()
                    villain["hp"] -= 1
                    xp += 5
                    if villain["hp"] <= 0:
                        if villain["name"] == "ElectroLord 👑" and not boss_phase:
                            boss_sound.play()
                            boss_msg = font.render("⚡ ElectroLord revives! Phase 2 begins!", True, RED)
                            screen.blit(boss_msg, (200, 300))
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            boss_phase = True
                        current_villain += 1
                else:
                    hero_health -= 1 if not using_shield else 0.5
                    using_shield = False
                user_input = ""
            elif event.key == pygame.K_2:  # Lightning Slash
                attack_sound.play()
                villain["hp"] -= 2
                hero_health -= 1  # self-damage
                xp += 8
            elif event.key == pygame.K_3:  # Shield
                shield_sound.play()
                using_shield = True
            elif event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

    # Boss counter attack (only for Phase 2)
    if villain["name"] == "ElectroLord Ascended ⚡👑" and random.randint(1, 15) == 1:
        hero_health -= 1
        counter_text = font.render("⚡ ElectroLord strikes back!", True, RED)
        screen.blit(counter_text, (300, 400))

    pygame.display.flip()

pygame.quit()
