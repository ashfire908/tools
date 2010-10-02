#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Remote wireshark script

# Import modules
import sys
import os
import subprocess
import optparse

# Define functions/classes
def argparser():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", action="store", type="string", dest="interface", help="Interface to listen on remote host")
    parser.add_option("-p", "--port", action="store", type="int", default=22, dest="port", help="Port to use to connect to remote host (default 22)")
    parser.add_option("-u", "--user", action="store", type="string", dest="user", help="User to login as on remote host")
    parser.add_option("-H", "--host", action="store", type="string", dest="host", help="The remote host to connect to")
    return parser

def main(options):
    host = options.host
    port = options.port
    user = options.user
    interface = options.interface
    if user == None:
        user = ""
    else:
        user = "%s@" % user
    tshark_command = ["tshark", "-n", "-w", "-", "not port %i and not host 127.0.0.1" % port]
    if interface != None:
        tshark_command.insert(1, "-i")
        tshark_command.insert(2, interface)
    remote_command = ["ssh", "-C", "-p", str(port), host, " ".join(tshark_command)]
    local_command = ["wireshark", "-i", "-", "-k"]
    # Start remote tshark
    remote_shark = subprocess.Popen(remote_command, stdout=subprocess.PIPE, stderr=sys.stderr)
    local_shark = subprocess.Popen(local_command, stdin=remote_shark.stdout, stdout=sys.stdout, stderr=sys.stderr)
    try:
        remote_shark.wait()
    except KeyboardInterrupt:
        try:
            remote_shark.terminate()
        except OSError:
            pass
    try:
        local_shark.wait()
    except KeyboardInterrupt:
        try:
            local_shark.terminate()
        except OSError:
            pass

# Run program
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    parser = argparser()
    (options, args) = parser.parse_args()
    main(options)
