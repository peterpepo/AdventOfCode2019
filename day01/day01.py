from commons.commons import read_puzzle_input
import os


def solve():
    """
    Advent Of Code 2019 - Day01 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day01_input.txt")

    def calculateFuelRequired(mass):
        """
        Calculates fuel required for defined mass.
        :param mass: (int) mass for which the required fuel is calculated
        :return: (int) fuel required
        """
        return max(mass // 3 - 2, 0)

    def calculateFuelRequiredIncludingOwnMass(mass):
        """
        Calculate fuel required for a defined mass including self mass (i.e. pumping fuel to the tank increases the mass,
        so we need another fuel to carry the previously tanked fuel.
        This goes on until adding to the tank doesn't require additional fuel)
        :param mass: (int) mass for which the required fuel is calculated
        :return: (int) fuel required
        """
        # First we calculate fuel to carry the mass.
        fuel_required = calculateFuelRequired(mass)

        # Second if we added fuel to tank, we calculate fuel to carry "previous' fuel
        if fuel_required > 0:
            fuel_required += calculateFuelRequiredIncludingOwnMass(fuel_required)

        return fuel_required

    def solvePartGeneric(function_name):
        """
        Generic day01 puzzle solver.
        :param function_name: function used to calculate required fuel
        """
        total_fuel_required = 0  # Total fuel required

        # Loop through all rockets
        for puzzle_instruction in puzzle_input:
            # Add fuel required for current rocket, based on defined function
            total_fuel_required += function_name(int(puzzle_instruction))

        return total_fuel_required

    def solvePartOne():
        """Advent Of Code 2019 - Day01 - Part One Solution.
        :return: int
        """
        # Fuel weight for rocket mass only
        return solvePartGeneric(calculateFuelRequired)

    def solvePartTwo():
        """Advent Of Code 2019 - Day01 - Part Two Solution.
        :return: int
        """
        # Fuel weight including both rocket and self weight
        return solvePartGeneric(calculateFuelRequiredIncludingOwnMass)

    return solvePartOne(), solvePartTwo()
