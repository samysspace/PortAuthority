from flask import Flask, render_template, request
import socket
import sys
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def form_data():
	ip_domain = request.form['firstname']
	port = request.form['lastname']
	if(port == ""):
		return """<p>Invalid port!</p>
				  <form action="/" method="get">
    		      <input type="submit" value="Try again!" />
			      </form>"""
	port_range = port.split("-")
	try:
		int(port[0])
		int(port[1])
	except Exception as e:
		print(e)
		return """<p>Invalid port!</p>
				  <form action="/" method="get">
    		      <input type="submit" value="Try again!" />
			      </form>"""
	timeout = 5
	lst = check(ip_domain, port_range, timeout)
	total = "The ports that are open for " + ip_domain + " are: "
	if len(lst) == 0:
		return """<p>No ports are open in this range.</p>
				  <form action="/" method="get">
    			  <input type="submit" value="Try again!" />
			      </form>"""
	for ports in range(len(lst)):
		if(ports == len(lst)-1):
			total += str(lst[ports])
		else:
			total += str(lst[ports])
	return """<p>{total_string}</p>
			<form action="/" method="get">
    		<input type="submit" value="Try again!" />
			</form>""".format(total_string=total)

def connect_to_ip(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock

    except Exception:
        return None


def scan_port(ip, port, timeout):
    socket.setdefaulttimeout(timeout)
    sock = connect_to_ip(ip, port)

    if sock:
        print('Able to connect to: {0}:{1}').format(ip, port)
        sock.close()
        return True
    else:
        print('Not able to connect to: {0}:{1}').format(ip, port)
        return False

def check(ip_domain, port_range, timeout):        
	# Get the IP address if the host name is a domain
	try:
		ip = socket.gethostbyname(ip_domain)
	except Exception as e:
		print(e)
		return []
	ports = []
	# If the user only entered one port we will only scan the one port
	# otherwise scan the range
	try: 
		if len(port_range) < 2:
			if(scan_port(ip, int(port_range[0]), int(timeout))):
				ports.append(port_range[0])
		else:
			for port in range(int(port_range[0]), int(port_range[1])+1):
				if(scan_port(ip, port, int(timeout))):
					ports.append(port)
	except Exception as e:
		print(e)
		return []
	print(ports)			
	return ports


if __name__ == "__main__":
    app.run()