#!/usr/bin/python

import os
import sys

#NOTE: I'm so sorry for this.
try:
	# if this file deos not exist, then we will jump to the exception and use
	# the local PLCSH without passing any additional arguments.

	os.stat("/etc/planetlab/master.py")
	sys.path.append("/etc/planetlab")
	import master

	# Use the values given to us in the /etc/planetlab/master.py file taken from
	# the master PLC and use them to construct the proper arguments to plcsh so
	# that we can get a user list from managing, CoPLC

	user=master.PLC_ROOT_USER
	passwd=master.PLC_ROOT_PASSWORD
	url = "https://" + master.PLC_API_HOST + ":" \
			+ master.PLC_API_PORT + master.PLC_API_PATH

	cmd = "plcsh --user=%s --password=%s --url=%s %s" % (user, 
			passwd, url, " ".join(sys.argv[1:]))
except:
	cmd = "plcsh %s" % " ".join(sys.argv[1:])

os.system(cmd)
