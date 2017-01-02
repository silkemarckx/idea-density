import nltk
from nltk import word_tokenize, pos_tag
import re
from nltk.corpus import brown, ptb, treebank #http://www.nltk.org/howto/corpus.html

def IdeaDensity(inputtext):
	#1. tokenization & part-of-speech tagging --> normally Penn Treebank
	f = open(inputtext,'rt', encoding='utf-8') #http://www.americanrhetoric.com/speeches/barackobama/barackobamawhitehousecorrespondentsdinner2016.htm
	text=f.read()
	f.close()
	#tokenized= re.split(r'\W+', text)

	tokenized= word_tokenize(text)
	taggedtext = pos_tag(tokenized)
	print('Tagged text: Original',taggedtext)


	#2. Total word count --> Multiplication: no words!

	#Deleting punctuation
	#Problem: Only removes all punctuation after a second identical loop. 
	#=> OVERALL PROBLEM: 2 items with same tag: No removal of second item!!
	Punctuation = (',','.','!',';','?',':',"'")
	for word in taggedtext:
		#regexp= re.compile(r'\,|\.|\;') PROBLEM!
		if word[0] in Punctuation:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext:
		if word[0] in Punctuation:
			taggedtext.remove(word)
		else:
			continue

	wordcount = len(taggedtext)
	print('wordcount: ',wordcount)


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
	COPULA + AdjP ==> copula(linking verb) =/ prop  (AdjP=prop!)
	Remove subject-auxiliary inversion"""

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
	propcount=(len(taggedtext))
	for i in range(1,(propcount)-1):
		if taggedtext[i] == ('to', 'TO'): 
			if taggedtext[i-1] == ('got', 'VBN'):
				#print(taggedtext[i-1],taggedtext[i])
				taggedtext.remove(taggedtext[i-1])
			else:
				continue
		else:
			continue

	ModalNeed= (('need', 'VB'),('Need', 'VB'),('need', 'VBP'),('Need', 'VBP'), ('need', 'MD'),('needed', 'VBD'),('Needed', 'VBD'))
	Negative= (("n't", 'RB'),('not', 'RB'))
	for i in range(1,(len(taggedtext))-5): 
		if taggedtext[i-1] in ModalNeed: 
			if taggedtext[i] != ('to', 'TO'): #Following the original grammar rules: need + to = main verb, instead of semi-modal
				if taggedtext[i] in Negative:
					#print('NOT',taggedtext[i-2],taggedtext[i],len(taggedtext))
					taggedtext.remove(taggedtext[i-1])
				else:
					for word in taggedtext[i]:
						if word == 'VB':
							#print('LAST',taggedtext[i-1],taggedtext[i],len(taggedtext))
							taggedtext.remove(taggedtext[i-1])
						else:
							continue
					for word in taggedtext:
						if word == ('Need', 'VB'): #only modal need can initiate a sentence
							#print('Beginning', word)
							taggedtext.remove(word)
						else:
							continue
			else:
				continue
		else:
			continue
	for i in range(1,(len(taggedtext))-6): 
		if taggedtext[i-1] in ModalNeed: 
			if taggedtext[i] != ('to', 'TO'): 
				for word in taggedtext[i+1]: #problem: '... need her. Do' --> need=removed!
					if word == 'VB':
						#print('LAST',taggedtext[i+1],len(taggedtext))
						taggedtext.remove(taggedtext[i-1])
					else:
						continue
			else:
				continue
		else:
			continue

	#removing aux 'used/able/going to', not a MODAL! (but must be removed before 'to' is removed)
	beXto = (('used', 'VBD'),('going', 'VBG'),('able', 'JJ'))
	for i in range(1,(len(taggedtext))-2): 
		if taggedtext[i-1] in beXto: 
			if taggedtext[i] == ('to', 'TO'):
				for word in taggedtext[i+1]:
					if word == 'VB':
						taggedtext.remove(taggedtext[i-1])
			else:
				continue			
		else:
			continue
	

	print('Propositions -Modals: ',taggedtext)
	propcount= len(taggedtext)
	print('Proposition Count -modals: ', propcount)

	#Removing 'To' in 'to+verb'
	#Problem: Only removes all 'To'(+verb) after second identical loop. (=Overall problem)
	for i in range(1,(len(taggedtext))-10):
		if taggedtext[i-1] == ('to', 'TO'): 
			for word in taggedtext[i]:
				if word == 'VB':
					#print(taggedtext[i])
					taggedtext[i-1]="I need to rename this, in order to avoid removing al TO's"
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue
	print(taggedtext)
	for i in range(1,(len(taggedtext))-3): #removing 'to' bij 'to+verb' 
		if taggedtext[i-1] == ('to', 'TO'): 
			for word in taggedtext[i]:
				if word == 'VB':
					#print(taggedtext[i-1],taggedtext[i])
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			#print(taggedtext[i],len(taggedtext))
			continue

	print('Propositions (-to): ',taggedtext)
	propcount= len(taggedtext)
	print('Proposition Count -to: ', propcount)

	#Removing auxiliary verbs
	#Problem: sentences like 'Why did you tell her that...' --> 'did' is NOT removed
	propcount= len(taggedtext)
	AuxDO= (('do', 'VBP'),('Do', 'VBP'),('does', 'VBZ'),('Does', 'VBZ'),('did', 'VBD'),('Did', 'VBD'))
	FollowingAux = (("n't", 'RB'),('not', 'RB'),('been', 'VBN'))
	for i in range(1,(propcount)-1): 
		if taggedtext[i] in FollowingAux: 
			if taggedtext[i-1] in AuxDO:
				#print(taggedtext[i-1],taggedtext[i])
				taggedtext.remove(taggedtext[i-1])
		else:
			continue
	for word in taggedtext: #removing do-verbs that initate a sentence.
		if (word == ('Do','VBP') or word == ('Does', 'VBZ')):
			#print(word)
			taggedtext.remove(word)
	propcount= len(taggedtext)
	print('Proposition Count -DO: ', propcount)


	AuxHAVE= (('have', 'VBP'),('Have', 'VBP'),('has', 'VBZ'),('Has', 'VBZ'),("'ve", 'VBP'),
		('had', 'VBD'),('Had', 'VBD'),('have', 'VB'))
	FolHAVE=('VB','VBN')
	for i in range(1,(len(taggedtext))-5): 
		if taggedtext[i] in FollowingAux: 
			if taggedtext[i-1] in AuxHAVE:
				#print(taggedtext[i-1],taggedtext[i])
				taggedtext.remove(taggedtext[i-1])
		elif taggedtext[i-1] in AuxHAVE: 
			for word in taggedtext[i]:
				if word in FolHAVE:
					#print(taggedtext[i-1],taggedtext[i])
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
			for word in taggedtext[i+1]:
				if word in FolHAVE:
					#print(taggedtext[i-1],taggedtext[i+1])
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue
	propcount= len(taggedtext)
	print('Proposition Count -HAVE: ', propcount)


	AuxBE= (('am', 'VBP'),('Am', 'VBP'),("'m", 'VBP'),('are', 'VBP'),('Are', 'VBP'),("'re", 'VBP'),
		('is','VBZ'),('Is','VBZ'),("'s",'VBZ'),('was','VBD'),('Was','VBD'),('were','VBD'),
		('Were','VBD'),('been','VBN'),('Been','VBN'),('being','VBG'),('Being','VBG'),('be', 'VB'))
	FolBE= ('VBG','VBN','VB') #VB --> Modal 'be to +verb', 'to' is already removed, so: be+ verb (& verb = VB)
	for i in range(1,(len(taggedtext))-8): 
		if taggedtext[i-1] in AuxBE:
			for word in taggedtext[i]:
				if word in FolBE:
					#print('FIRST',taggedtext[i-1],taggedtext[i])
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
			for word in taggedtext[i+1]:
				if word in FolBE:
					#print('MIDDLE',taggedtext[i-1],taggedtext[i+1])
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		if taggedtext[i-1] in AuxBE: #without repetition of if-clause: removal of wrong word!!
			for word in taggedtext[i+2]:
				if word in FolBE:
					#print('LAST',taggedtext[i-1],taggedtext[i+2])
					taggedtext.remove(taggedtext[i-1])
				else:
					continue
		else:
			continue

	AuxGET = (('get', 'VBP'), ('gets', 'VBZ'),('got', 'VBD'))
	for i in range(1,(len(taggedtext))-5): 
		if taggedtext[i-1] in AuxGET:
			for word in taggedtext[i]:
				if word == 'VBN':
					#print('FIRST',taggedtext[i-1],taggedtext[i])
					taggedtext.remove(taggedtext[i-1])

	print('Propositions -aux: ',taggedtext)
	propcount= len(taggedtext)
	print('Proposition Count -AUX: ', propcount)

	#Removing copula, followed by AdjP


	#Removing non-propositional tags + some determiners
	#Problem: see overall problem. 3 identical loops needed!!
	Removetags = ('NNP','NN','NNS','NNPS','PRP','RP','EX')
	RemoveDT= ('a','A','an','An','the','The')
	for word in taggedtext: #word= ('word','tag')
		if word[1] in Removetags:
			taggedtext.remove(word)
		elif word[0] in RemoveDT:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext: 
		if word[1] in Removetags:
			taggedtext.remove(word)
		elif word[0] in RemoveDT:
			taggedtext.remove(word)
		else:
			continue
	for word in taggedtext: 
		if word[1] in Removetags:
			taggedtext.remove(word)
		elif word[0] in RemoveDT:
			taggedtext.remove(word)
		else:
			continue

	print('Propositions -tags etc. : ',taggedtext)
	propcount= len(taggedtext)
	print('Proposition Count: ', propcount)

	#5. Measuring PD (#prop./#words)
	propdensity= propcount/wordcount
	print('Propositional Idea Density: ',propdensity)

IdeaDensity('testtext.txt')