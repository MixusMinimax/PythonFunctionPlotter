import threading

cmd = None

def thread_fun():
	while True:
		cmd = input()
		print(cmd)

x = threading.Thread(target=thread_fun)
x.start()