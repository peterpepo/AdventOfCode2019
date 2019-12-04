from commons.commons import read_puzzle_input
import os


def solve():
    """
    Advent Of Code 2019 - Day02 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Store parsed puzzle input "globally" to avoid re-reading input file in part-two of the puzzle. We copy parsed program instead.
    # Read puzzle input from file - input is single line
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day02_input.txt")[0]

    # Split input on "," to list of integers
    REGISTER_SPLITTER = ","
    puzzle_input_program = [int(x) for x in puzzle_input.split(REGISTER_SPLITTER)]

    def runProgram(input_program, register_one, register_two):
        program_registers = input_program[:]  # Create copy of a program in computers "internal memory"
        program_registers[1] = register_one  # Modify register 1 to specified value
        program_registers[2] = register_two  # Modify register 2 to specified value

        program_position = 0
        while True:
            # 1) Get current instruction
            current_instruction = program_registers[program_position]

            # 2) If it is 1, add values of register index on current + 1 and current + 2 to register index on current + 3 offset
            """ Explaining program_registers[program_registers[program_position + 3]]
            program_position + 3 - is third element to the right from current position
            program_registers[program_position + 3] - is the id of register which needs to be modified
            program_registers[program_registers[program_position + 3]] - is actual value at position which needs to be modified
            """
            if current_instruction == 1:
                program_registers[program_registers[program_position + 3]] = program_registers[program_registers[
                    program_position + 1]] + program_registers[program_registers[program_position + 2]]
            # 2) If it is 2, multiply values
            elif current_instruction == 2:
                program_registers[program_registers[program_position + 3]] = program_registers[program_registers[
                    program_position + 1]] * program_registers[program_registers[program_position + 2]]
            # 2) Terminate the program in case instruction 99 is found
            elif current_instruction == 99:
                break

            # 3) Jump 4 positions ahead
            program_position += 4

        # 4) Return value in 0th register
        return program_registers[0]

    def solvePartOne():
        """Advent Of Code 2019 - Day02 - Part One Solution.
        :return: int
        """
        # Set register one to 12 and register two to 2
        return runProgram(puzzle_input_program, 12, 2)

    def solvePartTwo():
        """Advent Of Code 2019 - Day02 - Part Two Solution.
        :return: int
        """
        EXPECTED_OUTPUT = 19690720  # Constant, value in register 0 we are looking for

        # Try values from 0 to 99 for noun
        for noun in range(100):
            # Try values from 0 to 99 for verb
            for verb in range(100):
                if runProgram(puzzle_input_program, noun, verb) == EXPECTED_OUTPUT:
                    return 100 * noun + verb

    return solvePartOne(), solvePartTwo()
