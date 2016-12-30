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
print('Tagged text: ',taggedtext)


#2. Total word count --> Multiplication: no words!

#Deleting punctuation
for word in taggedtext:
	#regexp= re.compile(r'\,|\.|\;') PROBLEM!
	if word[1] == '.':
		taggedtext.remove(word)
	elif word[1] == ',':
		taggedtext.remove(word)
	else:
		continue

wordcount = len(taggedtext)
print('wordcount: ',wordcount)


#3. Proposition count
"""= verbs
+adjectives
+adverbs
+prepositions
+conjunctions
+determiners (-a,an,the)
+modals (ONLY if negative)
-auxiliary verbs
-linking verbs """

for word in taggedtext: #word= ('word','tag')
	regex= r'NNP'  #problem: fitting NN,NNP,NNS,... in 1 regex
	if word[1] == regex:
		taggedtext.remove(word)
	elif word[1] == 'NN':
		taggedtext.remove(word)
	elif word[1] == 'NNS':
		taggedtext.remove(word)
	elif word[1] == 'NNPS':
		taggedtext.remove(word)
	elif word[1] == 'PRP':
		taggedtext.remove(word)
	elif word[1] == 'RP':
		taggedtext.remove(word)
	elif word[0] == 'a': #--> same problem for DT
		taggedtext.remove(word)
	elif word[0] == 'an':
		taggedtext.remove(word)
	elif word[0] == 'the':
		taggedtext.remove(word)
	elif word[1] == 'EX':
		taggedtext.remove(word)

#PROBLEM: DOES NOT REMOVE EVERY 'NN', 'NNP', etc!!??

#4. Adjustment Rules
""" 'either...or' = 1 prop.
'to'+verb = 1 prop
'a,an,the' =/ prop
models =/ prop, UNLESS negative (ending in "n't")
COPULA + NP ==> copula = prop 
COPULA + AdjP ==> copula(linking verb) =/ prop  (AdjP=prop!)
Remove subject-auxiliary inversion"""

"""for i in range(1,len(taggedtext)):
	print(taggedtext[i], taggedtext[i-1])
	"""

"""for i in range(1,(len(taggedtext))): #removing positive modals ---> PROBLEM: list index out of range
	if taggedtext[i] is not ("n't", 'RB'): 
		if taggedtext[i] is not ('not', 'RB'):
			if taggedtext[i-1] == ('can', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i-1] == ('could', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i-1] == ('should', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i-1] == ('would', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i-1] == ('should', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i-1] == ('must', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			elif taggedtext[i-1] == ('might', 'MD'):
				taggedtext.remove(taggedtext[i-1])
			else:
				continue
		else:
			break
	else:
		continue"""


print('Propositions: ',taggedtext)
propcount= len(taggedtext)
print('Proposition Count: ', propcount)

#5. Measuring PD (#prop./#words)
propdensity= propcount/wordcount
print('Propositional Idea Density: ',propdensity)