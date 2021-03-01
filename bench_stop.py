# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re, os
# import frappe, requests

# def check_site_state():
# 	session = create_log_session()
# 	url = "http://localhost:84/api/method/custom_clearance.custom_clearance.doctype.live_site.live_site.site_state"
# 	headers = {'content-type': 'application/x-www-form-urlencoded' }
# 	data = {
# 		'domain': 'localhost',
# 		'port': '1000'
# 	}
	
# 	state_dict = {
# 		"Active": 1,
# 		"Stop": 0,
# 		"hold": 0
# 	}

# 	status_flag = 0

# 	try:
# 		response = session.get(url, data=data, headers=headers)
# 		_result = response.json()
# 		print (str(_result))
# 		if 'message' in _result:
# 			status = _result.get('message')
# 			if status: status_flag = state_dict.get(status[0]['status'])
# 		else:
# 			print ('Failed') 
	
# 	except Exception as e:
# 		print (str(e))
# 		raise
	
# 	return status_flag


# def create_log_session():
# 	session = requests.Session()
# 	session.post("http://localhost:84/api/method/login",
# 		data={ "usr": "administrator",
# 			"pwd": "qwedsa@123" }
# 	)
# 	# Login
# 	return session

def nginx_state(alive = 0):
	comment_flag = 0
	uncomment_flag = 0

	try:
		with open("./config/nginx.conf", "rw+") as config_file:
			f_content = config_file.readlines()
			for idx, line in enumerate(f_content):
				listen_string = line.strip().find('listen')

				key, value = re.sub(r'([\t]+|[\n])', '', line, flags=re.M).partition(" ")[::2]
				
				if listen_string <> -1:
					if key.strip() == "listen" and int(value.strip().replace(";", "")) == 1000:
						uncomment_flag = 2

						if alive == 0:
							comment_flag = 1
							f_content[idx] = "# " + line
					
					elif key.strip() == "#":
						key, value = value.partition(" ")[::2]
						if key.strip() == "listen" and int(value.strip().replace(";", "")) == 1000:
							comment_flag = 2
							
							if alive == 1:
								uncomment_flag = 1
								f_content[idx] = line.replace("# ", "")
			
			config_file.seek(0)
			config_file.truncate()
			config_file.write(''.join(f_content))
		
		config_file.close()
	except IOError:
		print ('The file nginx.conf was not found. Are you sure you custom_stop.py is in bench directory?')
	finally:
		os.system("sudo service nginx restart")

	if alive:
		if uncomment_flag == 1:
			print ("Site STARTED")
		elif uncomment_flag == 2:
			print ("Site Already STARTED")
		else:
			print ("failed to START")
	else:
		if comment_flag == 1:
			print ("Site STOPPED")
		elif comment_flag == 2:
			print ("Site Already DOWN")
		else:
			print ("failed to STOP")


def move_to_bench():
	d = os.getcwd()
	i = 0
	while(not os.path.basename(d) == "frappe-bench"):
		os.chdir("..")
		d = os.getcwd()
		i += 1
		if i == 10: break


def bench_stop_launch():
	# move_to_bench()
	os.chdir("frappe-bench")
	# nginx_state(check_site_state())
	nginx_state(1)

if __name__ == '__main__':
	bench_stop_launch()