# maze-generation
This program generates maze and displays the solution of the generated maze.

Required installations.
```
pip install pygame
```

You can change generated maze's size by changing WIDTH, HEIGHT and BOX_WIDTH constants. Simply put, this script generates (WIDTH / BOX_WIDTH) by (HEIGHT / BOX_WIDTH) mazes.

The reason behind this logic is that PyGame generates WIDTH x HEIGHT window and our grid system which is actually set of individual cells, is located on this window (size of each cell is defined as BOX_WIDTH). Therefore, program can show WIDTH / BOX_WIDTH cells on x axis, and HEIGHT / BOX_WIDTH on y axis.

Moreover, entry and exit points of the maze is pre-defined (in main.py, line:23 to 27).
