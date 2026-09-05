# Rubik's Cube Solver

A command-line Rubik's Cube solver written in pure Python. You type in the colors of a scrambled cube face by face, and it works out a solution using the layer-by-layer method (white cross → first layer → second layer → OLL → PLL) and prints the moves it made along with the solved cube.

No external libraries required — just Python.

## How it works

The solver represents the cube as six faces of nine stickers each, using single-letter color codes:

| Letter | Color  |
|--------|--------|
| w      | white  |
| b      | blue   |
| o      | orange |
| g      | green  |
| r      | red    |
| y      | yellow |

It solves the cube the way a human would with the beginner's method: build the white cross, slot in the first-layer corners, place the second-layer edges, orient the last layer (OLL), then permute the last layer (PLL).

## Requirements

- Python 3.7 or later
- No third-party packages needed

## Usage

Run the script from a terminal:

```bash
python cube_solver.py
```

You'll be prompted to enter each face of your cube, one at a time. For each face, type all 9 stickers as a single string of letters, reading left to right, top to bottom, exactly as you see that face when holding the cube with **white on top** and **blue facing you**.

The prompts will guide you through all six faces in this order: UP (white), FRONT (blue), RIGHT (orange), BACK (green), LEFT (red), DOWN (yellow) — including which way to turn or tilt the cube before reading off each face.

Example input for a single face (already-solved orange face):

```
ooooooooo
```

Once all six faces are entered, the program validates that what you typed is actually a real, solvable cube (right sticker counts, valid corner/edge pieces, etc.), then prints the scrambled cube, solves it, and prints the solved result. If a stage of the algorithm gets stuck, it will say so and show its best effort.

## Limitations

- Input is manual (no camera/image scanning) — you type in the colors yourself, so accuracy depends on reading your cube correctly.
- This is a functional/educational solver, not an optimal (few-move) solver — it solves correctly but not necessarily in the minimum number of moves.

## License

MIT — see [LICENSE](LICENSE).
