#!/usr/bin/python

import subprocess, os, sys, pty, select, signal
import getopt
from ConfigParser import ConfigParser

working_path = '/home/hath/'
config_path = 'hath_config.conf'
cmd = 'java -jar HentaiAtHome.jar --disable_logging -Djava.net.preferIPv4Stack=true'
verbose = False
user_id = ''
user_key = ''

def usage():
    print 'Usage: python <this file> -v <user_id> <user_key>'
    print 'example: python start_hath_pty.py -v 23412 kop034j23jio2393'
    print '    options:'
    print '        -v: verbose detail process message'

# load user id/user key, if need to login
def load_config(filepath):
    configParser = ConfigParser()
    configParser.read(filepath)
    user_id = configParser.get('HATH', 'client_ID', '')
    user_key = configParser.get('HATH', 'client_key', '')
    
    return (user_id, user_key)
    

try:
    opts, args = getopt.getopt(sys.argv[1:], 'v')
except:
    print 'no or wrong argument input'
    usage()
    sys.exit()
    
# handle opts
for o, a in opts:
    if o == '-v':
        verbose = True
    else:
        usage()
        sys.exit()
        
# handle args
if len(args) == 0:
    pass
elif len(args) == 2:
    user_id = args[0]
    user_key = args[1]
else:
    usage()
    sys.exit()

    
# ============= main script ================
os.chdir(working_path)

master_fd, slave_fd = pty.openpty()
cmd_obj = subprocess.Popen(cmd, stdout=slave_fd, stdin=slave_fd, shell=True, close_fds=True)

init_phase = True

with os.fdopen(master_fd, 'r+b', 0) as master_pty_fd:
    reads = [master_pty_fd]
    while True:
        read_fds = select.select(reads, [], [], 1)[0]
        if master_pty_fd in read_fds:
            ptydata = os.read(master_fd, 4096)
            if verbose:
                print ptydata
            elif '[WARN]' in ptydata or '[ERROR]' in ptydata:
                print ptydata
            
            if init_phase:
                if 'Enter Client ID:' in ptydata:
                    print 'found id input'
                    if not user_id:
                        user_id, user_key = load_config(config_path)
                    os.write(master_fd, user_id + '\n')
                    
                if '[WARN] Invalid Client ID.' in ptydata:
                    print 'client ID ERROR, exit...'
                    cmd_obj.terminate() # send ctrl+C
                    init_phase = False
                    
                if 'Enter Client Key:' in ptydata:
                    print 'found client key input'
                    if not user_key:
                        user_id, user_key = load_config(config_path)
                    os.write(master_fd, user_key + '\n')
                    
                if '[WARN] Invalid Client Key.' in ptydata:
                    print 'client Key ERROR, exit...'
                    cmd_obj.terminate() # send ctrl+C
                    init_phase = False
                    
                if 'Finished applying settings' in ptydata:
                    print 'init over, no longer check id/key'
                    init_phase = False
            
            if not ptydata: # EOF
                reads.remove(master_pty_fd)
                print 'EOF'
        if not read_fds: #timeout in select
            if cmd_obj.poll() is not None:
                os.close(slave_fd)
                break
