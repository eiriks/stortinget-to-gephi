import pycurl
import time
import sys

import cStringIO

from xml.dom.minidom import parse, parseString

buf = cStringIO.StringIO()


if len(sys.argv) < 2:
    print 'No action specified, try --help'
    sys.exit()

if sys.argv[1].startswith('--'):
    help_text = '''\
        This program fetches all cases from data.stortinget.no for a particular session
        run with: python get_cases.py 2010-2011
    
        Input parameters:
        session    :  2010-2011
            
        Options include:
        --version : Prints the version number
        --help    : Display this help
        --info    : author info
            
        '''
    
    option = sys.argv[1][2:]
	# fetch sys.argv[1] but without the first two characters
    if option == 'version':
        print 'Version 0.1'
    elif option == 'info':
        print 'Written by Petter Chr. Bjelland, tamperd with by Eirik Stavelin'
    elif option == 'help':
        print help_text
    else:
        print 'Unknown option.'
        print help_text
    sys.exit()
else:

    session = sys.argv[1] #"2010-2011"

    c = pycurl.Curl()
    c.setopt(c.URL, 'http://data.stortinget.no/eksport/saker?sesjonid=' + session)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    
    result = buf.getvalue()
    buf.close()
    #print result
    try:
        dom3 = parseString(result)
    except:
        print "didn't get the expected result from remote server at: http://data.stortinget.no/eksport/saker?sesjonid=%s" % (session)
        sys.exit(1)
    cases = dom3.getElementsByTagName('sak')

    casefile = open('cases-' + session + '.txt', 'w')

    for case in cases:
    	status = case.getElementsByTagName('status')[0]

    	if status.childNodes[0].data == "behandlet":
    		for child in case.childNodes:
    	 		if child.localName=='id':			
    				casefile.write(child.childNodes[0].data + "\n")
    print "written file named: cases-%s.txt " % (session)
		
