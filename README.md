# Advent of Code Utilities

This repository contains the utilities I use for solving [Advent of Code](https://adventofcode.com) challenges.
While I usually solve the challenges in Python, you may find the tooling useful for other languages as well.

I use part of [exoji2e's `runner.py` script](https://github.com/exoji2e/aoc22)
to automatically download the input for a given day. To reduce redundant code
and keep the solutions self-contained, the rest of my setup uses the Visual Studio Code (VSCode)
extension
[terminal-command-keys](https://marketplace.visualstudio.com/items?itemName=petekinnecom.terminal-command-keys)
to partially automate the most common steps. The corresponding configuration is found in `keybindings.json`.

The utilities in this repository are written for UNIX-based systems and _will not work_ on Windows.

## Structure

The `prepare.py` script creates a new directory given a day number (integer) `X`
called `dayX`. The template is copied from `template/` to the new directory. The
input is downloaded and saved to `inputs/input.in` in the new directory. 

The directory contains the empty file `input/sample.in` to which you can copy
the sample input from the challenge description. If there are multiple sample
inputs you want to test your solution against, you can create a file for each in
the input folder whose name matches the shell substitution `s*.in`, the provided
commands will automatically run all of them.

Template scripts for part 1 and part 2 are designed to be very minimal and read
the input from stdin, as is common in competitive programming. Moreover, the
template script for part2 assumes you have already solved part 1 in a way that
it does not have to be modified and part2 can build on it.

Most of the template code is a function called `debug`, which prints its input
if the respective script is run with the `-v` flag. This way, the provided key
bindings can switch between running the script with and without debug output.

## Prerequisites

- Copy your session token from adventofcode.com to a file called `secret.py` and assign it as a string to the variable `session` (see `secret.py.example`)
- Make sure `YEAR` in `prepare.py` is set to the year you want to solve the challenges for
- Check that required packages for `prepare.py` are installed: (`pip3 -r requirements.txt`)
- (Optional, but recommended) Install and configure `terminal-command-keys`:
    - Copy the content of `keybindings.json` to your VSCode keybindings (Ctrl+Shift+P -> "Preferences: Open Keyboard Shortcuts (JSON)")
    - Check that keybindings do not interfere with your default ones; You will most likely have to change the prefix for the keybindings to something other than `Ctrl+A` if you are not using `vim` keybindings. 
    - If you are using `bash` or `zsh`, modify all keybindings with loops and/or command substitution. `keybindings.json` contains commented out commands that should work for `bash` and `zsh`.


## Keybindings (Cheat Sheet)

The following keybindings are available, all are prefixed with `Ctrl+A` such
that they do not interfere with VSCode's `vim` keybindings. Note that a
keybinding that is separated by spaces indicates subsequent key presses, e.g.
`Ctrl+A S` means press `Ctrl+A` _followed by_ `S` (`Ctrl+A` has to be released in between).

- All of the following commands execute the _currently open file_ in the editor.
"With debug output" refers to the script being run with the `-v` flag, which is
the switch for debug output in the template scripts.
    - `Ctrl+A S` (_"**S**amples"_): Run all samples
    - `Ctrl+A D` (_"**D**ebug"_): Run all samples with debug output
    - `Ctrl+A I` (_"**I**nput"_): Run input
    - `Ctrl+A V` (_"**V**erbose"_): Run input _with_ debug output
    - `Ctrl+A U` (_"s**U**bmit"_): Run input (no debug output) and copy the result to the clipboard using `xclip`
- The last two commands are meant for general workflow:
    - `Ctrl+A P` (_"**P**repare"_): Create a new directory for the current day using `prepare.py`, downloading the input and `cd`-ing to the new directory. This has the added benefit of spawning a `terminal-command-keys` terminal if there is no active one.
    - `Ctrl+A 2` (_"part **2**"_), only valid when in a `dayX` directory: Copy `part1.py` to `part2.py`, prompt the user if they want to overwrite if there is an existing file.

## Intended Workflow

1) Create a new directory for the current day using `Ctrl+A P` and watch the countdown if you start the script before the challenge is released
    - *Note*: This assumes you are doing the challenge on the day they are released or replay them in some other month/year on the same day of month. 
    - If you are doing them at some other time, you will have to run `prepare.py` for the intended day. In this case, spawn a new `terminal-command-keys` terminal (this is most easily achieved using some other registered keybinding) and `cd` to the newly created directory.
2) Copy the sample input to `inputs/sample.in`
3) Write your solution for part 1 in `part1.py`.
4) Copy the solution output to your clipboard `Ctrl+A U` and paste it into the solution box on adventofcode.com
    - (Optional) If you need to heavily modify part 1, copy it to `part2.py` using `Ctrl+A 2`
5) Write your solution for `part2.py` and submit your solution in the same way as for part 1.
