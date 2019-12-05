class IntCodes:
    def __init__(self):
        self.op_codes = {1: self.__addr_add__, 2: self.__addr_mult__, 99: self.__noop__}

    def __validate__(self, stack, index, read_len):
        if index + read_len > len(stack):
            return None
        args = [stack[i] for i in range(index, index + read_len)]
        return args

    def __addr_add__(self, stack, index):
        validated = self.__validate__(stack, index, 3)
        if not validated:
            raise BufferError
        a, b, store_at = validated
        stack[store_at] = stack[a] + stack[b]
        return index + 3

    def __addr_mult__(self, stack, index):
        validated = self.__validate__(stack, index, 3)
        if not validated:
            raise BufferError
        a, b, store_at = validated
        stack[store_at] = stack[a] * stack[b]
        return index + 3

    def __noop__(self, stack, index):
        return len(stack)

    def run_program(self, program):
        """Runs a program. To see supported op_codes, refer to __doc__
        
        Arguments:
            program {int[]} -- Array of integer opcodes
        
        Raises:
            Exception: BufferError
        
        Returns:
            None
        """
        if len(program) < 1:
            return
        exit_code = 0
        curr = 0
        while curr < len(program) - 1:
            op = program[curr]
            if op not in self.op_codes:
                raise Exception("unknown op code")
            try:
                func = self.op_codes[op]
                if func:
                    curr = func(program, curr + 1)
            except:
                print("program error")
                exit_code = 1
                break
        return exit_code, program
