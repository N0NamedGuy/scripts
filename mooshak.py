#!/usr/bin/env python2

import urllib
import urllib2
import httplib
import cookielib
import mimetypes
import mimetools
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
moo['problem'] = 'projecto3' 


### MULTIPART POSTING
def post_multipart(url, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    headers = {'Content-Type': content_type,
               'Content-Length': str(len(body))}
    r = urllib2.Request(url, body, headers)
    return urllib2.urlopen(r).read()

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

### END OF MULTIPART POSTING


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
        
    
    data = [
        ('command', 'analyze'),
        ('problem', moo['problem']),
        ('analyze', 'Submit')
    
    file_name = os.path.basename(file_path);
    
    f = open(file_path, 'b')
    file_data = f.read()
    f.close();

    files = [('program',file_name,file_data)]
    ret = post_multipart(moo['baseurl'] + '/cgi-bin/execute/' + moo['session'], data, files)

    print ret[1]


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



