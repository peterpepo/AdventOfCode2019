from commons.commons import read_puzzle_input
import os


def getCharCount(input_string):
    """
    Breaks input string into characters and counts occurrences of them.
    :param input_string: e.g. "01122211"
    :return: e.g. {'0':1, '1':4, '2':3}
    """
    char_count = {}

    for char in input_string:
        try:
            char_count[char] += 1
        except KeyError:
            char_count[char] = 1

    return char_count


def solve():
    """
    Advent Of Code 2019 - Day08 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file - input is single line
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day08_input.txt")[0]

    ROW_WIDTH = 25
    COL_HEIGHT = 6

    def solvePartOne():
        """Advent Of Code 2019 - Day08 - Part One Solution.
        :return: int
        """
        layers = []

        # Break input string into layers
        for idx_start in range(0, len(puzzle_input), ROW_WIDTH * COL_HEIGHT):
            # Calculate occurrences count for each character in layer
            layers.append(getCharCount(puzzle_input[idx_start:idx_start + ROW_WIDTH * COL_HEIGHT]))

        # Sort layers by occurrences of '0' character
        layers.sort(key=lambda x: x['0'] if '0' in x else 0)

        # Multiply occurrences of '1' by occurrences of '2'
        return layers[0]['1'] * layers[0]['2']

    def solvePartTwo():
        """Advent Of Code 2019 - Day08 - Part Two Solution.
        :return: int
        """
        top_layer = None

        # Loop through input string
        for idx_start in range(0, len(puzzle_input), ROW_WIDTH * COL_HEIGHT):
            # In case nothing is on top yet, copy first layer
            if top_layer is None:
                top_layer = puzzle_input[idx_start:ROW_WIDTH * COL_HEIGHT]
                continue

            # Construct new "top-to-bottom" view
            current_layer = ""
            # Loop through currently parsed layer
            for idx in range(ROW_WIDTH * COL_HEIGHT):
                # If top layer is transparent on top, display character from currently parsed layer
                if top_layer[idx] == '2':
                    current_layer += puzzle_input[idx_start + idx]
                # Otherwise display what is already on top
                else:
                    current_layer += top_layer[idx]

            # Set layer just calculated as new top layer
            top_layer = current_layer

        # Empty line to display nicely when running AdventOfCode2019.py from root package
        part_two_result = "\n"

        # Break layers into rows
        for row in range(COL_HEIGHT):
            # Break layers into columns
            for col in range(ROW_WIDTH):
                # Display pixel if it is BLACK
                if top_layer[row * ROW_WIDTH + col] == '1':
                    part_two_result += "#"
                # When white/transparent display nothing
                else:
                    part_two_result += "."
            part_two_result += "\n"

        return part_two_result

    return solvePartOne(), solvePartTwo()
