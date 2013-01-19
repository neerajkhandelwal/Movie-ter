# Contains the scoring mechanism, zagibolov and basic(has not been used for a long time).
from preprocess import Preprocess
import re

class Scoring(Preprocess):
	method = ''
	lexicons = {}
	lexicon_count = {}
	negatives = []
	stop_words = []
	
	def __init__(self, method, lexicons, negatives, stop_words, lexicon_count):
		self.method = method
		self.lexicons = lexicons
		self.negatives = negatives
		self.lexicon_count = lexicon_count
		for stop_word in stop_words:
			self.stop_words.append(re.compile("(^"+stop_word+"\s|\s"+stop_word+"\s|\s"+stop_word+"$|^"+stop_word+"$)"))
		
	def count(self, data):
		# if self.method == 'basic':
		# 	self.basicScoring(data)
		if self.method == 'zagibolov':
			#negative_found = self.Zagibolov_negative(data)
			self.Zagibolov_positive(data)
		else:
			print "No scoring measure named: %s." % method
			
	# def basicScoring(self, data):
	# 	score = 0
	# 	found = False
	# 	for token in self.findQuotedString(data).split():#data['tweet'].split():
	# 		try: 
	# 			if token == 'not' or found:
	# 				score -= self.lexicons[token.lower()]
	# 				found = True
	# 			else:
	# 				score += self.lexicons[token.lower()]
	# 		except:
	# 			pass
	# 	print "%s --------- Score:%s" % (data['tweet'], score)
		
	
	# def Zagibolov_negative(self, data):
	# 	for lexicon in self.lexicons:
	# 		if lexicon == 'movie':
	# 			continue
	# 		reg = re.compile(lexicon, re.M|re.I)
	# 		negative_found = len(re.findall(reg, tweet))
	# 		if lexicon not in self.lexicon_count.keys():
	# 			self.lexicon_count[lexicon] = {'positive': 0, 'negative': negative_found}
	# 		else:
	# 			self.lexicon_count[lexicon]['negative'] += negative_found
	# 		return negative_found

	#scoring need to be fixed.
	def score(self, data):
		zones = self.createZone(data['tweet'])
		score = 0
		seeds_found = []
		#print str(data['tweet_id']) + data['tweet'], zones, '\n'
		for zone in zones:
			zone_words = zone.split()
			if len(re.findall(r'n\'t\s', zone, re.M|re.I)) > 0:
				ni = -1
			else:
				ni = 1
			for seed in self.lexicons.keys():	
				reg = re.compile(seed, re.I|re.M)
				found = re.findall(reg, zone)
				if len(found) > 0 and seed not in seeds_found:
					seeds_found.append(seed)
				for f in found:
					#print f + str(self.lexicons[seed] / float(len(zone_words)))
					#loop on it for negative words...!
					if 'not' in zone_words:
						#print zone_words
						ni = ni * -1
					else:
						ni = ni * 1
					score += (self.lexicons[seed] / float(len(zone_words))) * ni

		for s in seeds_found:
			if score >= 0:
				self.lexicon_count[s]['positive'] += 1
			else:
				self.lexicon_count[s]['negative'] += 1

		data['score'] = score
		if score >= 0 :
			data['sentiment'] = 'positive'
		else:
			data['sentiment'] = 'negative'
		print str(data['tweet_id']) + data['tweet'] + " score of tweet ###" + str(score)
		#print score
		return score

	def Zagibolov_positive(self, data):
		for lexicon in self.lexicons:
			if lexicon == 'movie':
				continue
			reg = re.compile(lexicon, re.M|re.I)
			# if lexicon not in self.lexicon_count.keys():
			# 	self.lexicon_count[lexicon] = {'positive': 0, 'negative': 0}
			# else:
			self.lexicon_count[lexicon]['positive'] += (len(re.findall(reg, data)))

	def adjustScoring(self):
		for seed in self.lexicons:
			fp = self.lexicon_count[seed]['positive']
			fn = self.lexicon_count[seed]['negative']
			if fp > 0 or fn > 0:
				#2*|Fp - Fn|/(Fp+Fn) > 1
				num = 2*abs(fp - fn)
				den = float(fp + fn)

				if num/den > 1:
					self.lexicons[seed] = fp - fn

	def resetLexiconCount(self):
		for lex in self.lexicon_count.keys():
			self.lexicon_count[lex]['positive'] = 0
			self.lexicon_count[lex]['negative'] = 0