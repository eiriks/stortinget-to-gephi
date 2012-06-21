#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl
import time
import os, sys

import cStringIO

from xml.dom.minidom import parse, parseString

if len(sys.argv) < 2:
    print 'No action specified.'
    sys.exit()

if sys.argv[1].startswith('--'):
    help_text = '''\
        This program fetches all votes for cases from data.stortinget.no from a list of cases (the output from get_cases.py)
        run with: python get_results.py votes-2010-2011.txt 
    
        Input parameters:
        cases filname    :  votes-2010-2011.txt  <- the output from get_votes.py
            
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
    votesfilname = sys.argv[1] # votes-2010-2011.txt
    
    votesfile = open(votesfilname, 'r')

    votes = votesfile.readlines()

    for vote in votes:
    	date = "-".join(vote.split(":")[0].split("-")[0:2])
    	vote_id = vote.split(":")[2]
        
        # I had com problems with the original way on the mac, so ried this
    	#try:
    	#    os.mkdir('votes/' + date.strip(), 0777)
    	#except:
    	#	None
        
        folder = 'votes/' + date.strip()
        
        # her finner den ikke alt, tror jeg... hvor er 2012-04 -jeg finner data derfra med "min" innsamler https://github.com/eiriks/stortinget-til-mysql
        print folder
        
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # create file with name from vote_id inside folder from date of voting
    	votefile = open('votes/' + date.strip() + '/' + vote_id.strip() + '.txt', 'w')
        
    	buf = cStringIO.StringIO()
        
    	c = pycurl.Curl()
    	c.setopt(c.URL, 'http://data.stortinget.no/eksport/voteringsresultat?VoteringId=' + vote_id)
    	c.setopt(c.WRITEFUNCTION, buf.write)
    	c.perform()
	 
    	result = buf.getvalue()
    	buf.close()
        
    	dom3 = parseString(result)
        
    	representatives = dom3.getElementsByTagName('representant_voteringsresultat')
        
        for repre in representatives:
            v = repre.getElementsByTagName('votering')[0].childNodes[0].data
                        
            if v != 'ikke_tilstede':
                rep = repre.getElementsByTagName('representant')[0]
                rep_id = ""
                party = ""
                
                for child in rep.childNodes:
                    if child.localName=='id':
                        rep_id = child.childNodes[0].data
                        
                    elif child.localName=='parti':
                        party = child.getElementsByTagName('id')[0].childNodes[0].data	
                        
                st = (party + ":" + rep_id + ":" + v).encode("utf-8")
                votefile.write(st  + "\n")
                print "written vote result from %s" % (rep_id)
        
        print "finnished for vote_id %s" % (vote_id)

    print "Done. you now have all the data from all the votes in you %s file" % (votesfilname)
