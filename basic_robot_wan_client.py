import socket
import argparse
import numpy as np 
import threading
import queue
from Getch import _Getch


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Basic Robot Control Parser')
    parser.add_argument('--port', type=int, help="enter port", required=True)
    parser.add_argument('--ip', type=str, help="enter ip", required=True)
    args = parser.parse_args()


    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.settimeout(0.0)
    dest = (args.ip, args.port)
    getch = _Getch()	
    while(1):
        ch = getch()
        byte_ch = bytes(ch,encoding='utf8')
        if(byte_ch == bytes([27])):
            print("Caught ESC, exiting")
            break
        print(byte_ch)		
        soc.sendto(byte_ch,dest)
