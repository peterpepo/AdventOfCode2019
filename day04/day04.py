from commons.commons import read_puzzle_input
import os


def solve():
    """
    Advent Of Code 2019 - Day04 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    def containsTwoOrMoreSameInRow(string_to_check):
        """
        Checks, whether string contains two or more same characters in a row. (e.g.: aBBcde)
        @param string_to_check: String, on which the check is performed.
        @return: True/False
        """
        for idx in range(1, len(string_to_check)):
            if string_to_check[idx] == string_to_check[idx - 1]:
                return True

        return False

    def containsExactlyTwoSameInRow(string_to_check):
        """
        Checks, whether string contains exactly two same characters in a row. (e.g.: aBBcde, but not aBBBcde - triple B)
        @param string_to_check: String, on which the check is performed.
        @return: True/False
        """
        same_in_row = 1  # Counter how many of same character has been find in row

        # Loop through string, starting from 1st position (1 is 2nd in row)
        for idx in range(1, len(string_to_check)):
            # Increase counter, in case character is same as previous
            if string_to_check[idx] == string_to_check[idx - 1]:
                same_in_row += 1
            else:
                # If different character is found, check whether previous character has occured exactly twice in row
                if same_in_row == 2:
                    return True
                # Reset counter
                same_in_row = 1
        # Check whether current character has occured twice in row again - this is useful in situations, where twin occurs
        # at the end of checked string - in such case we didn't detect in previous if statement
        return same_in_row == 2

    def digitsNeverDecrease(string_to_check):
        """
        Checks, whether numbers in string are not decreasing (e.g. : 12345, 12234 are fine, 1243 - 3 after 4 NOK)
        @param string_to_check: String, on which the check is performed.
        @return: True/False
        """
        for idx in range(1, len(string_to_check)):
            if int(string_to_check[idx]) < int(string_to_check[idx - 1]):
                return False
        return True

    # Read puzzle input from file - input is single line
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day04_input.txt")[0]

    password_min, password_max = [int(x) for x in puzzle_input.split("-")]

    def solvePartOne():
        """Advent Of Code 2019 - Day04 - Part One Solution.
        :return: int
        """
        part_one_correct_counter = 0
        for password in range(password_min, password_max + 1):
            password_to_check = str(password)
            if digitsNeverDecrease(password_to_check) and containsTwoOrMoreSameInRow(password_to_check):
                part_one_correct_counter += 1

        return part_one_correct_counter

    def solvePartTwo():
        """Advent Of Code 2019 - Day04 - Part Two Solution.
        :return: int
        """
        part_two_correct_counter = 0

        for password in range(password_min, password_max + 1):
            password_to_check = str(password)
            if digitsNeverDecrease(password_to_check) and containsExactlyTwoSameInRow(password_to_check):
                part_two_correct_counter += 1

        return part_two_correct_counter

    return solvePartOne(), solvePartTwo()
