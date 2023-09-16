import time
import socket

def locate_server_from_bkst_query(port):
	hostname = socket.gethostname()
	# addr=socket.gethostbyname(hostname)
	hostname,aliaslist,addrlist=socket.gethostbyname_ex(hostname)
	usr_string_input = ''
	if(len(addrlist) > 1):
		print("Select an IP to use from list with a number (0,1,2,...)\r\n"+str(addrlist))
		usr_string_input = input()
	usr_input = int(usr_string_input)
	if(usr_input >= 0 and usr_input < len(addrlist)):
		addr=str(addrlist[usr_input])
		print("Host IP Addr: "+addr)
		addrmod = addr.split('.')
		addrmod[3] = '255'
		addrmod = '.'.join(addrmod)
		print("Using: "+addrmod+" on port: ",port)
		udp_server_addr = (addrmod, port)
		bufsize = 512
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.settimeout(0.0) #make non blocking

		start_time = time.time()

		try:
			barr = bytearray("marco",encoding='utf8')
			client_socket.sendto(barr,udp_server_addr)		
		except KeyboardInterrupt:
			print("some fkn error")

		found = 0
		while(time.time()-start_time < 3):
			try:
				pkt,addr = client_socket.recvfrom(bufsize)
				if(len(pkt) > 0):
					print("received response from: ",str(addr[0]))
					found = 1
					return str(addr[0])
			except:
				pass
		if(found == 0):
			return str(addrmod)
