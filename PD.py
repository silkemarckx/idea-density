import nltk
from nltk import word_tokenize, pos_tag
import re
from nltk.corpus import brown, ptb #http://www.nltk.org/howto/corpus.html


#Brief overview
#1. tokenization
f = open('obama.txt','rt', encoding='utf-8') #http://www.americanrhetoric.com/speeches/barackobama/barackobamawhitehousecorrespondentsdinner2016.htm
text=f.read()
tokenized= re.split(r'\W+', text)
tokenized= word_tokenize(text)
print(pos_tag(tokenized))

brown_tagged_sents = brown.tagged_sents(categories='news')
unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
print(unigram_tagger.tag(tokenized))
#2. Total word count
#3. Part of speech tagger
#4. Rules
#5. Measuring PD