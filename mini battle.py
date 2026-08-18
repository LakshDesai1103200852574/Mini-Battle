# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 02:03:14 2026

@author: prathna
"""

import tkinter as tk
import random

# =========================================================
# SETTINGS
# =========================================================

WIDTH = 900
HEIGHT = 600

player_hp = 120
enemy_hp = 100
energy = 100

shield_active = False
game_over = False
busy = False

player_x = 180
enemy_x = 720


# =========================================================
# WINDOW
# =========================================================

window = tk.Tk()
window.title("🚀 Space Battle")
window.geometry("900x600")
window.resizable(False, False)

canvas = tk.Canvas(
    window,
    width=WIDTH,
    height=HEIGHT,
    bg="#030712",
    highlightthickness=0
)

canvas.pack()


# =========================================================
# STARS
# =========================================================

stars = []

for i in range(100):

    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)

    star = canvas.create_oval(
        x, y,
        x + 2, y + 2,
        fill="white",
        outline=""
    )

    stars.append(star)


def move_stars():

    for star in stars:

        canvas.move(star, -1.5, 0)

        box = canvas.coords(star)

        if box[2] < 0:

            y = random.randint(0, HEIGHT)

            canvas.coords(
                star,
                WIDTH,
                y,
                WIDTH + 2,
                y + 2
            )

    window.after(40, move_stars)


# =========================================================
# TITLE
# =========================================================

canvas.create_text(
    450,
    30,
    text="SPACE BATTLE",
    fill="#8be9fd",
    font=("Arial", 25, "bold")
)

canvas.create_text(
    450,
    58,
    text="ENERGY DUEL",
    fill="#64748b",
    font=("Arial", 10)
)


# =========================================================
# PLAYER SHIP
# =========================================================

player_ship = canvas.create_polygon(
    player_x - 45, 270,
    player_x + 20, 240,
    player_x + 45, 270,
    player_x + 20, 300,
    fill="#00c8ff",
    outline="white",
    width=2
)

player_engine = canvas.create_oval(
    player_x - 55,
    260,
    player_x - 42,
    280,
    fill="#00ffff",
    outline=""
)


# =========================================================
# ENEMY SHIP
# =========================================================

enemy_ship = canvas.create_polygon(
    enemy_x + 45, 270,
    enemy_x - 20, 240,
    enemy_x - 45, 270,
    enemy_x - 20, 300,
    fill="#ff3344",
    outline="white",
    width=2
)

enemy_engine = canvas.create_oval(
    enemy_x + 42,
    260,
    enemy_x + 55,
    280,
    fill="#ff8800",
    outline=""
)


# =========================================================
# LABELS
# =========================================================

canvas.create_text(
    180,
    330,
    text="YOUR SHIP",
    fill="#00c8ff",
    font=("Arial", 12, "bold")
)

canvas.create_text(
    720,
    330,
    text="HOSTILE",
    fill="#ff4455",
    font=("Arial", 12, "bold")
)


# =========================================================
# HP BARS
# =========================================================

canvas.create_text(
    180,
    365,
    text="HULL",
    fill="white",
    font=("Arial", 10)
)

canvas.create_rectangle(
    70, 380,
    290, 402,
    outline="#334155"
)

player_bar = canvas.create_rectangle(
    70, 380,
    290, 402,
    fill="#00d4ff",
    outline=""
)


canvas.create_text(
    720,
    365,
    text="HULL",
    fill="white",
    font=("Arial", 10)
)

canvas.create_rectangle(
    610, 380,
    830, 402,
    outline="#334155"
)

enemy_bar = canvas.create_rectangle(
    610, 380,
    830, 402,
    fill="#ff3344",
    outline=""
)


# =========================================================
# ENERGY
# =========================================================

canvas.create_text(
    450,
    425,
    text="ENERGY",
    fill="#8be9fd",
    font=("Arial", 10)
)

canvas.create_rectangle(
    300,
    440,
    600,
    455,
    outline="#334155"
)

energy_bar = canvas.create_rectangle(
    300,
    440,
    600,
    455,
    fill="#00aaff",
    outline=""
)


# =========================================================
# STATUS
# =========================================================

status = canvas.create_text(
    450,
    100,
    text="SYSTEM READY",
    fill="white",
    font=("Arial", 17, "bold")
)


canvas.create_text(
    450,
    510,
    text="SPACE = FIRE     ↑ = SHIELD     ↓ = REPAIR",
    fill="#64748b",
    font=("Arial", 11)
)

canvas.create_text(
    450,
    540,
    text="R = RESTART",
    fill="#64748b",
    font=("Arial", 10)
)


# =========================================================
# UPDATE UI
# =========================================================

def update_ui():

    # Player HP
    player_width = max(0, player_hp * 220 / 120)

    canvas.coords(
        player_bar,
        70,
        380,
        70 + player_width,
        402
    )

    # Enemy HP
    enemy_width = max(0, enemy_hp * 220 / 100)

    canvas.coords(
        enemy_bar,
        610,
        380,
        610 + enemy_width,
        402
    )

    # Energy
    energy_width = max(0, energy * 3)

    canvas.coords(
        energy_bar,
        300,
        440,
        300 + energy_width,
        455
    )


# =========================================================
# MOVE PLAYER
# =========================================================

def move_player(amount):

    global player_x

    player_x += amount

    canvas.move(
        player_ship,
        amount,
        0
    )

    canvas.move(
        player_engine,
        amount,
        0
    )


# =========================================================
# MOVE ENEMY
# =========================================================

def move_enemy(amount):

    global enemy_x

    enemy_x += amount

    canvas.move(
        enemy_ship,
        amount,
        0
    )

    canvas.move(
        enemy_engine,
        amount,
        0
    )


# =========================================================
# PLAYER RECOIL
# =========================================================

def player_recoil():

    move_player(-12)

    window.after(
        80,
        lambda: move_player(12)
    )


# =========================================================
# ENEMY RECOIL
# =========================================================

def enemy_recoil():

    move_enemy(15)

    window.after(
        100,
        lambda: move_enemy(-15)
    )


# =========================================================
# FIRE
# =========================================================

def fire():

    global energy
    global busy

    if game_over or busy:
        return

    if energy < 5:

        canvas.itemconfig(
            status,
            text="⚠ LOW ENERGY!"
        )

        return

    energy -= 5

    update_ui()

    busy = True

    player_recoil()

    canvas.itemconfig(
        status,
        text="⚡ FIRING ENERGY PULSE..."
    )

    pulse = canvas.create_oval(
        player_x + 25,
        258,
        player_x + 45,
        282,
        fill="#00ffff",
        outline="white",
        width=2
    )

    target = enemy_x - 45

    def animate():

        coords = canvas.coords(pulse)

        if coords[0] >= target:

            canvas.delete(pulse)

            hit_enemy()

            return

        canvas.move(
            pulse,
            18,
            0
        )

        window.after(
            20,
            animate
        )

    animate()


# =========================================================
# HIT ENEMY
# =========================================================

def hit_enemy():

    global enemy_hp

    damage = random.randint(12, 20)

    enemy_hp -= damage

    if enemy_hp < 0:
        enemy_hp = 0

    enemy_recoil()

    # Explosion flash
    flash = canvas.create_oval(
        enemy_x - 55,
        215,
        enemy_x + 55,
        325,
        fill="#ffffff",
        outline=""
    )

    window.after(
        70,
        lambda: canvas.delete(flash)
    )

    # Particles
    for i in range(8):

        x = enemy_x + random.randint(-30, 30)
        y = random.randint(240, 300)

        particle = canvas.create_oval(
            x,
            y,
            x + 6,
            y + 6,
            fill=random.choice(
                ["#ffff00", "#ff6600", "#ffffff"]
            ),
            outline=""
        )

        window.after(
            250,
            lambda p=particle: canvas.delete(p)
        )

    update_ui()

    canvas.itemconfig(
        status,
        text=f"⚡ HIT!  -{damage} ENEMY HP"
    )

    if enemy_hp <= 0:

        victory()

        return

    window.after(
        500,
        enemy_attack
    )


# =========================================================
# ENEMY ATTACK
# =========================================================

def enemy_attack():

    global busy

    if game_over:
        return

    canvas.itemconfig(
        status,
        text="👾 HOSTILE FIRING..."
    )

    pulse = canvas.create_oval(
        enemy_x - 45,
        258,
        enemy_x - 25,
        282,
        fill="#ff3333",
        outline="white"
    )

    target = player_x + 40

    def animate():

        coords = canvas.coords(pulse)

        if coords[0] <= target:

            canvas.delete(pulse)

            hit_player()

            return

        canvas.move(
            pulse,
            -18,
            0
        )

        window.after(
            20,
            animate
        )

    animate()


# =========================================================
# HIT PLAYER
# =========================================================

def hit_player():

    global player_hp
    global shield_active
    global busy

    damage = random.randint(5, 10)

    # Shield works now!
    if shield_active:

        blocked = int(damage * 0.7)

        damage -= blocked

        shield_active = False

        canvas.itemconfig(
            status,
            text=f"🛡 SHIELD BLOCKED {blocked} DAMAGE!"
        )

    player_hp -= damage

    if player_hp < 0:
        player_hp = 0

    player_recoil()

    # Impact flash
    flash = canvas.create_oval(
        player_x - 55,
        215,
        player_x + 55,
        325,
        fill="#ffaa00",
        outline=""
    )

    window.after(
        70,
        lambda: canvas.delete(flash)
    )

    update_ui()

    if player_hp <= 0:

        defeat()

        return

    busy = False

    # Regenerate energy
    recover_energy()


# =========================================================
# SHIELD
# =========================================================

def activate_shield():

    global energy
    global shield_active
    global busy

    if game_over or busy:
        return

    if energy < 10:

        canvas.itemconfig(
            status,
            text="⚠ NOT ENOUGH ENERGY!"
        )

        return

    energy -= 10

    shield_active = True
    busy = True

    update_ui()

    canvas.itemconfig(
        status,
        text="🛡 SHIELD ONLINE!"
    )

    ring = canvas.create_oval(
        player_x - 65,
        205,
        player_x + 65,
        335,
        outline="#00ffff",
        width=5
    )

    # Pulsing shield
    def pulse_shield(size=65):

        if not shield_active:
            return

        canvas.coords(
            ring,
            player_x - size,
            270 - size,
            player_x + size,
            270 + size
        )

        if size == 65:
            new_size = 75
        else:
            new_size = 65

        window.after(
            100,
            lambda: pulse_shield(new_size)
        )

    pulse_shield()

    window.after(
        700,
        lambda: enemy_attack_with_shield(ring)
    )


def enemy_attack_with_shield(ring):

    global shield_active

    canvas.delete(ring)

    enemy_attack()


# =========================================================
# REPAIR
# =========================================================

def repair():

    global player_hp
    global energy
    global busy

    if game_over or busy:
        return

    if energy < 15:

        canvas.itemconfig(
            status,
            text="⚠ NOT ENOUGH ENERGY!"
        )

        return

    if player_hp >= 120:

        canvas.itemconfig(
            status,
            text="❤️ HULL ALREADY FULL"
        )

        return

    energy -= 15

    repair_amount = random.randint(10, 18)

    player_hp = min(
        120,
        player_hp + repair_amount
    )

    busy = True

    update_ui()

    canvas.itemconfig(
        status,
        text=f"🔧 REPAIRING +{repair_amount} HP"
    )

    # Green repair particles
    for i in range(15):

        x = random.randint(
            player_x - 40,
            player_x + 40
        )

        y = random.randint(
            230,
            310
        )

        particle = canvas.create_oval(
            x,
            y,
            x + 5,
            y + 5,
            fill="#00ff88",
            outline=""
        )

        window.after(
            random.randint(200, 600),
            lambda p=particle: canvas.delete(p)
        )

    window.after(
        700,
        enemy_attack
    )


# =========================================================
# ENERGY RECOVERY
# =========================================================

def recover_energy():

    global energy

    energy += 8

    if energy > 100:
        energy = 100

    update_ui()


# =========================================================
# VICTORY
# =========================================================

def victory():

    global game_over
    global busy

    game_over = True
    busy = False

    canvas.itemconfig(
        status,
        text="🏆 HOSTILE SHIP DISABLED!"
    )

    # Explosion
    for i in range(30):

        x = enemy_x + random.randint(-60, 60)
        y = random.randint(210, 330)

        particle = canvas.create_oval(
            x,
            y,
            x + 8,
            y + 8,
            fill=random.choice(
                ["#ff0000", "#ff6600", "#ffff00", "#ffffff"]
            ),
            outline=""
        )

        window.after(
            random.randint(100, 900),
            lambda p=particle: canvas.delete(p)
        )

    canvas.create_text(
        450,
        250,
        text="🏆 VICTORY!",
        fill="#00ffff",
        font=("Arial", 48, "bold"),
        tag="gameover"
    )

    canvas.create_text(
        450,
        315,
        text="You won the battle!",
        fill="white",
        font=("Arial", 17),
        tag="gameover"
    )

    canvas.create_text(
        450,
        350,
        text="Press R to play again",
        fill="#94a3b8",
        font=("Arial", 13),
        tag="gameover"
    )


# =========================================================
# DEFEAT
# =========================================================

def defeat():

    global game_over
    global busy

    game_over = True
    busy = False

    canvas.itemconfig(
        status,
        text="💥 SHIP DISABLED"
    )

    canvas.create_text(
        450,
        250,
        text="DEFEATED",
        fill="#ff3344",
        font=("Arial", 45, "bold"),
        tag="gameover"
    )

    canvas.create_text(
        450,
        315,
        text="Press R to try again",
        fill="white",
        font=("Arial", 15),
        tag="gameover"
    )


# =========================================================
# RESTART
# =========================================================

def restart():

    global player_hp
    global enemy_hp
    global energy
    global shield_active
    global game_over
    global busy
    global player_x
    global enemy_x

    canvas.delete("gameover")

    player_hp = 120
    enemy_hp = 100
    energy = 100

    shield_active = False
    game_over = False
    busy = False

    # Reset positions
    move_player(180 - player_x)
    move_enemy(720 - enemy_x)

    player_x = 180
    enemy_x = 720

    update_ui()

    canvas.itemconfig(
        status,
        text="SYSTEM READY"
    )


# =========================================================
# KEYBOARD
# =========================================================

window.bind(
    "<space>",
    lambda event: fire()
)

window.bind(
    "<Up>",
    lambda event: activate_shield()
)

window.bind(
    "<Down>",
    lambda event: repair()
)

window.bind(
    "r",
    lambda event: restart()
)


# =========================================================
# START
# =========================================================

update_ui()
move_stars()

window.mainloop() 