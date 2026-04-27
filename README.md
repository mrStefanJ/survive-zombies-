# Zombie Survivors

Zombie Survivors is a fast-paced arcade survival game written in Python using Pygame. The player must avoid and destroy zombies, use bombs strategically, and survive as long as possible to achieve the highest score.

Features:
- 🧟‍♂️ Dynamic Zombie System
Procedural enemy spawning with difficulty scaling over time.
- 💣 Bomb System
Limited number of bombs with cooldown mechanics and visual indicators.
- 💥 Explosion Effects & Particles
Visual effects for explosions and particles for a better game feel
- 🎯 Score & Survival Time Tracking
Tracking survival time in MM:SS format and highscore system.
- 🩸 Death Slow Effect & Screen Overlay
Dramatic slowdown effect and red overlay upon death.
- 🖥️ Custom HUD (Heads-Up Display)
Real-time display of time and results.
- 🎨 Player Customization (Shape & Color)
Choice of player appearance.
- 🔊 Audio Support
Integrisan background music i sound effects.

## Gameplay

The goal of the game is simple:
- Survive as long as you can
- Avoid zombies
- Use bombs tactically when surrounded
- Set a new highscore

As time passes, enemies spawn faster and gameplay becomes more intense

## Installation
Clone a turnip
```bash
git clone https://github.com/your-username/multiverse-runner.git
```
```bash
cd multiverse-runner
```
Instaliraj dependencies
```bash
pip install pygame
```
Start the game
```bash
python main.py
```

## Core Systems Overview
### Spawn System

Controls zombie spawn based on survival time.

### Bomb System
- Max Bombs
- Cooldown Regeneration
- Visual Indicator (HUD)
### HUD System

- In the upper left corner you will see how much time you have been playing and how many points you have collected. 
- In the lower left corner you will see how many bombs you can throw.
### Particle System

Adds visual feedback during explosions and actions.

## Tech Stack
- Python 3
- Pygame