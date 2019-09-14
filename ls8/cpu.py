"""CPU functionality."""

import sys

# Global Operation Variables
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011
# Globals
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.running = True

    def load(self):
        """Load a program into memory."""
        
        address = 0

        # For now, we've just hardcoded a program:
        
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  def ldi(reg, value):   address 0
        #     0b00000000, # sets register at                  address 1
        #     0b00001000, # sets the value
        #     0b01000111, # PRN R0 def prn(reg):
        #     0b00000000, # address of register which holds the value called
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_number = comment_split[0]
                    if possible_number == '':  # if line is empty
                        continue
                    first_bit = possible_number[0]  # check index for first number
                    if first_bit == '1' or first_bit == '0':  # does equal 1 or 0
                        instruction = int(possible_number[:8], 2)  #
                        self.ram[address] = instruction  #
                        address += 1  #

        except FileNotFoundError:
            print(f'Unable to find {sys.argv[1]}, please check the name and try again')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def ldi(self, address, value):
        self.reg[address] = value # sets the value to the register/address
        self.pc += 3 # because LDI takes operand a,b, and op we need to increment past used values in RAM
        
    def prn(self, address):
        print(self.reg[int(address)]) # prints the address
        self.pc += 2 # only takes in operand a and operation "op"
    
    def mul(self, rega, regb):
        sum = self.reg[rega] * self.reg[regb]
        self.reg[rega] = sum
        self.pc += 3
        
    def push(self, register):
        self.reg[SP] -= 1
        # 1. Decrement the `SP`.
        value = self.reg[register]
        self.ram_write(self.reg[SP], value)
        # 2. Copy the value in the given register to the address pointed to by `SP`.
        self.pc += 2
    
    def pop(self, register):
        value = self.ram_read(self.reg[SP])
        # 1. Copy the value from the address pointed to by `SP` to the given "PASTE" register.
        self.reg[register] = value # given register
        self.ram_write(self.reg[SP], 0) # sets the previous stack address to 0
        self.reg[SP] += 1
        # 2. Increment `SP`.
        self.pc += 2

    def run(self):
        """Run the CPU."""
        while self.running:
            op = self.ram_read(self.pc) # start at beginning of program index 0 also increment for every command in RAM
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            
            if op == LDI:
                self.ldi(operand_a, operand_b)
            elif op == PRN:
                self.prn(operand_a)
            elif op == MUL:
                self.mul(operand_a, operand_b)
            elif op == POP:
                self.pop(operand_a)
            elif op == PUSH:
                self.push(operand_a)
            elif op == HLT:
                running = False
