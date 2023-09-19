# from udp_bkst_query import *
import socket
import argparse
import cv2
import numpy as np 

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


if __name__ == "__main__":
	port = get_port_from_usr()
	resp = input("Use loopback? y/n")
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
	sendstr = ''
	recvstr = ''


	while(1):
	
	
		try:
			pkt,source_addr = server_socket.recvfrom(512)
			print("From: "+source_addr[0]+": "+str(pkt))
		except:
			pass
	
		
		image = 0
		cv2.imshow('Chat window', cv2.flip(image, 1))
		key = cv2.waitKey(1) & 0xFF
		if(key != 0 and key != 255):
			
			if(key == 27):	#escape
				break
			key = chr(key)
			# print(key,end='')
			if key != '\r' and key != '\n':	#enter
				sendstr = sendstr+key
				
			else:
				# print("Sending: "+sendstr)
				pld = bytearray(sendstr,encoding='utf8')
				client_socket.sendto(pld, dest_addr)
				# print('')
				sendstr = ''
				