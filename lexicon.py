# This file picks the sentiment words from the word sentiment file and also has the global variable lexicon which is used for storing lexicons.
class Lexicon:
	lexicons = {}
	adverbs = []
	def getLexiconsFromPN(self):			
		fp = open('positive.txt', 'r')
		line = fp.readline()
		while line:
			self.lexicons[line.strip()] = 1
			line = fp.readline()
		fp = open('negative.txt', 'r')
		line = fp.readline()
		while line:
			self.lexicons[line.strip()] = -1
			line = fp.readline()
			
	def getLexiconsFromSentiment(self):	
		fp = open('sentiments.tff', 'r')
		line = fp.readline()
		while line:
			lexicon = line.split()
			lex_type = (lexicon[0].split('='))[1]
			lex_word = (lexicon[2].split('='))[1]
			lex_pos = (lexicon[3].split('='))[1]
			lex_stemmed = (lexicon[4].split('='))[1]
			lex_polarity = (lexicon[5].split('='))[1]
			
			if lex_pos == 'adverb':
				self.adverbs.append(lex_word)
			
			if lex_type == 'strongsubj' and lex_polarity == 'positive':
				self.lexicons[lex_word] = 1
			elif lex_type == 'strongsubj' and lex_polarity == 'negative':
				self.lexicons[lex_word] = -1
			elif lex_type == 'weaksubj' and lex_polarity == 'positive':
				self.lexicons[lex_word] = 0.5
			elif lex_type == 'weaksubj' and lex_polarity == 'positive':
				self.lexicons[lex_word] = -0.5
			line = fp.readline()