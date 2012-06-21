import dircache
import sys
from calendar import monthrange

# colors from: http://stavelin.com/blog/2012/06/18/var-partifarger-krangle-kan-vi-gjore-siden/

def hex_to_rgba(value):
    value = value.lstrip('#')
    if len(value) == 3:
        value = value*2
    return tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))+(1,)


partifarger = {}
partifarger['A'] = '#da383f';       #'#fd0000' fra logo
partifarger['ALP'] = '#f6f6f6';     # finnes ikke lenher
partifarger['B'] = '#008140';       # samme som Sp
partifarger['DNF'] = '#f6f6f6';     # finnes ikke lenger. Det Nye Folkepartiet het ogsa det liberale forlepartiet og nye venste.
partifarger['FFF'] = '#f6f6f6';     # finnes ikke lenger
partifarger['FrP'] = '#393d87';
partifarger['H'] = '#0f658d';
partifarger['Kp'] = '#286d6d';      #'#f6f6f6' // finnes ikke lenger, stilte dog til valg i 2011 ...
partifarger['KrF'] = '#efae52';
partifarger['NKP'] = '#e40202';     # fra logo
partifarger['RV'] = '#a61e20';
partifarger['SF'] = '#f6f6f6';      # finnes ikke lenger
partifarger['Sp'] = '#008767';      #'#008140'
partifarger['SV'] = '#bb234a';      #'#cf0036'
partifarger['SVf'] = '#f6f6f6';     # finnes ikke lenger
partifarger['TF'] = '#f6f6f6';      # finnes ikke lenger
partifarger['Uav'] = '#f6f6f6';     # finnes ikke lenger
partifarger['V'] = '#81b45f';       #'#006c6e' # de under her hadde NRK med i 2011-valget, selv om de ikke kom inn
partifarger['DEMN'] = '#003366';    # demokratene er ikke inne
partifarger['PP'] = '#000000';      # pensjonistpartiet er ikke inne
partifarger['MDG'] = '#3b7346';     # miljopartiet de gronne er ikke inne
partifarger['R'] = '#7c2629';       # rodt er ikke inne

if len(sys.argv) < 2:
    print 'No action specified.'
    sys.exit()

if sys.argv[1].startswith('--'):
    help_text = '''\
        This program creates gephi files from  data youve prepared with get_results.py
        see http://gephi.org/ for .gexf file reader.
        
        run with: python make_gexf.py 2012-03 2012-05 2012-12
    
        Input parameters:
        session    :  2012-03 <- list of year-months you want to use, and have created with get_results.py
            
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
    # let's go!
    files = []
    
    good_months = sys.argv[1:]

    l = dircache.listdir('votes')
    
    for a in l:
        #if a == '2011-11' or a == '2011-12':
    	if a in good_months:
    		k = dircache.listdir('votes/' + a)

    		for t in k:
    			files.append(a + "/" + t)


    outfilename =  '_'.join(good_months)
    outfilepath = 'gexf/%s.gexf' % (outfilename)
    gexf = open(outfilepath, 'w')
    
    gexf.write('<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.1draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">')
    gexf.write('<meta lastmodifieddate="2009-03-20">')
    gexf.write('<creator>Gexf.net</creator>')
    gexf.write('<description>A hello world! file</description>')
    gexf.write('</meta>')
    #gexf.write('<graph mode="dynamic" defaultedgetype="undirected" start="2011-11-01" end="2013-05-12" timeformat="date">')
    gexf.write('<graph mode="dynamic" defaultedgetype="undirected" start="2011-01-01" end="2013-05-12" timeformat="date">')
    gexf.write('<nodes>')
    for f in files:
        votefile = open('votes/' + f, 'r')
        votes = votefile.readlines()
        # create nodes aka persons, with party as label
        for vote in votes:
            data = vote.strip().split(":")
            #print data
            gexf.write('<node id="' + data[1] + '" label="' + data[0] + '">')
            
            # if this fails, there is no backup (gray could be good for that..)
            color = hex_to_rgba(partifarger[data[0]])            
            viz_color_node = '<viz:color r="%s" g="%s" b="%s"/>' % (color[0],color[1],color[2])
            gexf.write(viz_color_node)
            
            # if data[0] == "A":
            #     gexf.write('<viz:color r="223" g="26" b="34"/>')
            # elif data[0] == "H":
            #     gexf.write('<viz:color r="0" g="0" b="255"/>')
            # elif data[0] == "FrP":
            #     gexf.write('<viz:color r="0" g="0" b="178"/>')
            # elif data[0] == "V":
            #     gexf.write('<viz:color r="4" g="123" b="117"/>')
            # elif data[0] == "KrF":
            #     gexf.write('<viz:color r="250" g="218" b="55"/>')
            # elif data[0] == "Sp":
            #     gexf.write('<viz:color r="0" g="157" b="88"/>')
            # elif data[0] == "SV":
            #     gexf.write('<viz:color r="203" g="45" b="80"/>')
                
            gexf.write('</node>')

    gexf.write('</nodes>')
    gexf.write('<edges>')

    score = {}

    for f in files: 
        votefile = open('votes/' + f, 'r')
        votes = votefile.readlines()
        
        for vote in votes:
            data = vote.strip().split(":")
            #print data                 # ['SV', 'HEIS', 'mot'
            value = data[2]             # f.eks. mot  - brukes ikke til noe?
            
            # if his' not in score, add him as an empty unit
            if data[1] not in score:
                score[data[1]] = []                     # create key for MP
                score[data[1]].append(0)                # totalt number of votes he have done
                score[data[1]].append({})               # ampty dict
                score[data[1]].append(f.split("/")[0])  # add the date for this first vote session (why?)
            
            score[data[1]][0] += 1                      # add one to the amounts of times voted
            #print score
            
            for other_vote in votes:
    			other_data = other_vote.strip().split(":")

    			if other_data[1] != data[1] and other_data[2] == data[2]:       # if other MP is not this MP and other vote falvour in not the same as this MPs vote.
    				if other_data[1] not in score[data[1]][1]:                  # this the other dude isn't recored in this MPs list of other votes:
    					score[data[1]][1][other_data[1]] = 0                    # add him and set his value to 0
				
    				score[data[1]][1][other_data[1]] += 1                       # then: add the others dudes voting +1 (this counts the number of times the disagree... )

    				#gexf.write('<edge id="' + other_data[1] + '_' + data[1] + '" source="' + other_data[1] + '" target="' + data[1] + '" />')
    
    
    # stricture of score: {ID_OF_MP: [total number of votes, {list of other MP voting the same}, 'date of first vote']}
    # so the score for the first MP is: score['PTA'] = [5, {'LIC': 5, 'WO': 5, 'AGES': 1, etc ...}, '2012-03']
	
    s = 0
    for r in score:
    	data = score[r]

    	total = data[0]         # total number of times voted
        
        # ======================================================================
        # = I ran into problems here. messing with end-dates seemed to work... =
        # ======================================================================
    	fr = data[2] + "-01T00:00:00.000"
    	#to = data[2] + "-31T00:00:00.000"    
        # to = 2011-02 + '-' + number of max days in this month +  "T00:00:00.000"        
        to = data[2] +'-'+ str(monthrange(int(data[2].split('-')[0]), int(data[2].split('-')[1]))[1]) + "T00:00:00.000"
        #print to

        # for other dudes in this MP list comparable MPs
    	for other in data[1]:
            #print float(data[1][other]), float(total), total        # number of times other dude voted the same / total numbers of times voted >= is more than 0.5
            # if     #ant-like-stemmer/(ant-like-stemmer+ant-ulike-stemmer)>0.5 
            if float(data[1][other]) / float(total) >= float(1)/float(2):
                # what's wrong here..
                # if r == 'LAT':
                #     print '<edge id="' + r + '_' + other + '" source="' + r + '" target="' + other + '" start="' + fr + '" end="' + to + '" />'
                gexf.write('<edge id="' + r + '_' + other + '" source="' + r + '" target="' + other + '" start="' + fr + '" end="' + to + '" />')
                s += 1
    #print s
    gexf.write('</edges>')
    gexf.write('</graph>')
    gexf.write('</gexf>')

    gexf.close()
    print "Gephi file written, check in folder: %s " % (outfilepath)