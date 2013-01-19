# Contains all the code for preprocessing a tweet.
import re

class Preprocess:
	stop_words = []
	processed_data = []
	seeds = {}

	def createZone(self, data):
		spliters = [',', '!', '.', '?', ';', '(', ')']
		zones = [data.lower()]
		temp_zones = []
		#print "\n\n\n\nCreating zones in Tweet..."
		for base in spliters:
			for zone in zones:
				if zone != '':
					temp_zones += [z.strip() for z in zone.split(base)]
			zones = temp_zones
			temp_zones = []
		#print zones
		return zones
	
	def findPhrase(self, zones):
		negative_reg = [r'\snot\s.+', r'n\'t\s']#, r'\snever\s', r'\sno\s']
		phrases = []
		#print "\nFinding phrase..."
		for zone in zones:
			i = 0
			for negative in negative_reg:
				if zone.split() == []:
					continue
				if re.findall(negative, zone, re.I|re.M) != [] or zone.split()[0] == 'not':
					possible_phrases = zone.split(self.negatives[i])
					j = 0
					phrase = ' '
					for possible_phrase in possible_phrases:
						j += 1
						if j == 1 or possible_phrase == '':
							continue
						phrases.append(phrase.join(possible_phrase.strip().split()[0:3]))
				i += 1
		#print phrases
		return phrases
	
	def findQuotedString(self, tweet):
		#print "\n\nFinding quoted string in the tweet"
		tweet = tweet['tweet'].lower()
		quotes = re.search(r"(^|\s)(\'|\")*.*?(\2)(?!s)", tweet)
		processed_tweet = re.sub(r"(^|\s)(\'|\")*.*?(\2)(?!s)", " MOVIE_NAME_OR_QUOTE", tweet)
		#try:
			#print "**Found quote or movie name **: " + quotes.group()
		#except:
		#	pass
		
		#print processed_tweet
		return processed_tweet

	def removeMoviename(self, data, movie_name):
		reg = re.compile(movie_name, re.M|re.I)
		data = re.sub(reg, 'MOVIE_NAME_OR_QUOTE', data)
		return data

		
	def removeStopWords(self, phrases):
		if self.method == 'basic':
			return
		
		elif self.method == 'zagibolov':
			i = 0
			for phrase in phrases:
				for stop_word in self.stop_words:
					phrase = stop_word.sub(' ', phrase).strip()
				phrases[i] = phrase
				i += 1
			#print phrases
			return phrases
		
	def removeChars(self, phrases):
		i = 0
		for phrase in phrases:
			phrase = re.sub(r'[^\x20-\x7e]', '', phrase)
			phrases[i] = re.sub(r'\\u(\d|[a-f]){4}', '',phrase).strip()
			i += 1
		#print phrases
		return phrases

	def removeLinks(self, data):
		#print "Removing links"
		reg = r'http(s)?:\/\/(www\.)?[\w\d\.\-\/]+(\s|$)'
		cleared = re.sub(reg, '', data).strip()
		#print cleared
		return cleared

	def removeTag(self, data):
		#print "Removing Tags"
		reg = r'@[\w\d]+'
		cleared = re.sub(reg, '', data).strip()
		#print cleared
		return cleared

	def removeHashTag(self, data):
		#print "Removing Hashtag"
		reg = r'#[\d\w]+'
		cleared = re.sub(reg, '', data).strip()
		#print cleared
		return cleared

	def Preprocess(self, phrases):
		#print "\nPreprocessing...."
		#print "Removing stop words..."
		phrases = self.removeStopWords(phrases)
		#print "Removing unicode and hexadecimals."
		phrases = self.removeChars(phrases)
		return phrases

	def preprocess(self, data):
		#if self.method == 'basic':
		#	self.basicScoring(data)
		if self.method == 'zagibolov':
			self.Zagibolov(data)
		else:
			print "No scoring measure named: %s." % method
			
	
	def Zagibolov(self, data):
		processed_tweet = self.findQuotedString(data) #not complete yet but still functional.
		processed_tweet = self.removeMoviename(processed_tweet, data['movie_name'])
		processed_tweet = self.removeLinks(processed_tweet)
		processed_tweet = self.removeHashTag(processed_tweet)
		processed_tweet = self.removeTag(processed_tweet)
		#print processed_tweet
		zones = self.createZone(processed_tweet)
		phrases = self.findPhrase(zones)
		processed_phrases = self.Preprocess(phrases)
		if processed_phrases is not None:
			for lexical_seed in processed_phrases:
				if lexical_seed != '':
					lex = lexical_seed.strip(' )}]').encode('ascii')
					if lex == 'movie':
						continue
					if lex not in self.lexicons.keys():
						self.lexicons[lex] = 1
						self.seeds[lex] = {'negative': 1, 'positive': -1}
					else:
						self.seeds[lex]['negative'] += 1
						self.seeds[lex]['positive'] -= 1

	def preprocessScoring(self, data):
		processed_tweet = self.findQuotedString(data) #not complete yet but still functional.
		processed_tweet = self.removeMoviename(processed_tweet, data['movie_name'])
		processed_tweet = self.removeLinks(processed_tweet)
		processed_tweet = self.removeHashTag(processed_tweet)
		processed_tweet = self.removeTag(processed_tweet)
		tweet = self.removeStopWords([processed_tweet])[0]
		self.processed_data.append({'tweet_id': data['tweet_id'], 'tweet': tweet, 'movie_name': data['movie_name']})

	def processLexicon(self):
		for seed in self.seeds.keys():
			if self.seeds[seed]['positive'] < 0 or self.seeds[seed]['positive'] - self.seeds[seed]['negative'] <= 0:
				del self.seeds[seed]
				del self.lexicons[seed]
		

	def __init__(self, method, lexicons, negatives, stop_words):
		self.method = method
		self.lexicons = lexicons
		self.negatives = negatives
		for stop_word in stop_words:
			self.stop_words.append(re.compile("(^"+stop_word+"\s|\s"+stop_word+"\s|\s"+stop_word+"$|^"+stop_word+"$|"+stop_word+"\))"))