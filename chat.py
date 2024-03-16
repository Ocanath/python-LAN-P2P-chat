# from udp_bkst_query import *
import socket
import argparse
# import numpy as np 
import threading
import queue
import serial
from serial.tools import list_ports


"""
	This function connects to every available serial port and returns the list 
	of connected ports
"""
def connect_to_all_serial_ports(baud):
	""" 
		Find a serial com port.
	"""
	print("Using baud",baud)
	com_ports_list = list(list_ports.comports())
	port = []
	slist = []
	for p in com_ports_list:
		if(p):
			pstr = ""
			pstr = p
			port.append(pstr)
			print("Found:", pstr)
	if not port:
		print("No port found")

	for p in port:
		try:
			ser = []
			ser = (serial.Serial(p[0], baud, timeout = 0, write_timeout = 0))
			slist.append(ser)
			print ("connected!", p)
		except:
			print("Attempt to connect to", p, "has failed.")
			pass
	print( "found ", len(slist), "ports.")
	return slist

def get_port_from_usr():
	print("What port do u want")
	port = int(input())
	if(port > 100 and port < 2**16-1):
		return port
	else:
		print("out of range")


def get_host_ip_to_bind(use_loopback=False):
	if(use_loopback==True):
		return "127.0.0.1"
	hostname = socket.gethostname()
	# addr=socket.gethostbyname(hostname)
	hostname,aliaslist,addrlist=socket.gethostbyname_ex(hostname)
	usr_string_input = ''
	usr_input = 0
	if(len(addrlist) > 1):
		print("Select an IP to use from list with a number (0,1,2,...)\r\n"+str(addrlist))
		usr_string_input = input()
		usr_input = int(usr_string_input)
	if(usr_input >= 0 and usr_input < len(addrlist)):
		addr=str(addrlist[usr_input])
		print("Host IP Addr: "+addr)
		return addr


def blocking_input(kill_sig, soc, dest, myname):
	while(kill_sig.is_set()==False):
		try:
			str = myname+input()
			pld = bytearray(str,encoding='utf8')
			soc.sendto(pld,dest)
		except EOFError:
			kill_sig.set()

def print_thread(kill_sig, soc, baud):
	slist = connect_to_all_serial_ports(baud)
	while(kill_sig.is_set()==False):	
		try:
			pkt,source_addr = server_socket.recvfrom(512)
			print("From: "+source_addr[0]+":"+str(source_addr[1])+": "+str(pkt))
			for s in slist:	#write serial
				s.write(pkt)
		except BlockingIOError:
			pass
		


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Chat Parser')
	parser.add_argument('--hardload_bind_ip', type=str, help="hard ip to bind", default='')
	parser.add_argument('--port', type=int, help="enter port for the server to bind to. By default, also the port we transmit to", default=0)
	parser.add_argument('--use_any',help="flag for using 0.0.0.0",action='store_true')
	parser.add_argument('--target-ip',help="IP and address of chat target. If system supports can be broadcast, or a WAN address",type=str)
	parser.add_argument('--target-port',help="Override of target port, in case we want to have a different bind port and target port",type=int)
	parser.add_argument('--chatname', help="Your name in the chat",type=str)
	parser.add_argument('--baud', help="baudrate override for serial chat message forwarding",type=int, default=230400)
	args = parser.parse_args()


	port = args.port
	if(port == 0):
		port = get_port_from_usr()
	myname = ''
	if(args.chatname is None):
		myname = input("Who are you?")
	else:
		myname = args.chatname
	if(myname != ''):
		myname = myname + ": "
	udp_server_addr = ()
	if(args.use_any == False):
		if(args.hardload_bind_ip == ''):
			addr = get_host_ip_to_bind(port)
			udp_server_addr = (addr, port)
		else:
			udp_server_addr = (args.hardload_bind_ip, port)
	else:
		udp_server_addr = ('0.0.0.0',port)
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.settimeout(0.0) #make non blocking
	try:
		print("binding: "+udp_server_addr[0]+", "+str(udp_server_addr[1]))
		server_socket.bind(udp_server_addr)
		print("Bind successful")
	except:
		print("something blocked us from binding to this ip")

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.settimeout(0.0)
	bkst_ip = udp_server_addr[0]
	bkst_port = port		
	if(bkst_ip!='127.0.0.1' and args.use_any == False):
		bkst_ip = bkst_ip.split('.')
		bkst_ip[3] = '255'
		bkst_ip = '.'.join(bkst_ip)
		print("Using bkst ip: "+bkst_ip)
	elif args.target_ip is None:
		bkst_ip = input("Enter target IP:")
	else:
		bkst_ip = args.target_ip
	if(args.target_port is not None):
		bkst_port = args.target_port
	dest_addr = (bkst_ip, bkst_port)
	print("Targeting", dest_addr[0], ":", dest_addr[1])
	sendstr = myname
	recvstr = ''

	ks = threading.Event()
	t0 = threading.Thread(target=blocking_input, args=(ks, server_socket,dest_addr,myname,))
	t1 = threading.Thread(target=print_thread, args=(ks, server_socket, args.baud))

	
	t0.start()
	t1.start()
	t0.join()
	t1.join()
	
	client_socket.close()