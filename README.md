# Tiddler

Tiddler is a 2D space game built with Pygame. Navigate your ship through a maze, collect fuel, and avoid obstacles.

## Features

- Ship navigation with thrust and rotation
- Maze generation
- Collision detection
- Fuel management
- Bullet firing mechanism

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tiddler.git
   cd tiddler
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the game using:

```
python main.py
```

## Controls

- Left Arrow: Rotate left
- Right Arrow: Rotate right
- Up Arrow: Thrust
- X: Fire bullet

## Project Structure

- `main.py`: The main game loop and initialization
- `ship.py`: Defines the Ship class and its behavior
- `maze.py`: Implements the Maze and Block classes
- `bullet.py`: Defines the Bullet class
- `colours.py`: Contains color definitions
- `game_state.py`: Manages the game state (currently empty)
- `hex_maze.py`: An alternative maze implementation (not currently used)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
