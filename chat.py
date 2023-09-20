# from udp_bkst_query import *
import socket
import argparse
import numpy as np 
import threading
import queue


def get_port_from_usr():
	print("What port do u want")
	port = int(input())
	if(port > 100 and port < 2**16-1):
		return port
	else:
		print("out of range")


def get_host_ip_to_bind(port,use_loopback=False):
	if(use_loopback==True):
		return "127.0.0.1"
	if port > 100 and port < 2**16-1:
		print("port is: "+str(port))
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

def print_thread(kill_sig, soc):
	while(kill_sig.is_set()==False):	
		try:
			pkt,source_addr = server_socket.recvfrom(512)
			print("From: "+source_addr[0]+": "+str(pkt))
		except:
			pass
		


if __name__ == "__main__":
	port = get_port_from_usr()
	resp = input("Use loopback? y/n")
	myname = input("Who are you?")
	if(myname != ''):
		myname = myname + ": "
	if(resp=='y'):
		addr = get_host_ip_to_bind(port,use_loopback=True)
	else:
		addr = get_host_ip_to_bind(port)
	udp_server_addr = (addr, port)
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
	if(bkst_ip!='127.0.0.1'):
		bkst_ip = bkst_ip.split('.')
		bkst_ip[3] = '255'
		bkst_ip = '.'.join(bkst_ip)
		print("Using bkst ip: "+bkst_ip)
	dest_addr = (bkst_ip, port)
	sendstr = myname
	recvstr = ''

	ks = threading.Event()
	t0 = threading.Thread(target=blocking_input, args=(ks, client_socket,dest_addr,myname,))
	t1 = threading.Thread(target=print_thread, args=(ks, client_socket,))

	
	t0.start()
	t1.start()
	t0.join()
	t1.join()
	
	client_socket.close()