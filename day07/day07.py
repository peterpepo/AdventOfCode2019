from commons.commons import read_puzzle_input
from itertools import permutations
import os


class VirtualMachine():
    def __init__(self, program_instructions):
        """
        Creates virtual machine, copy of program in internal memory and moves instruction pointer to beginning of program.
        :param program_instructions: [] program
        :param systemid: id of a system
        """
        self.registers = program_instructions[:]
        self.instruction_pointer = 0
        self.machine_input = []
        self.machine_output = []
        self.input_read_times = 0
        self.stopped = False

    def setInput(self, input):
        """
        Sets input for machine.
        :param input: list of parameters
        """
        self.machine_input = input[:]

    def getRegisterValue(self, register_mode_index_tuple):
        """
        Returns value of a register, based on mode.
        For position mode, register with index value is returned - self.registers[value].
        For immediate mode, value itself is returned.
        """
        param_mode, param_value = register_mode_index_tuple

        if param_mode == 0:  # position mode 0
            return self.registers[param_value]
        else:  # immediate mode 1
            return param_value

    def runProgram(self):
        """
        Runs program in virtual machine memory.
        """

        # Run program forever
        while True:
            # 1) Load single instruction - opcode + register modes
            param0 = self.registers[self.instruction_pointer]  # parameter 0 (op_code + parameter modes)
            self.instruction_pointer += 1  # increase instruction pointer by one

            opcode = param0 % 100  # Get opcode out of first parameter - two rightmost numbers

            # 2) Find how many additional parameters we need to read, based on instruction type
            if opcode in (1, 2, 7, 8):
                additional_parameters_count = 3
            elif opcode in (3, 4):
                additional_parameters_count = 1
            elif opcode in (5, 6):
                additional_parameters_count = 2
            elif opcode in (99,):
                additional_parameters_count = 0

            # 3a) Load modes for additional parameters - two rightmost digits (ones and tens are opcode),
            # the rest to the left hundreds, thousands, ten-thousands digits are modes for parameters from 1 to n,
            # e.g. ABCDEF -> opcode = EF, D=param1 mode, C=param2 mode, B=param3 mode, A=param4 mode
            #
            # How to get e.g thousands digit: get remainder after division one magnitude higher,
            # then whole-number divide (floor) by same magnitude,
            # example: get thousands of 12345: 12345 % 10000 = 2345; 2345 // 1000 = 2 - thousands digit is 2
            param_modes = [param0 % (1000 * pow(10, par_mode)) // (100 * pow(10, par_mode)) for par_mode in
                           range(0, additional_parameters_count)]

            # 3b) Load additional parameters
            param_values = [self.registers[idx] for idx in
                            range(self.instruction_pointer, self.instruction_pointer + additional_parameters_count)]

            # 3c) Join parameter modes and parameters into list of sets [(par1_mode, par1_val), (par2_mode, par2_val),..]
            parameters = list(zip(param_modes, param_values))

            # 4) Increase instruction pointer by number of parameters, which have been read
            self.instruction_pointer += additional_parameters_count

            # 5) Process instruction
            # Assignments are always treated as IMMEDIATE, in contrary to puzzle requirements, and I explain why:
            # position assignment to register 4 would mean, that we get value out of register 4, for example 8 and
            # then store value in register 8. Value must be stored in 4 instead. This means, that assignments are
            # always treated as immediate.
            #
            # example: self.getRegisterValue((1, parameters[2][1])) - we manually change mode of this parameter to (1, value) - immediate

            if opcode == 1:  # Addition
                self.registers[self.getRegisterValue((1, parameters[2][1]))] = self.getRegisterValue(
                    parameters[0]) + self.getRegisterValue(parameters[1])
            elif opcode == 2:  # Multiplication
                self.registers[self.getRegisterValue((1, parameters[2][1]))] = self.getRegisterValue(
                    parameters[0]) * self.getRegisterValue(parameters[1])
            elif opcode == 3:  # Read Input
                # in case, input is read first time, it is phase setting
                if self.input_read_times == 0:
                    self.registers[self.getRegisterValue((1, parameters[0][1]))] = self.machine_input[0]
                # otherwise it is "power input" and it stays for consequents reading
                else:
                    self.registers[self.getRegisterValue((1, parameters[0][1]))] = self.machine_input[-1]

                self.input_read_times += 1

            elif opcode == 4:  # Write output
                self.machine_output.append(self.getRegisterValue(parameters[0]))
                break
            elif opcode == 5:  # Jump-if-true
                if self.getRegisterValue(parameters[0]) != 0:
                    self.instruction_pointer = self.getRegisterValue(parameters[1])
            elif opcode == 6:  # Jump-if-false
                if self.getRegisterValue(parameters[0]) == 0:
                    self.instruction_pointer = self.getRegisterValue(parameters[1])
            elif opcode == 7:  # Less than
                if self.getRegisterValue(parameters[0]) < self.getRegisterValue(parameters[1]):
                    self.registers[self.getRegisterValue((1, parameters[2][1]))] = 1
                else:
                    self.registers[self.getRegisterValue((1, parameters[2][1]))] = 0
            elif opcode == 8:  # Equals
                if self.getRegisterValue(parameters[0]) == self.getRegisterValue(parameters[1]):
                    self.registers[self.getRegisterValue((1, parameters[2][1]))] = 1
                else:
                    self.registers[self.getRegisterValue((1, parameters[2][1]))] = 0
            elif opcode == 99:  # Terminate program
                self.stopped = True
                break

    def isStopped(self):
        return self.stopped

    def getDiagnosticCode(self):
        """
        Returns diagnostic code of a machine - last entry in machine output.
        """
        return self.machine_output[-1]


def solve():
    """
    Advent Of Code 2019 - Day07 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Store parsed puzzle input "globally" to avoid re-reading input file in part-two of the puzzle. We copy parsed program instead.
    # Read puzzle input from file - input is single line
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day07_input.txt")[0]

    # Split input on "," to list of integers
    REGISTER_SPLITTER = ","
    puzzle_input_program = [int(x) for x in puzzle_input.split(REGISTER_SPLITTER)]

    def solvePartOne():
        """Advent Of Code 2019 - Day07 - Part One Solution.
        :return: int
        """
        amplifiers_config_options = permutations([i for i in range(5)])

        # Answer for part one - maximum output
        max_amplifiers_output = 0

        # Try every possible phase permutation
        for amplifier_config_option in amplifiers_config_options:

            previous_machine_output = 0  # Output of previous amplifier, initialized to 0 (0 input to 0th amplifier)

            # Create five machines
            amplifiers_count = 5
            amplifiers = [VirtualMachine(puzzle_input_program) for i in range(amplifiers_count)]

            # Convert permutation object to list
            amplifiers_config = list(amplifier_config_option)

            # Order of amplifier to be started
            amplifier_offset = 0

            # Run all machines
            for i in range(amplifiers_count):
                # Construct configuration, consisting of [phase, previous_output]
                amplifier_config = [amplifiers_config[amplifier_offset % amplifiers_count], previous_machine_output]

                # Load and set input for current virtual machine/amplifier
                current_vm = amplifiers[amplifier_offset % amplifiers_count]
                current_vm.setInput(amplifier_config)

                # Run program on machine (until it stops, or outputs new value)
                current_vm.runProgram()

                # Get output value from current machine
                previous_machine_output = current_vm.getDiagnosticCode()

                amplifier_offset += 1

            # Store new maximum
            if previous_machine_output > max_amplifiers_output:
                max_amplifiers_output = previous_machine_output

        return max_amplifiers_output

    def solvePartTwo():
        """Advent Of Code 2019 - Day07 - Part Two Solution.
        :return: int
        """
        # All configuration options - permutations of [5, 6, 7, 8, 9]
        amplifiers_config_options = permutations([i for i in range(5, 10)])

        # Answer for part two - maximum output
        max_amplifiers_output = 0

        # Try every possible phase permutation
        for amplifier_config_option in amplifiers_config_options:

            previous_machine_output = 0  # Output of previous amplifier, initialized to 0 (0 input to 0th amplifier)

            # Create five machines
            amplifiers_count = 5
            amplifiers = [VirtualMachine(puzzle_input_program) for i in range(amplifiers_count)]

            # Convert permutation object to list
            amplifiers_config = list(amplifier_config_option)

            # Order of amplifier to be started
            amplifier_offset = 0

            # loop until last-4th machine stops
            while not amplifiers[4].isStopped():
                # Construct configuration, consisting of [phase, previous_output]
                amplifier_config = [amplifiers_config[amplifier_offset % amplifiers_count], previous_machine_output]

                # Load and set input for current virtual machine/amplifier
                current_vm = amplifiers[amplifier_offset % amplifiers_count]
                current_vm.setInput(amplifier_config)

                # Run program on machine (until it stops, or outputs new value)
                current_vm.runProgram()

                # Get output value from current machine
                previous_machine_output = current_vm.getDiagnosticCode()

                amplifier_offset += 1

            # Store new maximum
            if previous_machine_output > max_amplifiers_output:
                max_amplifiers_output = previous_machine_output

        return max_amplifiers_output

    return solvePartOne(), solvePartTwo()
