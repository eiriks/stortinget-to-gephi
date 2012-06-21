stortinget-to-gephi
===================

code to grenerate gephi xml from stortinget voting data

- written by Petter Christian Bjelland
- altered by Eirik Stavelin


#Info
Dette programmet lag deg lage gephi-filer med stortingsrepresentanter og relasjoner mellom dem etter hvor ofte de stemmer likt i avstemninger på tinget.
Se denne posten for eksempler: http://pcbje.com/post/22899427417/visualization-of-votes-in-the-norwegian-parliament

Denne filen forklarer hvordan du kan bruke dette programmet, og lage slike selv.

#Innstrukjsoner

Først trenger du å hente ned saker. Dette gjøres pr stortingssesjon med scriptet get_cases.py

	python get_cases.py 2010-2011

Resultatet er en fil med en lang lister over saksIDer. Ikke alle har vært stemt over, så trenger vi å hente ut voterings_IDer for de som har:

	python get_vote.py cases-2010-2011.txt

dette skriver til en fil i formatet: dato:saks_id:voteringsid
eks:
	2012-06-14:50867:2634

Denne listen er betrakelig kortere enn den forrige, og inneholder kun de sakene som det finnes stemme-data om.

Videre må vi finne ut hvem som stemte hva i de ulike sakene:

	python get_results.py votes-2010-2011.txt 

dette lager foldere etter hvilken måned pr år saken ble stemt på, med voterings_id som filnavn.

Så må vil lage gephifiler:

	 python make_gexf.py 2011-11 2011-12 2012-01 
	 
du lister ut så mange måneder som du selv vil. Dette lager en .gexf-fil. Denne kan du åpne i gephi, se gephi.org for leser.	





#Instructions
Instruktions for this code is in Norwegian only. Sorry.
http://translate.google.com/
.. the code is written and documented in English though.

 
