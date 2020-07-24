import time

print ("The result from time.time() is: ", time.time())
print ("The result from time.localtime(time.time()) is: ", time.localtime(time.time()))
print ("The result from time.gmtime(time.time()) is: ", time.gmtime(time.time()))