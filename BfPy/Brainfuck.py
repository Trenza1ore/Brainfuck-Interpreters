DEFAULT_SYMBOLS = ('>', '<', '+', '-', '.', ',', '[', ']')
def default_output(x):
    global print_buffer
    print_buffer += x.getval()
    print("\nCurrent output: %s\n" %(print_buffer))

class Cell:
    def __init__(self):
        self.__val = 0
    
    def inc(self):
        self.__val = (self.__val + 1) % 256
    
    def dec(self):
        self.__val = (self.__val - 1) % 256
    
    def setval(self, x: str):
        self.__val = ord(x[0])
    
    def getval(self):
        return chr(self.__val)
    
    def iszero(self):
        return self.__val is 0
    
    def __str__(self):
        return "%03d "%(self.__val)
    
    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self, memsize: int = 30000, symbols: tuple = DEFAULT_SYMBOLS, output = default_output):
        self.memory = [Cell() for _ in [None]*memsize]
        self.ptr = 0
        self.iptr = 0
        self.current = self.memory[self.ptr]
        self.symbols = symbols
        self.output = output
        self.operations = [self.rp, self.lp, self.ic, self.dc, self.op, self.ip, self.ls, self.le]
    
    def rp(self):
        self.ptr += 1
        self.current = self.memory[self.ptr]
    
    def lp(self):
        self.ptr -= 1
        self.current = self.memory[self.ptr]
    
    def ic(self):
        self.current.inc()
    
    def dc(self):
        self.current.dec()
    
    def op(self):
        self.output(self.current)
    
    def ip(self):
        self.current.setval(input("Waiting for input: "))
        
    def ls(self):
        if self.current.iszero():
            while self.instructions[self.iptr] != ']':
                self.iptr += 1
    
    def le(self):
        if not self.current.iszero():
            while self.instructions[self.iptr] != '[':
                self.iptr -= 1
    
    def interpret(self, x: str):
        global print_buffer
        print_buffer = ""
        self.ptr, self.iptr, length = 0, 0, len(x)
        self.instructions = x
        while self.iptr < length:
            if x[self.iptr] in self.symbols:
                self.operations[self.symbols.index(x[self.iptr])]()
            self.iptr += 1
        print("Output: %s" %(print_buffer))
    
    def dinterpret(self, x: str):
        global print_buffer
        print_buffer = ""
        self.ptr, self.iptr, length = 0, 0, len(x)
        self.instructions = x
        while self.iptr < length:
            print(repr(self))
            if x[self.iptr] in self.symbols:
                self.operations[self.symbols.index(x[self.iptr])]()
            self.iptr += 1
        print("Output: %s" %(print_buffer))

    def __str__(self):
        temp = ""
        for m in self.memory:
            temp += m.__str__()
        return temp
    
    def __repr__(self):
        return self.__str__() + '\n' + "    " * self.ptr + " ^\n" + self.instructions + '\n' + ' ' * self.iptr + '^\n'
