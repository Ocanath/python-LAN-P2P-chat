# from udp_bkst_query import *
import socket
import argparse
import threading
from datetime import datetime
import time

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

def print_thread(kill_sig, do_ttracker, soc):
	last_time = time.time()
	is_in_office = 0
	elapsed_sec = 0
	while(kill_sig.is_set()==False):	
		cur_epoch_time = time.time()	#epoch
		elapsed_sec = cur_epoch_time - last_time
		try:
			pkt,source_addr = server_socket.recvfrom(512)
			if(do_ttracker == True):
				if(pkt != bytearray("WAZZAP BIATCHS ITS YA BOY JESSE", encoding='utf8')):
					print("From: "+source_addr[0]+":"+str(source_addr[1])+": "+str(pkt))
				else:			#we received the special message corresponding to me being here
					last_time = cur_epoch_time			
			else:
				print("From: "+source_addr[0]+":"+str(source_addr[1])+": "+str(pkt))
		except BlockingIOError:
			pass
		if(do_ttracker == True):
			curtime = datetime.now()
			if(elapsed_sec > 600 and is_in_office != 0):
				print("Left at: "+curtime.strftime("%m/%d/%Y %H:%M:%S"))
				is_in_office = 0
			elif(elapsed_sec <= 600):	
				if( is_in_office == 0):
					print("Arrived at: "+curtime.strftime("%m/%d/%Y %H:%M:%S"))
					is_in_office = 1
			if(elapsed_sec > 1200 and is_in_office == 0):
				pass	#TODO: consider jesse gone for the day, and write the log exit time to the log file

		


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Chat Parser')
	parser.add_argument('--hardload_bind_ip', type=str, help="hard ip to bind", default='')
	parser.add_argument('--port', type=int, help="enter port", default=0)
	parser.add_argument('--use_any',help="flag for using 0.0.0.0",action='store_true')
	parser.add_argument("--target_ip", type=str, help="cmd line argument for ip to send messages to", default='')
	parser.add_argument("--no_name", action='store_true')
	parser.add_argument("--do_ttracking", action='store_true')
	args = parser.parse_args()

	port = args.port
	if(port == 0):
		port = get_port_from_usr()
	myname = ''
	if(args.no_name == False):
		myname = input("Who are you?")
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
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server_socket.settimeout(0.0) #make non blocking
	try:
		print("binding: "+udp_server_addr[0]+", "+str(udp_server_addr[1]))
		server_socket.bind(udp_server_addr)
		print("Bind successful")
	except:
		print("something blocked us from binding to this ip")

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client_socket.settimeout(0.0)
	bkst_ip = udp_server_addr[0]
	if(bkst_ip!='127.0.0.1' and args.use_any == False):
		bkst_ip = bkst_ip.split('.')
		bkst_ip[3] = '255'
		bkst_ip = '.'.join(bkst_ip)
		print("Using bkst ip: "+bkst_ip)
	elif (args.target_ip != ''):
		bkst_ip = args.target_ip
	else:
		bkst_ip = input("Enter target IP:")
	dest_addr = (bkst_ip, port)
	sendstr = myname
	recvstr = ''

	ks = threading.Event()
	t0 = threading.Thread(target=blocking_input, args=(ks, server_socket,dest_addr,myname,))
	t1 = threading.Thread(target=print_thread, args=(ks, args.do_ttracking, server_socket,))

	
	t0.start()
	t1.start()
	t0.join()
	t1.join()
	
	client_socket.close()