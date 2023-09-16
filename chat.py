from udp_bkst_query import *

def get_port_from_usr():
	print("What port do u want")
	port = int(input())
	if(port > 100 and port < 2**16-1):
		return port
	else:
		print("out of range")


def get_host_ip_to_bind(port, use_loopback=False):
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
	addr = get_host_ip_to_bind(port)
	udp_server_addr = (addr, port)
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.settimeout(0.0) #make non blocking
	try:
		server_socket.bind(udp_server_addr)
		print("Bind successful")
	except:
		print("something blocked us from binding to this ip")
	
	