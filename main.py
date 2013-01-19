# Main file
from scoring import Scoring
from corpus import Corpus
from lexicon import Lexicon
from preprocess import Preprocess

class Project:
    lexicons = {}
    corpus = []     
    negatives = []
    
    def generateCorpus(self, c_type = 'not'):
        corpus = Corpus(password='', db='project_major')
        if c_type == 'not':
            corpus.getTweetsWithNot()
        else:
            corpus.getTweets()
        self.corpus = corpus.dataSet
        self.negatives = corpus.negatives
        self.stopWords = corpus.stopWords
        corpus.close()
        
    def getLexicons(self, l_type='Senti'):
        lexicon = Lexicon()
        if l_type == 'Senti':
            lexicon.getLexiconsFromSentiment()
        elif l_type == 'PN':
            lexicon.getLexiconsFromPN()
        self.lexicons = lexicon.lexicons
    
    def preprocessing(self, method='zagibolov'):
        preprocess = Preprocess(method, self.lexicons, self.negatives, self.stopWords)
        for data in self.corpus:
            preprocess.preprocess(data)
            lexicons = preprocess.lexicons
            self.lexicons = dict(self.lexicons.items() + lexicons.items())
        self.seeds = preprocess.seeds

    def scoring(self, method='zagibolov'):
        # Supply argument in Corpus to connect to databse. user, password and db.
        corpus = Corpus(password='', db='project_major')
        corpus.getTweets()
        dataset = corpus.dataSet
        preprocess = Preprocess('zagibolov', self.lexicons, self.negatives, self.stopWords)
        scoring = Scoring(method, self.lexicons, self.negatives, self.stopWords, self.seeds)
        j = 0
        for data in dataset:
            preprocess.preprocessScoring(data)
            processed = preprocess.processed_data
            
        for data in processed:
            scoring.count(data['tweet'])
    ##        print self.seeds
        preprocess.seeds = scoring.lexicon_count
        preprocess.processLexicon()
        scoring.lexicons = preprocess.lexicons
    ##        print scoring.lexicon_count
        last_score = {}
        i = 0
        for i in range(0,3):
            total = 0
            j = 0
            negative = 0
            positive = 0
            scoring.resetLexiconCount()
    ##        print self.lexicons
            for data in processed:
                if j == 50:
                    break
                j += 1
                score = scoring.score(data)
                if score != 0:
                    total += 1
                    if score < 0:
                        negative += 1
                    else:
                        positive += 1
            scoring.adjustScoring()
            if last_score == {}:
                last_score = scoring.lexicons
                this_score = last_score
            else:
                this_score = scoring.lexicons
                if this_score == last_score:
                    break
                else:
                    last_score = this_score
            print this_score
            print "Total scored: " + str(total), "Negative: ", negative, "Positive: ", positive
        print this_score
        print "Total scored: " + str(total), "Negative: ", negative, "Positive: ", positive

def main():
    prjct = Project()
    prjct.generateCorpus('not')
    #prjct.getLexicons()
    #prjct.score()
    #print prjct.corpus
    #prjct.generateCorpus('not')
    #prjct.getLexicons('PN')
    prjct.preprocessing()
    prjct.scoring()
    
    
    
if __name__ == '__main__':
    main()
