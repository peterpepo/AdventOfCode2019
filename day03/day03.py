from commons.commons import read_puzzle_input
import os


def solve():
    """
    Advent Of Code 2019 - Day03 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    def findCrossingPositions():
        """
        Returns dict of position indexed dicts of wire index and distance to that point, where the wires cross
        """
        # Read puzzle input from file - input is single line
        puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day03_input.txt")

        # (x,y) indexed dictionary of space occupied by wire, e.g. : (10, 20): set (1, 3) - on position (10, 20)
        #   there are two wires placed - with id 1 and 3
        wires_occupied = {}

        # Wire directions
        two_dim_directions = {
            "L": (-1, 0),
            "R": (1, 0),
            "U": (0, -1),
            "D": (0, 1)
        }

        # Loop through lines, each line is a wire
        for wire_idx in range(len(puzzle_input)):
            # Starting position of a wire
            wire_pos_x = 0
            wire_pos_y = 0

            # Total steps
            current_length = 0

            # Split line on comma to coordinates
            line_coordinates = puzzle_input[wire_idx].split(",")

            # Loop through all coordinates for single wire
            for line_coordinate in line_coordinates:
                section_direction = line_coordinate[:1]
                section_length = int(line_coordinate[1:])

                # Move section_length times in specified direction
                for i in range(section_length):
                    wire_pos_x += two_dim_directions[section_direction][0]
                    wire_pos_y += two_dim_directions[section_direction][1]

                    wire_pos = (wire_pos_x, wire_pos_y)

                    current_length += 1

                    # Place the wire into space
                    if wire_pos not in wires_occupied:
                        wires_occupied[wire_pos] = {}

                    if wire_idx not in wires_occupied[wire_pos]:
                        wires_occupied[wire_pos][wire_idx] = current_length

        # Return dict of position indexed dicts of wire index and distance to that point, where the wires cross
        return {key: value for (key, value) in wires_occupied.items() if len(value) >= len(puzzle_input)}

    def solvePartOne():
        """Advent Of Code 2019 - Day03 - Part One Solution.
        :return: int
        """
        part_one_result = list(findCrossingPositions().keys())  # All positions at which wires cross
        part_one_result.sort(key=lambda x: abs(x[0]) + abs(x[1]))  # Sort positions by manhattan distance
        part_one_result = part_one_result[0]  # Select first - 0th element
        return abs(part_one_result[0]) + abs(part_one_result[1])  # Return manhattan distance to position

    def solvePartTwo():
        """Advent Of Code 2019 - Day03 - Part Two Solution.
        :return: int
        """
        """
        for wire_idx_and_distance in findCrossingPositions().values() - loops through values - wire index and total
                distance to the point (please note, we are not interested in position itself), e.g. {0:250, 1:100}
        sum(wire_idx_and_distance.values()) - sum of values inside, e.g. 250 + 100
        min([]) - minimum of all values
        """
        return min([sum(wire_idx_and_distance.values()) for wire_idx_and_distance in findCrossingPositions().values()])

    return solvePartOne(), solvePartTwo()
