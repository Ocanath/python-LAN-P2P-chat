import socket
import argparse
import numpy as np 
import threading
import queue
from Getch import _Getch


if __name__ == "__main__":


    getch = _Getch()	
    while(1):
        ch = getch()
        byte_ch = bytes(ch,encoding='utf8')
        if(byte_ch == bytes([27])):
            print("Caught ESC, exiting")
            break
        print(byte_ch)		
