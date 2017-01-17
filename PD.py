import nltk
from nltk import word_tokenize, pos_tag

def IdeaDensity(inputtext):
	#1. tokenization & part-of-speech tagging
	f = open(inputtext,'rt', encoding='utf-8-sig') 
	text=f.read()
	f.close()

	tokenized= word_tokenize(text)
	taggedtext = pos_tag(tokenized)
	Originaltext = pos_tag(tokenized)

	#2. Total word count
	#Deleting punctuation
	#Problem: Only removes all punctuation after a second& even third identical loop. 
	#=> OVERALL PROBLEM: 2 items with same tag: No removal of second item!!
	Punctuation = (',','.','!',';','?',':',"'","''",'``','(',')','[',']')
	for word in taggedtext:
		if (word[1] in Punctuation) or (word[0] in Punctuation):
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext:
		if (word[1] in Punctuation) or (word[0] in Punctuation):
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext:
		if (word[1] in Punctuation) or (word[0] in Punctuation):
			taggedtext.remove(word)
		else:
			continue
	wordcount = len(taggedtext)

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
	"""'to'+verb = 1 prop
	COPULA + NP ==> copula = prop 
	COPULA + AdjP ==> copula(linking verb) != prop  (AdjP=prop!)"""
	propcount= len(taggedtext)

	#Removing positive modals from prop count.
	#For negative modals: Modal is removed, negative part carries prop count & is not removed(otherwise: double count)
	#Modal 'Have to' is removed in a later stage, when removing 'have' as a auxiliary verb
	Modals = (('can', 'MD'),('ca','MD'),('Can', 'MD'),('could', 'MD'),('Could', 'MD'),('will', 'MD'),
		('Will', 'MD'),("'ll", 'MD'),('wo', 'MD'),('Wo', 'MD'),('would', 'MD'),('Would', 'MD'),
		("'d", 'MD'),('shall', 'MD'),('Shall', 'MD'),('should', 'MD'),('Should', 'MD'),
		('may', 'MD'),('May', 'MD'),('might', 'MD'),('Might', 'MD'),('must', 'MD'),('Must', 'MD'),
		('ought', 'MD'),('Ought', 'MD'))
	for word in taggedtext:
		if word in Modals:
			taggedtext.remove(word)
	regmodalcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	#Removing modal 'got'
	countGot=1
	for word in taggedtext:
		if word == ('got', 'VBN'):
			countGot+=1
	for i in range(1,(len(taggedtext)-countGot)):
		if taggedtext[i] == ('to', 'TO'): 
			if taggedtext[i-1] == ('got', 'VBN'):
				taggedtext[i-1]='I (have) got to go'
				taggedtext.remove(taggedtext[i-1])

	ModalHave= (('have', 'VBP'),('Have', 'VBP'),('has', 'VBZ'),('Has', 'VBZ'),("'ve", 'VBP'),
		('had', 'VBD'),('Had', 'VBD'),('have', 'VB'))
	countHave=1
	for word in taggedtext:
		if word in ModalHave:
			countHave+=1
	for i in range(1,len(taggedtext)-countHave):
		if taggedtext[i-1] in ModalHave:
			if taggedtext[i] == ('to', 'TO'):
				taggedtext[i-1]='I have to...'
				taggedtext.remove(taggedtext[i-1])
	HaveTocount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	BeTo= (('am', 'VBP'),('Am', 'VBP'),("'m", 'VBP'),('are', 'VBP'),('Are', 'VBP'),("'re", 'VBP'),
		('is','VBZ'),('Is','VBZ'),("'s",'VBZ'),('was','VBD'),('Was','VBD'),('were','VBD'),('Were','VBD'))
	countBe=1
	for word in taggedtext:
		if word in BeTo:
			countBe+=1
	for i in range(1,(len(taggedtext)-(int((countBe)/2)))):
		if taggedtext[i-1] in BeTo:
			if taggedtext[i] == ('to', 'TO'):
				taggedtext[i-1]='Such people are to be pitied'
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i] == (("n't", 'RB')) or (taggedtext[i] == ('not', 'RB')):
				if taggedtext[i+1] == ('to', 'TO'):
					taggedtext[i-1]='Such people are not to be pitied'
					taggedtext.remove(taggedtext[i-1])
	BeTocount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	ModalNeed= (('need', 'VB'),('Need', 'VB'),('need', 'VBP'),('Need', 'VBP'), ('need', 'MD'),('needed', 'VBD'),('Needed', 'VBD')) #be aware of the 3 types of Need:modal, semi-modal/aux,lexical verb
	Negative= (("n't", 'RB'),('not', 'RB'))
	countNeed1=1
	for word in taggedtext:
		if word in ModalNeed:
			countNeed1+=1
	for i in range(1,(len(taggedtext))-countNeed1): 
		if taggedtext[i-1] in ModalNeed: 
			if taggedtext[i] != ('to', 'TO'): #Following the original grammar rules: need + to != modal verb
				if taggedtext[i] in Negative:
					taggedtext[i-1]="I needn't..."
					taggedtext.remove(taggedtext[i-1])
				elif str(taggedtext[i]).endswith("'VB')"):
					taggedtext[i-1]="She need have no fear"
					taggedtext.remove(taggedtext[i-1])
				elif str(taggedtext[i+1]).endswith("'VB')"):
					taggedtext[i-1]="You need just ask/ Need I ask?"
					taggedtext.remove(taggedtext[i-1])					
	countNeed2=1
	for word in taggedtext:
		if word in ModalNeed:
			countNeed2+=1
	for i in range(1,(len(taggedtext))-countNeed2): 
		if taggedtext[i-1] in ModalNeed: 
			if str(taggedtext[i]).endswith("'PRP')"): 
				if (str(taggedtext[i+2]).endswith("'VB')")) or (str(taggedtext[i+2]).endswith("'VBP')")):
					if str(taggedtext[i+1]).endswith("'RB')"):
						taggedtext[i-1]='Need she really say that?'
						taggedtext.remove(taggedtext[i-1])
	Needmodalcount = propcount-len(taggedtext)
	propcount= len(taggedtext)
	modalcount = wordcount-len(taggedtext)

	#Removing auxiliary verbs
	AuxDO= (('do', 'VBP'),('Do', 'VBP'),('does', 'VBZ'),('Does', 'VBZ'),('did', 'VBD'),('Did', 'VBD'))
	FollowingAux = (("n't", 'RB'),('not', 'RB'),('been', 'VBN'))
	PRP = (('I','PRP'),('you','PRP'),('she','PRP'),('he','PRP'),('we','PRP'),('they','PRP'),('it','PRP'))
	countDo1=1
	for word in taggedtext:
		if word in AuxDO:
			countDo1+=1
	for i in range(2,(len(taggedtext))-countDo1): 
		if taggedtext[i-2] != ('to','TO'):
			if taggedtext[i] in FollowingAux: 
				if taggedtext[i-1] in AuxDO:
					taggedtext[i-1]= "Don't you understand?"
					taggedtext.remove(taggedtext[i-1])
	countDo2=1
	for word in taggedtext:
		if word in AuxDO:
			countDo2+=1
	for i in range(1,(len(taggedtext))-countDo2):
		if taggedtext[i-1] in AuxDO:
			if taggedtext[i] in PRP:
				for word in taggedtext[i+1]:
					if word == ('VB'):
						taggedtext[i-1]='Why did you call me?'
						taggedtext.remove(taggedtext[i-1])
	countDo3=1
	for word in taggedtext:
		if word in AuxDO:
			countDo3+=1
	for i in range(1,(len(taggedtext))-countDo3):
		if taggedtext[i] in AuxDO:
			if str(taggedtext[i-1]).endswith("'WRB')"):
				taggedtext[i]='Where does this man come from?'
				taggedtext.remove(taggedtext[i])
	DOcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	AuxHAVE= (('have', 'VBP'),('Have', 'VBP'),('has', 'VBZ'),('Has', 'VBZ'),("'ve", 'VBP'),
		('had', 'VBD'),('Had', 'VBD'),('have', 'VB'))
	FolHAVE=('VBN','VBD') #VBD: test-run on larger text mistakingly tagged VBN as VBD. Won't do any harm to add this to the removal-list
	countHave1=1
	for word in taggedtext:
		if word in AuxHAVE:
			countHave1+=1
	for i in range(1,(len(taggedtext)-countHave1)):
		if taggedtext[i] in FollowingAux: 
			if taggedtext[i-1] in AuxHAVE:
				taggedtext[i-1]='I have not been honest.'
				taggedtext.remove(taggedtext[i-1])
		elif taggedtext[i-1] in AuxHAVE: 
			for word in taggedtext[i]:
				if word in FolHAVE:
					taggedtext[i-1]='You have done a great job'
					taggedtext.remove(taggedtext[i-1])
			for word in taggedtext[i+1]:
				if word in FolHAVE:
					taggedtext[i-1]='But she has actually done a better job'
					taggedtext.remove(taggedtext[i-1])
	HAVEcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	AuxBE= (('am', 'VBP'),('Am', 'VBP'),("'m", 'VBP'),('are', 'VBP'),('Are', 'VBP'),("'re", 'VBP'),
		('is','VBZ'),('Is','VBZ'),("'s",'VBZ'),('was','VBD'),('Was','VBD'),('were','VBD'),
		('Were','VBD'),('been','VBN'),('Been','VBN'),('being','VBG'),('Being','VBG'),('be', 'VB'))
	FolBE= ('VBG','VBN')
	countBe1=1
	for word in taggedtext:
		if word in AuxBE:
			countBe1+=1
	for i in range(1,(len(taggedtext)-(int((countBe1)/2)))):
		if taggedtext[i-1] in AuxBE:
			for word in taggedtext[i]:
				if word in FolBE:
					taggedtext[i-1]='She has been beaten up'
					taggedtext.remove(taggedtext[i-1])
	countBe2=1
	for word in taggedtext:
		if word in AuxBE:
			countBe2+=1
	for i in range(1,(len(taggedtext))-countBe2):
		if taggedtext[i-1] in AuxBE:
			if not str(taggedtext[i]).endswith("'DT')"):
				for word in taggedtext[i+1]:
					if word in FolBE:
						taggedtext[i-1]='I am just kidding'
						taggedtext.remove(taggedtext[i-1])
	countBe3=1
	for word in taggedtext:
		if word in AuxBE:
			countBe3+=1
	for i in range(1,(len(taggedtext))-countBe3):
		if taggedtext[i-1] in AuxBE: 
			if not str(taggedtext[i]).endswith("'DT')"):
				for word in taggedtext[i+2]:
					if word in FolBE:
						taggedtext[i-1]='I am really just kidding'		
						taggedtext.remove(taggedtext[i-1])
	BEcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	AuxGET = (('get', 'VBP'), ('gets', 'VBZ'),('got', 'VBD'))
	countGet1=1
	for word in taggedtext:
		if word in AuxGET:
			countGet1+=1
	for i in range(1,(len(taggedtext))-countGet1):
		if taggedtext[i-1] in AuxGET:
			for word in taggedtext[i]:
				if word == 'VBN':
					taggedtext[i-1]='He got beaten up'
					taggedtext.remove(taggedtext[i-1])
	GETcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	#removing aux 'used/able/going'
	Xto = (('used', 'VBD'),('going', 'VBG'),('able', 'JJ'))
	countAux1=1
	for word in taggedtext:
		if word in Xto:
			countAux1+=1
	for i in range(1,(len(taggedtext)-countAux1)):
		if taggedtext[i-1] in Xto: 
			if taggedtext[i] == ('to', 'TO'):
				if str(taggedtext[i+1]).endswith("'VB')"):
					taggedtext[i-1]='I am able to pass that test.'
					taggedtext.remove(taggedtext[i-1])
	countAux2=1
	for word in taggedtext:
		if word == ('used', 'VBD'):
			countAux2+=1
	for i in range(1,(len(taggedtext)-countAux2)):
		if (taggedtext[i-1] == ('used', 'VBD')) or (taggedtext[i-1] == ('Used', 'VBD')):
			if taggedtext[i] == ("n't", 'RB'):
				taggedtext[i-1]= "usedn't to/Usedn't to"
				taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext)-countAux2)):
		if taggedtext[i-1] == ('Used', 'VBD'):
			if str(taggedtext[i]).endswith("'PRP')"):
				taggedtext[i-1]='sentence initial basic form: Used he to...'
				taggedtext.remove(taggedtext[i-1])
	Xtocount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	#removing aux 'need to'
	Needto = (('need', 'VB'),('need', 'VBP'),('needs', 'VBZ'),('needed','VBD'))
	countNeed3=1
	for word in taggedtext:
		if word in Needto:
			countNeed3+=1
	for i in range(1,(len(taggedtext))-countNeed3):
		if taggedtext[i-1] in Needto: 
			if taggedtext[i] == ('to', 'TO'):
				if str(taggedtext[i+1]).endswith("'VB')"):
					taggedtext[i-1]='I need to pass this test'
					taggedtext.remove(taggedtext[i-1])
	#Sentence ambiguity: 'I need a teddybear to comfort me'(lexical need) != 'I need you to stop laughing'(an order). --> Safe option: basic structure need+to+VB
	NeedTocount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	AUXcount = GETcount+Xtocount+NeedTocount
	propcount= len(taggedtext)

	#Removing 'To' in 'to+verb'
	#Problem: Only removes all 'To'(+verb) after second identical loop. (=Overall problem)
	FolTO = ('VB','VBG','VBN') #When aux have&be are removed-->> (VBG: have to be ..ing--> to ...ing) (VBN: ought to have ..ed --> to ..ed)
	NOTFOLTO = ('DT','NNP','NN','NNS','NNPS','PRP','PRP$') 
	countTo1=1
	for word in taggedtext:
		if word == ('to', 'TO'):
			countTo1+=1
	for i in range(1,(len(taggedtext)-countTo1)):
		if taggedtext[i-1] == ('to', 'TO'): 
			for word in taggedtext[i]:
				if word not in NOTFOLTO: #extra security
					if word in FolTO:
						taggedtext[i-1]="I adviced him to start studying"
						taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext))): #removing 'to' bij 'to+verb' 
		if taggedtext[i-1] == ('to', 'TO'): 
			for word in taggedtext[i]:
				if word not in NOTFOLTO:
					if word in FolTO:
						taggedtext[i-1]="But he made no effort to listen."
						taggedtext.remove(taggedtext[i-1])
	TOcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	#Removing prime copula 'to be', followed by AdjP
	PrimeCopula = (('be','VB'),('am','VBP'), ('Am', 'VBP'),("'m",'VBP'),('are','VBP'),('Are', 'VBP'),("'re",'VBP'),
		('is','VBZ'),('Is', 'VBZ'),("'s",'VBZ'),('was','VBD'),('Was', 'VBD'),('were','VBD'),('Were', 'VBD'),
		('been','VBN'),('being','VBG'))
	AdjP= ('JJ','JJR','JJS')
	countBe4=1
	for word in taggedtext:
		if word in PrimeCopula:
			countBe4+=1
	for i in range(1,(len(taggedtext)-int(countBe4/2))):
		if taggedtext[i-1] in PrimeCopula:
			for word in taggedtext[i]:
				if word in AdjP:
					taggedtext[i-1]="I am happy"
					taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext)-int(countBe4/2))): 
		if taggedtext[i-1] in PrimeCopula:
			if (str(taggedtext[i]).endswith("'RB')")):
				for word in taggedtext[i+1]:
					if word in AdjP:
						taggedtext[i-1]="I am very happy"
						taggedtext.remove(taggedtext[i-1])
					elif word == 'RB':
						for word in taggedtext[i+2]:
							if word in AdjP:
								taggedtext[i-1]="I am not very happy"
								taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext)-int(countBe4/2))): 
		if taggedtext[i-1] in PrimeCopula:
			if str(taggedtext[i]).endswith("'PRP')"):
				for word in taggedtext[i+1]:
					if word in AdjP:
						taggedtext[i-1]="Is she happy?"
						taggedtext.remove(taggedtext[i-1])
					elif word == 'RB':
						for word in taggedtext[i+2]:
							if word in AdjP:
								taggedtext[i-1]="am I not happy?"
								taggedtext.remove(taggedtext[i-1])
							elif word == 'RB':
								for word in taggedtext[i+3]:
									if word in AdjP:
										taggedtext[i-1]="Is she not very happy?"
										taggedtext.remove(taggedtext[i-1])
	BECOPcount = propcount-len(taggedtext)
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
	Copulagroup=(CopulaInchoative+CopulaSenses+CopulaOthers)
	countCop1=1
	for word in taggedtext:
		if word in Copulagroup:
			countCop1+=1
	for i in range(1,(len(taggedtext))-countCop1):
		if taggedtext[i-1] in Copulagroup:
			for word in taggedtext[i]:
				if word in AdjP:
					taggedtext[i-1]='She looked pretty'
					taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext))-countCop1):
		if taggedtext[i-1] in Copulagroup:
			for word in taggedtext[i]:
				if word == 'RB':
					for word in taggedtext[i+1]:
						if word in AdjP:
							taggedtext[i-1]='She turned completely red'
							taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext))-countCop1):
		if taggedtext[i-1] in Copulagroup:
			if str(taggedtext[i]).endswith("'RB')"):
				if str(taggedtext[i+1]).endswith("'RB')"):
					for word in taggedtext[i+2]:
						if word in AdjP:
							taggedtext[i-1]="She sounded extremely, horribly bad"
							taggedtext.remove(taggedtext[i-1])
	for i in range(1,(len(taggedtext))-countCop1):
		if taggedtext[i-1] in CopulaSenses:
			if taggedtext[i] == ('like', 'IN'):
				taggedtext[i-1]='The house smells like my grandmother'
				taggedtext.remove(taggedtext[i-1])
	COPcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	#Removing non-propositional tags + some determiners
	#Problem: see overall problem. 4 identical loops needed!! (test-run on conrad.txt still kept 2 NN & 1 PRP after 3loops)
	Nouns = ('NNP','NN','NNS','NNPS','PRP')
	for word in taggedtext: #word= ('word','tag')
		if word[1] in Nouns:
			taggedtext.remove(word)
	for word in taggedtext: 
		if word[1] in Nouns:
			taggedtext.remove(word)
	for word in taggedtext: 
		if word[1] in Nouns:
			taggedtext.remove(word)
	for word in taggedtext: 
		if word[1] in Nouns:
			taggedtext.remove(word)
	Nouncount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	for word in taggedtext: 
		if word[1] == 'RP':
			taggedtext.remove(word)
	Particlecount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	for word in taggedtext: 
		if word[1] == 'EX':
			taggedtext.remove(word)
	EXcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	for word in taggedtext: 
		if word[1] == 'FW':
			taggedtext.remove(word)
	FWcount = propcount-len(taggedtext)
	propcount= len(taggedtext)	

	for word in taggedtext: 
		if word[1] == 'LS':
			taggedtext.remove(word)
	LScount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	TAGcount = Nouncount+Particlecount+EXcount+FWcount+LScount
	propcount= len(taggedtext)

	RemoveDT= ('a','A','an','An','the','The')
	for word in taggedtext: #word= ('word','tag')
		if word[0] in RemoveDT:
			taggedtext.remove(word)
	for word in taggedtext: 
		if word[0] in RemoveDT:
			taggedtext.remove(word)
	DTcount = propcount-len(taggedtext)
	propcount= len(taggedtext)

	#5. Measuring PD (#prop./#words)
	propdensity= propcount/wordcount

	#6. Output
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>STATISTICS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<',
		'\n\nPropositional Idea Density:\t\t\t',propdensity,
		'\n----------------------------------------------------------------------',
		'\nTotal wordcount:\t\t\t\t\t', wordcount,'items',
		'\nNumber of removed items (Absolute number, Relative number):',
		'\n\t>> Modals:\t\t\t\t\t\t', modalcount,'\t\t\t',round(modalcount/wordcount,5),
		'\n\t>> Auxiliary "to do":\t\t\t', DOcount,'\t\t\t',round(DOcount/wordcount,5),
		'\n\t>> Auxiliary "to have":\t\t\t', HAVEcount,'\t\t\t',round(HAVEcount/wordcount,5),
		'\n\t>> Auxiliary "to be":\t\t\t', BEcount,'\t\t\t',round(BEcount/wordcount,5),
		'\n\t>> Remaining auxiliaries:\t\t', AUXcount,'\t\t\t',round(AUXcount/wordcount,5),
		'\n\t>> "TO" followed by a verb:\t\t', TOcount,'\t\t\t',round(TOcount/wordcount,5),
		'\n\t>> Copula "to be":\t\t\t\t', BECOPcount,'\t\t\t',round(BECOPcount/wordcount,5),
		'\n\t>> Other copulas:\t\t\t\t', COPcount,'\t\t\t',round(COPcount/wordcount,5),
		'\n\t>> Non-propositional tags:\t\t',TAGcount,'\t\t\t',round(TAGcount/wordcount,5),
		'\n\t>> "a,an,the"-determiners:\t\t', DTcount,'\t\t\t',round(DTcount/wordcount,5),
		'\n----------------------------------------------------------------------',
		'\nOriginal tagged text: \t\t\t\t', Originaltext,
		'\n\nTagged propositions: \t\t\t\t', taggedtext)
	
	import time
	print('Date of analysis:\t'+time.strftime("%Y-%m-%d %H:%M"))

	statistics='>>>>>>>>>>>>>>>>>>>>>>>>>>>>>STATISTICS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'+'\n\nPropositional Idea Density: \t\t'+str(propdensity)+'\n----------------------------------------------------------------------'+'\nTotal wordcount: 	\t\t'+ str(wordcount)+' items'+'\nNumber of removed items (Absolute number, Relative number):'+'\n\t>> Modals: 	\t\t' +str(modalcount)+'\t\t'+str(round(modalcount/wordcount,5))+'\n\t>> Auxiliary "to do":\t\t'+ str(DOcount)+'\t\t'+str(round(DOcount/wordcount,5))+'\n\t>> Auxiliary "to have":\t\t'+ str(HAVEcount)+'\t\t'+str(round(HAVEcount/wordcount,5))+'\n\t>> Auxiliary "to be": \t\t' +str(BEcount)+'\t\t'+str(round(BEcount/wordcount,5))+'\n\t>> Remaining auxiliaries: \t' +str(AUXcount)+'\t\t'+str(round(AUXcount/wordcount,5))+'\n\t>> "TO" followed by a verb:\t' +str(TOcount)+'\t\t'+str(round(TOcount/wordcount,5))+'\n\t>> Copula "to be":\t\t' +str(BECOPcount)+'\t\t'+str(round(BECOPcount/wordcount,5))+'\n\t>> Other copulas:\t\t' +str(COPcount)+'\t\t'+str(round(COPcount/wordcount,5))+'\n\t>> Non-propositional tags:\t' +str(TAGcount)+'\t\t'+str(round(TAGcount/wordcount,5))+'\n\t>> "a,an,the"-determiners:\t'+ str(DTcount)+'\t\t'+str(round(DTcount/wordcount,5))+'\n----------------------------------------------------------------------'+'\nDate of analysis:\t'+str(time.strftime("%Y-%m-%d %H:%M"))+'\n\noriginal text:\t\t\t'+str(text)+'\n\nOriginal tagged text: \t\t\t' +str(Originaltext)+'\n\nTagged propositions: \t\t\t' +str(taggedtext)
	composition='>>>>>>>>>>>>>>>>>>>>>>>>>>Compositional Analysis<<<<<<<<<<<<<<<<<<<<<<<<<<<<'+'\n\nPropositional Idea Density: \t\t'+str(propdensity)+'\n----------------------------------------------------------------------'+'\nTotal wordcount: 	\t\t'+ str(wordcount)+' items'+'\nNumber of removed items (Absolute number, Relative number):'+'\n Modals: 	\t\t' +'\n\t>> Principal Modals: \t\t' +str(regmodalcount)+'\t\t'+str(round(regmodalcount/wordcount,5))+'\n\t>> Modal verb "have (got) to":\t' +str(HaveTocount)+'\t\t'+str(round(HaveTocount/wordcount,5))+'\n\t>> Modal verb "be to": \t\t' +str(BeTocount)+'\t\t'+str(round(BeTocount/wordcount,5))+'\n\t>> Modal verb "need": \t\t' +str(Needmodalcount)+'\t\t'+str(round(Needmodalcount/wordcount,5))+'\n Auxiliaries:\t\t'+'\n\t>> "to do":\t\t\t'+ str(DOcount)+'\t\t'+str(round(DOcount/wordcount,5))+'\n\t>> "to have":\t\t\t'+ str(HAVEcount)+'\t\t'+str(round(HAVEcount/wordcount,5))+'\n\t>> "to be": \t\t\t' +str(BEcount)+'\t\t'+str(round(BEcount/wordcount,5))+'\n\t>> "to get": \t\t\t' +str(GETcount)+'\t\t'+str(round(GETcount/wordcount,5))+'\n\t>> "Used to/Able to/Going to":\t' +str(Xtocount)+'\t\t'+str(round(Xtocount/wordcount,5))+'\n\t>> Auxiliary "need to": \t' +str(NeedTocount)+'\t\t'+str(round(NeedTocount/wordcount,5))+'\n "To" followed by verb:\t\t\t' +str(TOcount)+'\t\t'+str(round(TOcount/wordcount,5))+'\n Copulas\t\t'+'\n\t>> Prime copula "to be":\t' +str(BECOPcount)+'\t\t'+str(round(BECOPcount/wordcount,5))+'\n\t>> Secondary copulas:\t\t' +str(COPcount)+'\t\t'+str(round(COPcount/wordcount,5))+'\n Non-propositional tags:\t\t'+'\n\t>> (Proper)(Pers. Pro-)noun: \t' +str(Nouncount)+'\t\t'+str(round(Nouncount/wordcount,5))+'\n\t>> Particle: \t\t\t' +str(Particlecount)+'\t\t'+str(round(Particlecount/wordcount,5))+'\n\t>> Existential "There": \t' +str(EXcount)+'\t\t'+str(round(EXcount/wordcount,5))+'\n\t>> Foreign Word: \t\t' +str(FWcount)+'\t\t'+str(round(FWcount/wordcount,5))+'\n\t>> List item marker: \t\t' +str(LScount)+'\t\t'+str(round(LScount/wordcount,5))+'\n "a,an,the"-determiners:\t\t'+ str(DTcount)+'\t\t'+str(round(DTcount/wordcount,5))+'\n----------------------------------------------------------------------'+'\nDate of analysis:\t'+str(time.strftime("%Y-%m-%d %H:%M"))

	outputtext='statistics-'+inputtext
	output = open(outputtext,'wt')
	output.write(statistics)
	output.close()

	outputtext='Composition-'+inputtext
	output = open(outputtext,'wt')
	output.write(composition)
	output.close()

	proptext='tagged_propositions-'+inputtext
	propoutput = open(proptext,'wt')
	propoutput.write('Date of analysis:\t'+str(time.strftime("%Y-%m-%d %H:%M"))+'\n\nOriginal text:\n\t'+str(text)+'\n\nTagged propositional elements:\n\t'+str(taggedtext))
	propoutput.close()


IdeaDensity('Obama.txt')