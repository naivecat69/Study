class ITA2Decoder:
    def __init__(self, test_list):
        self.ITA2_table = {
        0b00000: '*NULL*',       # Null
        0b00001: 'E',
        0b00010: '*LF*',        # Line Feed
        0b00011: 'A',
        0b00100: ' ',         # Space
        0b00101: 'S',
        0b00110: 'I',
        0b00111: 'U',
        0b01000: '*CR*',        # Carriage Return
        0b01001: 'D',
        0b01010: 'R',
        0b01011: 'J',
        0b01100: 'N',
        0b01101: 'F',
        0b01110: 'C',
        0b01111: 'K',
        0b10000: 'T',
        0b10001: 'Z',
        0b10010: 'L',
        0b10011: 'W',
        0b10100: 'H',
        0b10101: 'Y',
        0b10110: 'P',
        0b10111: 'Q',
        0b11000: 'O',
        0b11001: 'B',
        0b11010: 'G',
        0b11011: '*FIGS*',      # Shift to FIGURES
        0b11100: 'M',
        0b11101: 'X',
        0b11110: 'V',
        0b11111: '*LTRS*'       # Shift to LETTERS
}
        self.test_list = test_list
        self.decoded_str = ''

    def reverse_bits(self, width=5):
        for i in range(len(self.test_list)):
            bit = self.test_list[i]
            rbit = 0 # reversed bit
            for _ in range(width):
                rbit = (rbit << 1) | (bit & 1)
                bit >>= 1
            self.test_list[i] = rbit

    def rotate_bits(self, r = 0):
        if type(r) != int:
            raise TypeError('rotate bit must be an integer')
        elif not 0 <= r <= 32:
            print('warning: parameter error')

        for i in range(len(self.test_list)):
            bit = self.test_list[i]
            bit = (bit + r) % 0b100000
            print(bin(bit))
            self.test_list[i] = bit

        print(self.test_list) # for debugging line

    def run(self, reverse_mode = False, rotate_mode = 0) -> str:
        # bitwise operation line start
        if reverse_mode: self.reverse_bits()
        if rotate_mode: self.rotate_bits(rotate_mode)
        # bitwise operation line end

        # from binaray to ITA2
        for bit in self.test_list:
            self.decoded_str += self.ITA2_table[bit]

        return self.decoded_str

if __name__ == '__main__':
    test_list = [0b00110, 0b00100, 0b00100, 0b00100]
    result = ITA2Decoder(test_list).run(False, 3)
    print(result)