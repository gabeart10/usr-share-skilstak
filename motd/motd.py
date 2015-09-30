#!/usr/bin/env python3

import colors as c
import os
import pwd

euid =  os.geteuid()
name =  pwd.getpwuid(euid)[4].split(',')[0]
groups = os.getgroups()
#isuser = os.popen('/usr/local/bin/name ' + name).read() 
#bux = os.popen('/usr/share/skilstak/bin/bux').read() 

#if not isuser: exit()

print(c.yellow + "Welcome back " + name + ". Good to see you." + c.reset)
#print(c.red + "Fall registration and payment due before August 1st" + c.reset)
#if 9000 in groups:
#    print(c.yellow + "I see you are enrolled as a student." + c.reset)
#print(bux, end='')
#else:
#    print(c.red + 'Looks like you are no longer enrolled, your login is limited.' + c.reset)
#    print(c.red + 'You are free to code and talk and behave but not keep anything running.' + c.reset)
#    print(c.red + 'Attempts to start your Minecraft, Web, or other server are logged.' + c.reset)
#    print(c.red + 'Repeated attempts will lock your login out.' + c.reset)
