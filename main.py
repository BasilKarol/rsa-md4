#!/bin/env python
import sys
from md4_oop import MD4

if __name__ == '__main__':
        md4_args = sys.argv[1:] 
        if len(md4_args) == 1:
            encoded_str = MD4( md4_args[0] )
        elif len(md4_args) == 2:
            if md4_args[1] == 'file':
                encoded_str = MD4.from_file(md4_args[0])    
            elif md4_args[1] == 'str':
                encoded_str = MD4.from_string(md4_args[0])    
        print(encoded_str )
            
        