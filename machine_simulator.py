from parser import MachineParser

class AbstractMachineSimulator:
    def __init__(self, input_text):
        self.parser = MachineParser(input_text)
        self.memory = self.parser.memory
        self.logic = self.parser.logic
        self.initial_state = self.parser.initial_state
        self.halt = False
        self.accept = False

# # Example Usage
# input_text = """
# .DATA
# STACK S1
# QUEUE Q1
# TAPE T1
# .LOGIC
# A] WRITE(S1) (1,B)
# B] SCAN (0,C), (1,D), (2,E)
# C] SCAN LEFT (0,C), (1,reject)
# D] SCAN RIGHT (b,D), (c,F), (#,F)
# E] PRINT (0,C), (1,D), (2,E)
# F] READ(S1) (#,E)
# G] LEFT(T1) (0/0,C), (Y/Y,C), (X/X,A)
# H] RIGHT(T1) (Y/Y,D), (#/#,accept), (1/1,reject)
# I] UP(T1) (0/0,B), (Y/Y,B), (1/Y,C)
# K] DOWN(T1) (0/0,C), (Y/Y,C), (X/X,A)
# """

# parser = AbstractMachineSimulator(input_text)
# print(parser.memory)
