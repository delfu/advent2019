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
        self.stack = []

    def __dereference__(self, modes, *vals):
        for i in range(len(vals)):
            m = modes[i]
            if m == "0":
                if vals[i] > len(self.stack):
                    raise BufferError("Dereferencing beyond program memory")
                yield self.stack[vals[i]]
            elif m == "1":
                yield vals[i]

    def __validate__(self, index, read_len, modes):
        if index + read_len > len(self.stack):
            raise BufferError("Reading beyond the program memory")
        # pad modes to be same len as arguments
        modes += "0" * (read_len - len(modes))

        args = [self.stack[i] for i in range(index, index + read_len)]

        return args, modes

    def __addi__(self, index, modes):
        validated, modes = self.__validate__(index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, a, b)
        self.stack[store_at] = a + b
        return index + 3

    def __mult__(self, index, modes):
        validated, modes = self.__validate__(index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, a, b)
        self.stack[store_at] = a * b
        return index + 3

    def __input__(self, index, modes):
        """Read from input and store at next pointer
        
        Returns:
            index + 1
        """
        validated, modes = self.__validate__(index, 1, modes)
        store_at = validated[0]
        if not self.input:
            raise ValueError("program executed without providing input")
        self.stack[store_at] = self.input
        return index + 1

    def __output__(self, index, modes):
        """Prints
        """
        validated, modes = self.__validate__(index, 1, modes)
        print(self.stack[validated[0]] if modes[0] == "0" else validated[0])
        return index + 1

    def __noop__(self, index, modes):
        return len(self.stack)

    def __jump_true__(self, index, modes):
        """Move execution pointer to 2nd param if 1st != 0
        """
        validated, modes = self.__validate__(index, 2, modes)
        a, b = validated
        a, b = self.__dereference__(modes, a, b)
        return b if a != 0 else index + 2

    def __jump_false__(self, index, modes):
        """Move execution pointer to 2nd param if 1st == 0
        """
        validated, modes = self.__validate__(index, 2, modes)
        a, b = validated
        a, b = self.__dereference__(modes, a, b)
        return b if a == 0 else index + 2

    def __less_than__(self, index, modes):
        """Store 1 in 3rd param if 1st < 2nd
        """
        validated, modes = self.__validate__(index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, a, b)
        self.stack[store_at] = 1 if a < b else 0
        return index + 3

    def __equals__(self, index, modes):
        """Store 1 in 3rd param if 1st = 2nd
        """
        validated, modes = self.__validate__(index, 3, modes)
        a, b, store_at = validated
        a, b = self.__dereference__(modes, a, b)
        self.stack[store_at] = 1 if a == b else 0
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
        self.stack = program

        if len(self.stack) < 1:
            return
        exit_code = 0
        ptr = 0
        while ptr < len(self.stack):
            op = str(self.stack[ptr])
            modes = op[:-2][::-1]  # parameter modes
            op = int(op[-2:])

            if op not in self.op_codes:
                raise Exception("unknown op code", op)
            try:
                func = self.op_codes[op]
                ptr = func(ptr + 1, modes)
            except (ValueError, BufferError) as e:
                print(e)
                exit_code = 1
                break
        print("Program exited with exit code: " + str(exit_code))
        return exit_code, self.stack
