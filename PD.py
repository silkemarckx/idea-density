import nltk
from nltk import word_tokenize, pos_tag

def IdeaDensity(inputtext, rnge=0):
	#1. tokenization & part-of-speech tagging
	f = open(inputtext,'rt', encoding='utf-8') #http://www.americanrhetoric.com/speeches/barackobama/barackobamawhitehousecorrespondentsdinner2016.htm
	text=f.read()
	f.close()

	tokenized= word_tokenize(text)
	taggedtext = pos_tag(tokenized)
	Originaltext = pos_tag(tokenized)
	#print('Tagged text: Original',taggedtext)


	#2. Total word count
	#Deleting punctuation
	#Problem: Only removes all punctuation after a second identical loop. 
	#=> OVERALL PROBLEM: 2 items with same tag: No removal of second item!!
	Punctuation = (',','.','!',';','?',':',"'","''",'``','(',')')
	for word in taggedtext:
		if word[1] in Punctuation:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext:
		if word[1] in Punctuation:
			taggedtext.remove(word)
		else:
			continue

	wordcount = len(taggedtext)
	#print('wordcount: ',wordcount)

	if wordcount > 10000:
		rnge +=184
	elif wordcount > 2000:
		rnge +=40
	elif wordcount >1000:
		rnge+=4

	#3. Proposition count & Adjustment Rules
	"""= verbs
	+adjectives
	+adverbs
	+prepositions
	+conjunctions
	+determiners (-a,an,the)
	+modals (ONLY if negative)
	-auxiliary verbs
	-linking verbs """

	#Adjustment rules:
	""" 'either...or' = 1 prop.
	'to'+verb = 1 prop
	'a,an,the' =/ prop
	models =/ prop, UNLESS negative (ending in "n't")
	COPULA + NP ==> copula = prop 
	COPULA + AdjP ==> copula(linking verb) =/ prop  (AdjP=prop!)"""
	propcount= len(taggedtext)

	#Removing positive modals from prop count.
	#For negative modals: Modal is removed, negative part carries prop count & is not removed(otherwise: double count)
	#Modal 'Have to' is removed in a later stage, when removing 'have' as a auxiliary verb
	Modals = (('can', 'MD'),('Can', 'MD'),('could', 'MD'),('Could', 'MD'),('will', 'MD'),
		('Will', 'MD'),("'ll", 'MD'),('wo', 'MD'),('Wo', 'MD'),('would', 'MD'),('Would', 'MD'),
		("'d", 'MD'),('shall', 'MD'),('Shall', 'MD'),('should', 'MD'),('Should', 'MD'),
		('may', 'MD'),('May', 'MD'),('might', 'MD'),('Might', 'MD'),('must', 'MD'),('Must', 'MD'),
		('ought', 'MD'),('Ought', 'MD'))
	for word in taggedtext:
		if word in Modals:
			taggedtext.remove(word)
		else:
			continue
	#Removing modal 'got'
	for i in range(1,(len(taggedtext)-(1+rnge))):
		if taggedtext[i] == ('to', 'TO'): 
			if taggedtext[i-1] == ('got', 'VBN'):
				taggedtext.remove(taggedtext[i-1])
			else:
				continue
		else:
			continue

	ModalNeed= (('need', 'VB'),('Need', 'VB'),('need', 'VBP'),('Need', 'VBP'), ('need', 'MD'),('needed', 'VBD'),('Needed', 'VBD'))
	Negative= (("n't", 'RB'),('not', 'RB'))
	for i in range(1,(len(taggedtext)-(5+rnge))): 
		if taggedtext[i-1] in ModalNeed: 
			if taggedtext[i] != ('to', 'TO'): #Following the original grammar rules: need + to = main verb, instead of semi-modal
				if taggedtext[i] in Negative:
					taggedtext.remove(taggedtext[i-1])
				else:
					for word in taggedtext[i]:
						if word == 'VB':
							taggedtext[i-1]="I need to rename this, in order to avoid removing all 'need'"
							taggedtext.remove(taggedtext[i-1])
						else:
							continue
					for word in taggedtext: #problem: NOT CASE-SENSITIVE??????????!!!!!!!!!!
						if word == ('Need', 'VB'): #only modal need can initiate a sentence
							#print('Beginning', word)
							taggedtext.remove(word)
						else:
							continue
			else:
				continue
		else:
			continue
	for i in range(1,(len(taggedtext)-(6+rnge))): 
		if taggedtext[i-1] in ModalNeed: 
			if taggedtext[i] != ('to', 'TO'): 
				for word in taggedtext[i+1]: #problem: '... need her. Do' --> need=removed!
					if word == 'VB':
						taggedtext.remove(taggedtext[i-1])
					else:
						continue
			else:
				continue
		else:
			continue
	modalcount = propcount-len(taggedtext)
	#print('#removed modals: ', modalcount)
	propcount= len(taggedtext)


	#Removing auxiliary verbs
	#Problem: sentences like 'Why did you tell her that...' --> 'did' is NOT removed
	AuxDO= (('do', 'VBP'),('Do', 'VBP'),('does', 'VBZ'),('Does', 'VBZ'),('did', 'VBD'),('Did', 'VBD'))
	FollowingAux = (("n't", 'RB'),('not', 'RB'),('been', 'VBN'))
	for i in range(5,(len(taggedtext)-(2+(100*rnge)))): 
		if taggedtext[i] in FollowingAux: 
			if taggedtext[i-1] in AuxDO:
				taggedtext.remove(taggedtext[i-1])
		else:
			continue
	for word in taggedtext: #removing do-verbs that initate a sentence.
		if (word == ('Do','VBP') or word == ('Does', 'VBZ')):
			taggedtext.remove(word)
	DOcount = propcount-len(taggedtext)
	#print('#removed Do-verbs: ', DOcount)
	propcount= len(taggedtext)


	AuxHAVE= (('have', 'VBP'),('Have', 'VBP'),('has', 'VBZ'),('Has', 'VBZ'),("'ve", 'VBP'),
		('had', 'VBD'),('Had', 'VBD'),('have', 'VB'))
	FolHAVE=('VBN','TO')
	for i in range(1,(len(taggedtext)-(6+10*rnge))): 
		if taggedtext[i] in FollowingAux: 
			if taggedtext[i-1] in AuxHAVE:
				taggedtext.remove(taggedtext[i-1])
		elif taggedtext[i-1] in AuxHAVE: 
			for word in taggedtext[i]:
				if word in FolHAVE:
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
			for word in taggedtext[i+1]:
				if word in FolHAVE:
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue
	HAVEcount = propcount-len(taggedtext)
	#print('#removed HAVE-verbs: ', HAVEcount)
	propcount= len(taggedtext)


	AuxBE= (('am', 'VBP'),('Am', 'VBP'),("'m", 'VBP'),('are', 'VBP'),('Are', 'VBP'),("'re", 'VBP'),
		('is','VBZ'),('Is','VBZ'),("'s",'VBZ'),('was','VBD'),('Was','VBD'),('were','VBD'),
		('Were','VBD'),('been','VBN'),('Been','VBN'),('being','VBG'),('Being','VBG'),('be', 'VB'))
	FolBE= ('VBG','VBN','TO') #TO --> Modal 'be to +verb'
	for i in range(1,(len(taggedtext)-(9+rnge))): 
		if taggedtext[i-1] in AuxBE:
			for word in taggedtext[i]:
				if word in FolBE:
					taggedtext[i-1]='remove'
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
			for word in taggedtext[i+1]:
				if word in FolBE:
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		if taggedtext[i-1] in AuxBE: #without repetition of if-clause: removal of wrong word!!
			for word in taggedtext[i+2]:
				if word in FolBE:
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue
	BEcount = propcount-len(taggedtext)
	#print('#removed BE-verbs: ', BEcount)
	propcount= len(taggedtext)


	AuxGET = (('get', 'VBP'), ('gets', 'VBZ'),('got', 'VBD'))
	for i in range(1,(len(taggedtext)-(5+rnge))): 
		if taggedtext[i-1] in AuxGET:
			for word in taggedtext[i]:
				if word == 'VBN':
					taggedtext.remove(taggedtext[i-1])

	#removing aux 'used/able/going/need to'
	Xto = (('used', 'VBD'),('going', 'VBG'),('able', 'JJ'),('need', 'VB'),('need', 'VBP'),('needs', 'VBZ'))
	for i in range(1,(len(taggedtext)-(7+rnge))): 
		if taggedtext[i-1] in Xto: 
			if taggedtext[i] == ('to', 'TO'):
				for word in taggedtext[i+1]:
					if word == 'VB':
						word ="I need to rename this, in order to avoid removing all TO's"
						taggedtext.remove(taggedtext[i-1])
			else:
				continue			
		else:
			continue
	#print('Propositions -aux: ',taggedtext)
	AUXcount = propcount-len(taggedtext)
	#print('#removed other AUX-verbs: ', AUXcount)
	propcount= len(taggedtext)

	
	#Removing 'To' in 'to+verb'
	#Problem: Only removes all 'To'(+verb) after second identical loop. (=Overall problem)
	FolTO = ('VB','VBG','VBN') #When aux have&be are removed-->> (VBG: have to be ..ing--> to ...ing) (VBN: ought to have ..ed --> to ..ed)
	NOTFOLTO = ('DT','NNP','NN','NNS','NNPS','PRP','PRP$') 
	for i in range(1,(len(taggedtext)-(12+(2*rnge)))):
		if taggedtext[i-1] == ('to', 'TO'): 
			for word in taggedtext[i]:
				if word not in NOTFOLTO: #extra security
					if word in FolTO:
						taggedtext[i-1]="I need to rename this, in order to avoid removing al TO's"
						taggedtext.remove(taggedtext[i-1])
					else:
						continue
				else:
					continue
		else:
			continue
	for i in range(1,(len(taggedtext)-(3+rnge))): #removing 'to' bij 'to+verb' 
		if taggedtext[i-1] == ('to', 'TO'): 
			for word in taggedtext[i]:
				if word not in NOTFOLTO:
					if word in FolTO:
						taggedtext[i-1]="I need to rename this, in order to avoid removing al TO's"
						taggedtext.remove(taggedtext[i-1])
					else:
						continue
				else:
					continue
		else:
			continue
	TOcount = propcount-len(taggedtext)
	#print("#removed TO's: ", TOcount)
	propcount= len(taggedtext)

	
	#Removing prime copula 'to be', followed by AdjP
	PrimeCopula = (('be','VB'),('am','VBP'),("'m",'VBP'),('are','VBP'),("'re",'VBP'),('is','VBZ'),("'s",'VBZ'),
		('was','VBD'),('were','VBD'),('been','VBN'),('being','VBG'))
	AdjP= ('JJ','JJR','JJS')
	for i in range(1,(len(taggedtext)-(1+rnge))): 
		if taggedtext[i-1] in PrimeCopula:
			for word in taggedtext[i]:
				if word in AdjP:
					taggedtext[i-1]="to be removed"
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue
	for i in range(1,(len(taggedtext)-(1+rnge))): 
		if taggedtext[i-1] in PrimeCopula:
			for word in taggedtext[i]:
				if word == 'RB':
					for word in taggedtext[i+1]:
						if word in AdjP:
							taggedtext[i-1]="To be removed"
							taggedtext.remove(taggedtext[i-1])
						else:
							continue
				else:
					continue
		else:
			continue		
	BECOPcount = propcount-len(taggedtext)
	#print('#removed COPULA-verbs: ', BECOPcount)
	propcount= len(taggedtext)

	#Removing secondary copula, followed by AdjP
	CopulaInchoative= (('become','VB'),('become','VBP'),('becomes','VBZ'),('became','VBD'),('become','VBN'),('becoming','VBG'),
		('come','VB'),('come','VBP'),('comes','VBZ'),('came','VBD'),('come','VBN'),('coming','VBG'),
		('fall','VB'),('fall','VBP'),('falls','VBZ'),('fell','VBD'),('fallen','VBN'),('falling','VBG'),
		('get','VB'),('get','VBP'),('gets','VBZ'),('got','VBD'),('got','VBN'),('gotten','VBN'),('getting','VBG'),
		('go','VB'),('go','VBP'),('goes','VBZ'),('went','VBD'),('gone','VBN'),('going','VBG'),
		('grow','VB'),('grow','VBP'),('grows','VBZ'),('grew','VBD'),('grown','VBN'),('growing','VBG'),
		('run','VB'),('run','VBP'),('runs','VBZ'),('ran','VBD'),('ran','VBN'),('running','VBG'),
		('turn','VB'),('turn','VBP'),('turn','VBZ'),('turned','VBD'),('turned','VBN'),('turning','VBG'),
		('wear','VB'),('wear','VBP'),('wears','VBZ'),('wore','VBD'),('worn','VBN'),('wearing','VBG'))
	CopulaSenses= (('feel','VB'),('feel','VBP'),('feels','VBZ'),('felt','VBD'),('felt','VBN'),('feeling','VBG'),
		('taste','VB'),('taste','VBP'),('tastes','VBZ'),('tasted','VBD'),('tasted','VBN'),('tasting','VBG'),
		('smell','VB'),('smell','VBP'),('smells','VBZ'),('smelled','VBD'),('smelt','VBD'),('smelled','VBN'),('smelt','VBN'),('smelling','VBG'),
		('sound','VB'),('sound','VBP'),('sounds','VBZ'),('sounded','VBD'),('sounded','VBN'),('sounding','VBG'),
		('look','VB'),('look','VBP'),('looks','VBZ'),('looked','VBD'),('looked','VBN'),('looking','VBG'))
	CopulaOthers= (('appear','VB'),('appear','VBP'),('appears','VBZ'),('appeared','VBD'),('appeared','VBN'),('appearing','VBG'),
		('prove','VB'),('prove','VBP'),('proves','VBZ'),('proved','VBD'),('proven','VBN'),('proved', 'VBN'),('proving','VBG'),
		('remain','VB'),('remain','VBP'),('remains','VBZ'),('remained','VBD'),('remained','VBN'),('remaining','VBG'),
		('seem','VB'),('seem','VBP'),('seems','VBZ'),('seemed','VBD'),('seemed','VBN'),('seeming','VBG'),
		('sound','VB'),('sound','VBP'),('sounds','VBZ'),('sounded','VBD'),('sounded','VBN'),('sounding','VBG'),
		('look','VB'),('look','VBP'),('looks','VBZ'),('looked','VBD'),('looked','VBN'),('looking','VBG'))
	for i in range(1,(len(taggedtext)-(6+rnge))): 
		if (taggedtext[i-1] in CopulaInchoative or taggedtext[i-1] in CopulaSenses or taggedtext[i-1] in CopulaOthers):
			for word in taggedtext[i]:
				if word in AdjP:
					taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext)-(2+rnge))): 
		if (taggedtext[i-1] in CopulaInchoative or taggedtext[i-1] in CopulaSenses or taggedtext[i-1] in CopulaOthers):
			for word in taggedtext[i]:
				if word == 'RB':
					for word in taggedtext[i+1]:
						if word in AdjP:
							taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue

	#print('Propositions -COP: ',taggedtext)
	COPcount = propcount-len(taggedtext)
	#print('#removed COPULA-verbs: ', COPcount)
	propcount= len(taggedtext)

	#Removing non-propositional tags + some determiners
	#Problem: see overall problem. 3 identical loops needed!!
	Removetags = ('NNP','NN','NNS','NNPS','PRP','RP','EX')
	for word in taggedtext: #word= ('word','tag')
		if word[1] in Removetags:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext: 
		if word[1] in Removetags:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext: 
		if word[1] in Removetags:
			taggedtext.remove(word)
		else:
			continue
	TAGcount = propcount-len(taggedtext)
	#print('#removed non-prop tags: ', TAGcount)
	propcount= len(taggedtext)

	RemoveDT= ('a','A','an','An','the','The')
	for word in taggedtext: #word= ('word','tag')
		if word[0] in RemoveDT:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext: 
		if word[0] in RemoveDT:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext: 
		if word[0] in RemoveDT:
			taggedtext.remove(word)
		else:
			continue

	#print('Propositions -tags etc. : ',taggedtext)
	DTcount = propcount-len(taggedtext)
	#print('#removed DT(a,an,the): ', DTcount)
	propcount= len(taggedtext)
	#print('Propositions : ',taggedtext)

	#5. Measuring PD (#prop./#words)
	propdensity= propcount/wordcount
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>STATISTICS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<',
		'\n\nPropositional Idea Density: 	\t',propdensity,
		'\n----------------------------------------------------------------------',
		'\nOriginal tagged text: 	\t\t\t', Originaltext,
		'\nTotal wordcount: 		\t\t\t', wordcount,'items',
		'\nNumber of removed items (Absolute number, Relative number):',
		'\n\t>> Modals: 			\t\t\t', modalcount,'\t\t',round(modalcount/wordcount,5),
		'\n\t>> Auxiliary "to do": 	\t\t', DOcount,'\t\t',round(DOcount/wordcount,5),
		'\n\t>> Auxiliary "to have": \t\t', HAVEcount,'\t\t',round(HAVEcount/wordcount,5),
		'\n\t>> Auxiliary "to be": 	\t\t', BEcount,'\t\t',round(BEcount/wordcount,5),
		'\n\t>> Remaining auxiliaries: 	\t', AUXcount,'\t\t',round(AUXcount/wordcount,5),
		'\n\t>> "TO" followed by a verb: \t', TOcount,'\t\t',round(TOcount/wordcount,5),
		'\n\t>> Copula "to be": 		\t\t', BECOPcount,'\t\t',round(BECOPcount/wordcount,5),
		'\n\t>> Other copulas: 			\t', COPcount,'\t\t',round(COPcount/wordcount,5),
		'\n\t>> Non-propositional tags:	\t', TAGcount,'\t',round(TAGcount/wordcount,5),
		'\n\t>> "a,an,the"-determiners: \t\t', DTcount,'\t',round(DTcount/wordcount,5),
		'\n\nTagged propositions: 		\t\t', taggedtext)

	#Next step: printing to new file
	#Next next step: pickle

IdeaDensity('secondtext.txt')