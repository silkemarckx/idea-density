import nltk
from nltk import word_tokenize, pos_tag
import re
from nltk.corpus import brown, ptb #http://www.nltk.org/howto/corpus.html


#1. tokenization & part-of-speech tagging --> normally Penn Treebank
f = open('obama.txt','rt', encoding='utf-8') #http://www.americanrhetoric.com/speeches/barackobama/barackobamawhitehousecorrespondentsdinner2016.htm
text=f.read()
tokenized= re.split(r'\W+', text)
tokenized= word_tokenize(text)
print(pos_tag(tokenized))

brown_tagged_sents = brown.tagged_sents(categories='news')
unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
print(unigram_tagger.tag(tokenized))

#2. Total word count --> Multiplication: no words!

#3. Adjustment Rules
""" 'either...or' = 1 prop.
'to'+verb = 1 prop
'a,an,the' =/ prop
models =/ prop, UNLESS negative (ending in "n't")
COPULA + NP ==> copula = prop 
COPULA + AdjP ==> copula(linking verb) =/ prop  (AdjP=prop!)
Remove subject-auxiliary inversion"""

#4. Proposition count
"""= verbs
+adjectives
+adverbs
+prepositions
+conjunctions
+determiners (-a,an,the)
+modals (ONLY if negative)
-auxiliary verbs
-linking verbs """
#5. Measuring PD (#prop./#words)