from commons.commons import read_puzzle_input
import os


class Planet():
    def __init__(self):
        self.sun_planet = None

    def setSunPlanet(self, sun_planet):
        self.sun_planet = sun_planet

    def getAllSuns(self):
        """
        Returns path - list of planets from CENTER to PLANET (CENTER as 0th, PLANET as last element)
        """
        if self.sun_planet is None:
            return []
        else:
            all_suns = self.sun_planet.getAllSuns().copy()
            all_suns.append(self.sun_planet)
            return all_suns


def solve():
    """
    Advent Of Code 2019 - Day06 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day06_input.txt")

    # Split input on ")" to sun and orbiting planets
    LINE_SPLITTER = ")"

    # Planets dict indexed by planet name
    planets = {}

    # Get or create planet with specified name
    def getOrCreatePlanet(planet_name):
        try:
            return planets[planet_name]
        except KeyError:
            new_planet = Planet()
            planets[planet_name] = new_planet
            return new_planet

    # Loop through puzzle input
    for puzzle_input_line in puzzle_input:
        # Parse sun and orbiting planets out of input
        sun_planet_name, orbiting_planet_name = puzzle_input_line.strip().split(LINE_SPLITTER)

        # Get (or create) both planets and set the orbiting planet to orbit around sun
        # This is necessary, as planet's sun may be unknown at time of parsing input, e.g.: B)C, A)B (first we created
        # planet B, but learned later, that it orbits around planet A)
        getOrCreatePlanet(orbiting_planet_name).setSunPlanet(getOrCreatePlanet(sun_planet_name))

    def solvePartOne():
        """Advent Of Code 2019 - Day06 - Part One Solution.
        :return: int
        """
        # Loop through all planets and find how many planets does it orbit direct and undirect
        total_orbits = 0

        for planet in planets.values():
            total_orbits += len(planet.getAllSuns())

        return total_orbits

    def solvePartTwo():
        """Advent Of Code 2019 - Day06 - Part Two Solution.
        :return: int
        """
        # All planets from SAN to centre of universe (SAN excluding) - distance increasing from left to right
        san_to_center_path = planets["SAN"].getAllSuns()
        # All planets from YOU to centre of universe (YOU excluding)
        you_to_center_path = planets["YOU"].getAllSuns()

        # Planets which are common for both paths
        common_path_to_center = [x for x in san_to_center_path if x in you_to_center_path]

        # Rightmost (or first common) is the planet which is closest to SAN and YOU
        # (since each planet can have only single sun - parent in graph, the first (rightmost) path is shortest.
        # There are no shortcuts in the space. If we moved one step closed, we would need to take that same step back
        # (remember, there is only one way to each of planets).
        first_common_planet = common_path_to_center[-1]

        # Find how many steps are required from SAN to COMMON planet and YOU to COMMON planet. Substract 2
        # (we don't need to actually step on COMMON planet. Being on the orbit is enough. Those two hops are TO
        # and FROM common planet)
        # As our path is given as SUN-DIST_N-COMMON-DIST_2-DIST_1-(PLANET - not actual part of path), we get
        # the distance from PLANET to COMMON as path_length - index(COMMON),
        # for example: total hops to sun(len) = 5, index(COMMON) = 2, distance = 5-2 = 3
        san_to_you_steps_count = len(san_to_center_path) - san_to_center_path.index(first_common_planet) + \
                                 len(you_to_center_path) - you_to_center_path.index(first_common_planet) - 2

        return san_to_you_steps_count

    return solvePartOne(), solvePartTwo()
