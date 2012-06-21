import pycurl
import time
import sys
import cStringIO

from xml.dom.minidom import parse, parseString


if len(sys.argv) < 2:
    print 'No action specified.'
    sys.exit()

if sys.argv[1].startswith('--'):
    help_text = '''\
        This program fetches all votes for cases from data.stortinget.no from a list of cases (the output from get_cases.py)
        run with: python get_vote.py cases-2010-2011.txt
    
        Input parameters:
        cases filname    :  cases-2010-2011.txt <- the output from get_cases.py
            
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

    filname = sys.argv[1] # cases-2010-2011.txt
    casefile = open(filname, 'r')

    cases = casefile.readlines()
    
    votefilename = "votes-" + filname[6:]
    # print votefilename
    # sys.exit(1)
    votefile = open(votefilename, 'w')

    for case_id in cases:
        buf = cStringIO.StringIO()

        c = pycurl.Curl()
        c.setopt(c.URL, 'http://data.stortinget.no/eksport/voteringer?sakid=' + case_id)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
     
        result = buf.getvalue()
        buf.close()

        dom3 = parseString(result)

        e = dom3.getElementsByTagName('alternativ_votering_id')

        if len(e) > 0:
            a = e[0].childNodes

            if len(a) > 0:
                alt_vote_id = a[0].data

                if int(alt_vote_id) > 0:
                    date = dom3.getElementsByTagName('votering_tid')[0].childNodes[0].data.split("T")[0]
                    print date + ":" + case_id.strip() + ":" + alt_vote_id + "\n"
                    #prints the date, the case_id and vote_id
                    votefile.write(date + ":" + case_id.strip() + ":" + alt_vote_id + "\n")
                    print "found votes!"
    print "written file named: %s " % (votefilename)
                
