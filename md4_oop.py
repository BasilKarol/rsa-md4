import struct

class MD4:
    def __init__(self, x):
        if not isinstance(x, bytes):
            raise TypeError(f"Expected <class 'bytes'>, but {type(x)} were given.\nTry to use .from_string(x) or .from_file(x) instead!")
        self.input_text = x    ##.encode()
        self.block_list = self.bit_blocks()
        self.ABCD_list = [1732584193, 4023233417, 2562383102, 271733878] 
        self.ABCD_old = self.ABCD_list.copy()
        self.output_hash = self.get_hash()

    @classmethod
    def from_string(cls, x):
        if not isinstance(x, str):
            raise TypeError(f"Expected <class 'str'>, but {type(x)} were given.")
        x = x.encode('utf-8')
        return cls(x)

    @classmethod
    def from_file(cls, x):
        if not isinstance(x, str):
            raise TypeError(f"Expected <class 'str'>, but {type(x)} were given.")
        with open(x, 'rb') as file:
            x = file.read()
        return cls(x)

    def __str__(self):
        return hex(self.output_hash)[2:] 
    def __eq__(self, hash_2):
        return hex(self.output_hash)[2:] == hash_2
    
    def bit_blocks(self):
        text = self.input_text
        n = len(text) *8  ## do bitów
        
        text += b"\x80" 
        text += b"\x00" * (64- ( len(text)+len(b"\x80")*8 )% 64 )
        text += struct.pack("<Q", n)

        block_list = [text[i : i + 64] for i in range(0, len(text), 64)]  ## 1 bajt == 8 bitów !!
        unpacked_blocks = [ struct.unpack("<16I", block) for block in block_list ]
        return unpacked_blocks
    
    def get_hash(self):
        ## Runda 1
        z_1_list = list( range(16) )
        w_1_list = [3, 7, 11, 19]*4

        for unpacked_block in self.block_list: 
            for z, w in zip(z_1_list, w_1_list):
                A_prim = self.ABCD_list[3]
                new_X = self.ABCD_list[0] + self.F( self.ABCD_list[1], self.ABCD_list[2], self.ABCD_list[3] ) + unpacked_block[z] 
                B_prim = self.rotate_left( new_X & 0xFFFFFFFF, w )

                C_prim = self.ABCD_list[1]
                D_prim = self.ABCD_list[2]
                self.ABCD_list = [A_prim, B_prim, C_prim, D_prim]
        
        ## Runda 2
        y_2 = 1518500249
        z_2_list = [ i for i_start in range(4) for i in range(i_start, 16, 4) ]
        w_2_list = [3, 5, 9, 13]*4

        for unpacked_block in self.block_list: 
            for z, w in zip(z_2_list, w_2_list):
                A_prim = self.ABCD_list[3]
                new_X = self.ABCD_list[0] + self.G( self.ABCD_list[1], self.ABCD_list[2], self.ABCD_list[3] ) + unpacked_block[z] + y_2
                B_prim = self.rotate_left( new_X & 0xFFFFFFFF, w )
                C_prim = self.ABCD_list[1]
                D_prim = self.ABCD_list[2]
                self.ABCD_list = [A_prim, B_prim, C_prim, D_prim]

        ## Runda 3
        y_3 = 1859775393
        z_3_list = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        w_3_list = [3, 9, 11, 15]*4

        for unpacked_block in self.block_list: 
            for z, w in zip(z_3_list, w_3_list):
                A_prim = self.ABCD_list[3]
                new_X = self.ABCD_list[0] + self.H( self.ABCD_list[1], self.ABCD_list[2], self.ABCD_list[3] ) + unpacked_block[z] + y_3
                B_prim = self.rotate_left( new_X & 0xFFFFFFFF, w )
                C_prim = self.ABCD_list[1]
                D_prim = self.ABCD_list[2]
                self.ABCD_list = [A_prim, B_prim, C_prim, D_prim]
        ABCD_out = [ (x_list + x_old) & 0xFFFFFFFF for x_list, x_old in zip(self.ABCD_list, self.ABCD_old) ]

        hash = struct.pack("<4L", *ABCD_out) 
        hash = int.from_bytes(hash, 'big')
        return hash
    

    @staticmethod
    def F(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def G(x, y, z):
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def rotate_left(value, shift):  ## https://nickthecrypt.medium.com/cryptography-hash-method-md4-message-digest-4-explained-with-python-f201b74f51d
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

if __name__ == "__main__":
    test_all = True
    ala_hash = "e1fefa8fb989926d1322695a4ae34503"
    if test_all:
        test_bytes = b"Ala ma kota"
        encoded_str = MD4(test_bytes)
        print(encoded_str == ala_hash) #, int(encoded_str.__str__(), 16))
    
        test_str = "Ala ma kota"
        encoded_str = MD4.from_string(test_str)
        #print(encoded_str, encoded_str.output_hash)
        print(encoded_str == ala_hash)
    
        test_plik = "test_text"
        encoded_str = MD4.from_file(test_plik)
        print(encoded_str == ala_hash)

