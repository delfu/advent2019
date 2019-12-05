class IntCodes:
    def __init__(self):
        self.op_codes = {
            1: self.__addi__,
            2: self.__mult__,
            3: self.__input__,
            4: self.__output__,
            5: self.__jump_true__,
            6: self.__jump_false__,
            7: self.__less_than__,
            8: self.__equals__,
            99: self.__noop__,
        }
        self.input = None

    def __dereference__(self, modes, stack, *vals):
        for i in range(len(vals)):
            m = modes[i]
            if m == "0":
                yield stack[vals[i]]
            elif m == "1":
                yield vals[i]

    def __validate__(self, stack, index, read_len, modes):
        if index + read_len > len(stack):
            raise BufferError
        # pad modes to be same len as arguments
        if len(modes) < read_len:
            modes += "0" * (read_len - len(modes))

        args = [None for i in range(index, index + read_len)]
        for i in range(len(args)):
            m = modes[i]
            if m == "0":  # positional/addressing mode
                addr = stack[index + i]
                if addr > len(stack):
                    raise BufferError
                args[i] = addr
            elif m == "1":  # immediate mode, just read as val
                args[i] = stack[index + i]
        return args, modes

    def __addi__(self, stack, index, modes):
        validated, modes = self.__validate__(stack, index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, stack, a, b)
        stack[store_at] = a + b
        return index + 3

    def __mult__(self, stack, index, modes):
        validated, modes = self.__validate__(stack, index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, stack, a, b)
        stack[store_at] = a * b
        return index + 3

    def __input__(self, stack, index, modes):
        """read from input and store at next pointer
        
        Returns:
            index + 1
        """
        validated, modes = self.__validate__(stack, index, 1, modes)
        store_at = validated[0]
        if not self.input:
            raise ValueError("program executed without providing input")
        stack[store_at] = self.input
        return index + 1

    def __output__(self, stack, index, modes):
        """Prints
        """
        validated, modes = self.__validate__(stack, index, 1, modes)
        print(stack[validated[0]] if modes[0] == "0" else validated[0])
        return index + 1

    def __noop__(self, stack, index, modes):
        return len(stack)

    def __jump_true__(self, stack, index, modes):
        """Move execution pointer to 2nd param if 1st != 0
        """
        validated, modes = self.__validate__(stack, index, 2, modes)
        a, b = validated
        a, b = self.__dereference__(modes, stack, a, b)
        return b if a != 0 else index + 2

    def __jump_false__(self, stack, index, modes):
        """Move execution pointer to 2nd param if 1st == 0
        """
        validated, modes = self.__validate__(stack, index, 2, modes)
        a, b = validated
        a, b = self.__dereference__(modes, stack, a, b)
        return b if a == 0 else index + 2

    def __less_than__(self, stack, index, modes):
        """Store 1 in 3rd param if 1st < 2nd
        """
        validated, modes = self.__validate__(stack, index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, stack, a, b)
        stack[store_at] = 1 if a < b else 0
        return index + 3

    def __equals__(self, stack, index, modes):
        """Store 1 in 3rd param if 1st = 2nd
        """
        validated, modes = self.__validate__(stack, index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, stack, a, b)
        stack[store_at] = 1 if a == b else 0
        return index + 3

    def run_program(self, program, input=None):
        """Runs a program. To see supported op_codes, refer to __doc__
        
        Arguments:
            program {int[]} -- Array of integer opcodes
        
        Raises:
            Exception: BufferError
        
        Returns:
            Exit code, memory
        """
        self.input = input

        if len(program) < 1:
            return
        exit_code = 0
        curr = 0
        while curr < len(program) - 1:
            op = str(program[curr])
            modes = op[:-2][::-1]  # parameter modes
            op = int(op[-2:])

            if op not in self.op_codes:
                raise Exception("unknown op code", op)
            try:
                func = self.op_codes[op]
                if func:
                    curr = func(program, curr + 1, modes)
            except (ValueError, BufferError) as e:
                print(e)
                exit_code = 1
                break
        print("Program exited with exit code: " + str(exit_code))
        return exit_code, program
