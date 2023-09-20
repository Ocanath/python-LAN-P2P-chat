import socket

def get_hostip():
	hostname = socket.gethostname()
	# addr=socket.gethostbyname(hostname)
	hostname,aliaslist,addrlist=socket.gethostbyname_ex(hostname)
	if(len(addrlist)>1):
		print("Select an IP to use from list with a number (0,1,2,...)\r\n"+str(addrlist))
		usr_string_input = input()
		usr_input = int(usr_string_input)
		usr_input = max(0,min(usr_input,len(addrlist)-1))
		return addrlist[usr_input]
	else:
		return addrlist[0]


ip = get_hostip()
port = int(input("What port do you want: "))

server_addr = (ip,port)
print(server_addr)
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.settimeout(0.0)
soc.bind(server_addr)

strlist = [ "Hello? (Hello? Hello? Hello?)",
	"Is there anybody in there?",
	"Just nod if you can hear me",
	"Is there anyone home?",
	"Come on now",
	"I hear you're feeling down",
	"Well I can ease your pain",
	"Get you on your feet again",
	"Relax",
	"I'll need some information first",
	"Just the basic facts",
	"Can you show me where it hurts?",
	"There is no pain you are receding",
	"A distant ship smoke on the horizon",
	"You are only coming through in waves",
	"Your lips move but I can't hear what you're saying",
	"When I was a child I had a fever",
	"My hands felt just like two balloons",
	"Now I've got that feeling once again",
	"I can't explain you would not understand",
	"This is not how I am",
	"I have become comfortably numb",
	"I have become comfortably numb",
	"Okay (okay, okay, okay)",
	"Just a little pinprick",
	"There'll be no more, ah",
	"But you may feel a little sick",
	"Can you stand up?",
	"I do believe it's working, good",
	"That'll keep you going through the show",
	"Come on it's time to go",
	"There is no pain you are receding",
	"A distant ship, smoke on the horizon",
	"You are only coming through in waves",
	"Your lips move but I can't hear what you're saying",
	"When I was a child",
	"I caught a fleeting glimpse",
	"Out of the corner of my eye",
	"I turned to look but it was gone",
	"I cannot put my finger on it now",
	"The child is grown",
	"The dream is gone",
	"I have become comfortably numb"
	]
	
try:
	stridx = 0
	while(True):
		try:
			pkt,source_addr = soc.recvfrom(512)
			print("From: "+source_addr[0]+":"+str(source_addr[1])+": "+str(pkt))
			dest_addr = (source_addr[0], port)
			print("Sending to: "+dest_addr[0]+":"+str(dest_addr[1]))
			if(len(pkt)>0):
				sendstr = strlist[stridx]
				stridx = (stridx + 1) % len(strlist)
				soc.sendto(bytearray(sendstr,encoding='utf8'), dest_addr)
		except BlockingIOError:
			pass
except KeyboardInterrupt:	
	pass


soc.close()