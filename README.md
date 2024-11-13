# Rogue

## Description

A Roguelike game in which the player explores randomly generated dungeons, fights monsters, collects items, equips gear, and uses magic with the goal of retrieving the Legendary Master Sword hidden in the dungeon.

## Main features

- **Random level generation** : Each floor of the dungeon is randomly generated with increasingly stronger enemies.</br>
- **Turn-based combat** : A turn-based combat system where actions are determined by the speed of the hero and the monsters.</br>
- **Hero versatility** : The player can choose to play in different ways, whether by fleeing, fighting, attacking close or ranged, using magic, and more.</br>
- **Permadeath** : Each death is permanent, encouraging the player to be strategic.

## Technologies used

- **Language** : `Python`</br>
- **Librairies** : `abc`, `copy`, `math`, `random`, `typing`, `sys`, `os`, `msvcrt`

## Installation

- **Clone the repository** :
    ```bash
    git clone https://github.com/HugoHeilmann/Rogue.git
    ```

- **Install a sufficient version of Python (3.6)** :
    - **Debian/Ubuntu** : 
    ```bash
    sudo apt-get install python3.6
    ```
    - **Windows** :
    >https://www.python.org/downloads/
    - **macOS** :
    ```bash
    brew install python@3.6*
    ```

- **Run the game** :
    ```bash
    python rogue.py
    # ou
    python3 rogue.py
    ```

## Usage

- Lateral movements : <span style="color:#FFD700">z</span>(↑), <span style="color:#FFD700">q</span>(←), <span style="color:#FFD700">s</span>(↓), <span style="color:#FFD700">d</span>(→)</br>
- Diagonal movements : <span style="color:#FFD700">a</span>(↖), <span style="color:#FFD700">e</span>(↗), <span style="color:#FFD700">w</span>(↙), <span style="color:#FFD700">c</span>(↘)</br>
- Use an object : <span style="color:#FFD700">u</span></br>
- Toss an object : <span style="color:#FFD700">t</span></br>
- Throw an object : <span style="color:#FFD700">j</span></br>
- Cast a spell : <span style="color:#FFD700">m</span></br>
- View the hero's description : <span style="color:#FFD700">i</span></br>
- View the description of owned items : <span style="color:#FFD700">o</span></br>
- View the description of spells : <span style="color:#FFD700">p</span></br>
- View the glossary of available actions : <span style="color:#FFD700">l</span></br>
- Do nothing : <span style="color:#FFD700">x</span></br>
- Kill yourself : <span style="color:#FFD700">k</span>

## Author

**Hugo Heilmann, IT student, Polytech' Nice-Sophia**