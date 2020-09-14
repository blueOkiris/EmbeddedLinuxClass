# Etch-A-Sketch (HW02)

## Description

A small etch-a-sketch game written in python that uses buttons for input

## Running

To run:

1) In a terminal type:

   ```
   chmod +x ./etch-a-sketch.py
   ```

2) and then run with

   ```
   ./etch-a-sketch.py
   ```

View controls and cli options:

1) Run with the option `--help`:

   ```
   ./etch-a-sketch.py --help
   ```

   To see command line options and also the controls for the game

## Documentation

Here is a class diagram for the system:

![class diagram](../docs/etch-a-sketch-class.png)

And here is a rough sequence diagram for how it all connects and functions:

![sequence diagram](../docs/etch-a-sketch-seq.png)

Note also that key press sequences, which aren't shown, are fairly simple and exist solely in the Game class. Basically when 'setKey' happens, key pressed booleans get set true, and when they get set false, it sets key-released booleans, which stay on until that input is handled. So when 'w' is pressed and released, the game class will move its cursor, draw the new cursor point, and then set the 'w' release to false
