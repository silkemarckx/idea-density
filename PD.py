import nltk
from nltk import word_tokenize, pos_tag
import re
from nltk.corpus import brown, ptb, treebank #http://www.nltk.org/howto/corpus.html


#1. tokenization & part-of-speech tagging --> normally Penn Treebank
f = open('obama.txt','rt', encoding='utf-8') #http://www.americanrhetoric.com/speeches/barackobama/barackobamawhitehousecorrespondentsdinner2016.htm
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
Punctuation = (',','.','!',';','?',':')
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

propcount= len(taggedtext)
#Removing positive modals from prop count.
#'Problem': Alle modals are removed. No problem: negative part carries the propositional count and is not removed. (otherwise: double count)
Modals = (('can', 'MD'),('Can', 'MD'),('could', 'MD'),('Could', 'MD'),('will', 'MD'),('Will', 'MD'),('would', 'MD'),('Would', 'MD'),('should', 'MD'),('Should', 'MD'),('may', 'MD'),('May', 'MD'),('might', 'MD'),('Might', 'MD'),('must', 'MD'),('Must', 'MD'))
for i in range((propcount)-5): 
	if not (taggedtext[i] is ("n't", 'RB') or taggedtext[i] is ('not', 'RB')): 
		if taggedtext[i-1] in Modals:
			taggedtext.remove(taggedtext[i-1])
			continue
	else:
		continue


print('Propositions -Modals: ',taggedtext)
propcount= len(taggedtext)
print('Proposition Count -modals: ', propcount)

#Removing 'To' in 'to+verb'
#Problem: Removes all 'to's!
#Problem: Only removes all 'To'(+verb) after second identical loop. (=Overall problem)
for i in range((propcount)-9):
	if taggedtext[i-1] == ('to', 'TO'): 
		for word in taggedtext[i]:
			#print(word,word[-2:])
			if word == 'VB':
				taggedtext.remove(taggedtext[i-1])
			else:
				continue
	else:
		continue
for i in range((propcount)-9): #removing 'to' bij 'to+verb' 
	if taggedtext[i-1] == ('to', 'TO'): 
		for word in taggedtext[i]:
			if word == 'VB':
				taggedtext.remove(taggedtext[i-1])
			else:
				continue
	else:
		continue

print('Propositions (-to): ',taggedtext)
propcount= len(taggedtext)
print('Proposition Count -to: ', propcount)

#Removing non-propositional tags + some determiners
#Problem: see overall problem. 2 identical loops needed
Removetags = ('NNP','NN','NNS','NNPS','PRP','RP','a','A','an','An','the','The','EX')
for word in taggedtext: #word= ('word','tag')
	if word[1] in Removetags:
		taggedtext.remove(word)
	elif word[0] in Removetags:
		taggedtext.remove(word)
	else:
		continue
for word in taggedtext: 
	if word[1] in Removetags:
		taggedtext.remove(word)
	elif word[0] in Removetags:
		taggedtext.remove(word)
	else:
		continue


print('Propositions -tags etc. : ',taggedtext)
propcount= len(taggedtext)
print('Proposition Count: ', propcount)

#5. Measuring PD (#prop./#words)
propdensity= propcount/wordcount
print('Propositional Idea Density: ',propdensity)