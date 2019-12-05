class __TestCase__:
    def __init__(self, result):
        self.result = result

    def equals(self, comparison):
        assert self.result == comparison
        return self

    def toBeTruthy(self):
        assert type(self.result) == "bool"
        assert self.result
        return self

    def toBeFalsey(self):
        assert type(self.result) == "bool"
        assert not self.result
        return self


def expect(result):
    return __TestCase__(result)

