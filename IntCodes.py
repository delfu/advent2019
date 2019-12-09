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
            9: self.__relative__,
            99: self.__noop__,
        }
        self.input = []
        self.stack = []
        self.relative_base = 0

    def __read_at__(self, modes, *vals):
        for i in range(len(vals)):
            m = modes[i]
            if m == "0":
                if vals[i] >= len(self.stack):
                    yield 0
                elif vals[i] < 0:
                    raise BufferError("Dereferencing beyond program memory")
                else:
                    yield self.stack[vals[i]]
            elif m == "1":
                yield vals[i]

    def __get_args__(self, index, read_len, modes):
        if index + read_len < 0:
            raise BufferError("Reading beyond the program memory")
        # pad modes to be same len as arguments
        modes += "0" * (read_len - len(modes))

        args = [
            self.stack[i] if i < len(self.stack) else 0
            for i in range(index, index + read_len)
        ]
        # transform relative mode (2) to positional mode (0)
        for i, m in enumerate(modes):
            if m == "2":
                args[i] = args[i] + self.relative_base
                modes = modes[:i] + "0" + modes[i + 1 :]

        return args, modes

    def __safe_store__(self, index, val):
        if index >= len(self.stack):
            self.stack.extend([0] * (index - len(self.stack) + 1))
        elif index < 0:
            raise BufferError("storing with negative address")
        self.stack[index] = val

    def __addi__(self, index, modes):
        args, modes = self.__get_args__(index, 3, modes)
        a, b, store_at = args
        a, b = self.__read_at__(modes, a, b)
        self.__safe_store__(store_at, a + b)
        return index + 3, None

    def __mult__(self, index, modes):
        args, modes = self.__get_args__(index, 3, modes)
        a, b, store_at = args
        a, b = self.__read_at__(modes, a, b)
        self.__safe_store__(store_at, a * b)
        return index + 3, None

    def __input__(self, index, modes):
        """Read from input and store at next pointer
        
        Returns:
            index + 1
        """
        if len(self.input) == 0:
            raise ValueError("program executed without providing input")
        args, modes = self.__get_args__(index, 1, modes)
        store_at = args[0]
        input = self.input.pop(0)
        self.__safe_store__(store_at, input)
        return index + 1, None

    def __output__(self, index, modes):
        """Prints
        """
        args, modes = self.__get_args__(index, 1, modes)
        output = next(self.__read_at__(modes, args[0]))
        return index + 1, output

    def __noop__(self, index, modes):
        return len(self.stack), None

    def __jump_true__(self, index, modes):
        """Move execution pointer to 2nd param if 1st != 0
        """
        args, modes = self.__get_args__(index, 2, modes)
        a, b = args
        a, b = self.__read_at__(modes, a, b)
        return (b if a != 0 else index + 2), None

    def __jump_false__(self, index, modes):
        """Move execution pointer to 2nd param if 1st == 0
        """
        args, modes = self.__get_args__(index, 2, modes)
        a, b = args
        a, b = self.__read_at__(modes, a, b)
        return (b if a == 0 else index + 2), None

    def __less_than__(self, index, modes):
        """Store 1 in 3rd param if 1st < 2nd
        """
        args, modes = self.__get_args__(index, 3, modes)
        a, b, store_at = args
        a, b = self.__read_at__(modes, a, b)
        self.__safe_store__(store_at, 1 if a < b else 0)
        return index + 3, None

    def __equals__(self, index, modes):
        """Store 1 in 3rd param if 1st = 2nd
        """
        args, modes = self.__get_args__(index, 3, modes)
        a, b, store_at = args
        a, b = self.__read_at__(modes, a, b)
        self.__safe_store__(store_at, 1 if a == b else 0)
        return index + 3, None

    def __relative__(self, index, modes):
        """ adjusts relative base
        """
        args, modes = self.__get_args__(index, 1, modes)
        offset = args[0]
        offset = next(self.__read_at__(modes, offset))
        self.relative_base += offset
        return index + 1, None

    def run_program(self, program, input=[]):
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
        self.relative_base = 0

        if len(self.stack) < 1:
            return
        ptr = 0
        while ptr < len(self.stack):
            op = str(self.stack[ptr])
            modes = op[:-2][::-1]  # parameter modes
            op = int(op[-2:])

            if op not in self.op_codes:
                raise Exception("unknown op code", op)
            try:
                func = self.op_codes[op]
                ptr, output = func(ptr + 1, modes)
                if output is not None or op == 99:
                    yield output
            except (ValueError, BufferError) as e:
                print(e)
                break
        # print("Program exited with exit code: " + str(exit_code))
