#!/usr/bin/env python2

import urllib
import urllib2
import httplib
import cookielib
import os
import sys

moo = {}
moo['cookiefile'] = '.mooshak.lwp'
moo['cookiejar'] = cookielib.LWPCookieJar()
moo['baseurl'] = 'http://di90.di.fct.unl.pt/~mooshak'

moo['session'] = None
moo['sessionfile'] = '.mooshak.sess'

# Auth
moo['contest'] = 'ada2011-t3'
moo['user'] = None
moo['password'] = None


def save_session():
    moo['cookiejar'].save(moo['cookiefile'], True, True)

def get_session():
    sf = moo['sessionfile']
    if os.path.isfile(sf):
        f = open(sf)
        sess = f.read()
        f.close()
        return sess

    return None

# Starts a saved session
def resume_session():
    cj = moo['cookiejar']
    cf = moo['cookiefile']
    sf = moo['sessionfile']

    if os.path.isfile(cf):
        cj.load(cf)
    
    moo['session'] = get_session()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

# Gets a new session number
def new_session():
    req = urllib2.Request(moo['baseurl'] + '/cgi-bin/execute')
    handle = urllib2.urlopen(req)
    url = handle.geturl()
    sess = url.split('/')[-1]

    sf = moo['sessionfile']
    f = open(sf, 'w')
    f.write(sess)
    f.close()

    moo['session'] = sess
    resume_session()

# Logs out from mooshak
def do_logout():
    resume_session()

    if moo['session'] == None:
        print 'You\'re not logged in'
        return
   
    # won't alert mooshak because it hangs...
    
    cf = moo['cookiefile']
    if os.path.isfile(cf):
        os.unlink(cf)

    sf = moo['sessionfile']
    if os.path.isfile(sf):
        os.unlink(sf)

# TODO: check wrong pw
def do_login():
    moo['session'] = get_session()
    if moo['session'] == None:
        new_session()
    else:
        print 'Please log out first'
        return

    # Do the actual login
    data_dict = {}
    data_dict['command'] = 'login'
    data_dict['arguments'] = ''
    data_dict['contest'] = moo['contest']
    data_dict['user'] = moo['user']
    data_dict['password'] = moo['password']

    req = urllib2.Request(moo['baseurl'] + '/cgi-bin/execute/' +
        moo['session'], urllib.urlencode(data_dict))
    handle = urllib2.urlopen(req) 
    print handle.read()

    save_session()

def do_submit(file_path):
    moo['session'] = get_session()
    if moo['session'] == None:
        print 'Please login first'
        return

    print 'Submit stuff!'



cmd = sys.argv[1]
if len(sys.argv) > 2:
    args = sys.argv[2:]
else:
    args = None


if cmd == 'login':
    do_login()    
elif cmd == 'logout':
    do_logout()
elif cmd == 'submit':
    do_submit(args[0])

# Save session



