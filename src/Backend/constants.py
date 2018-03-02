import inflect
from nltk import word_tokenize
from nltk.corpus import stopwords


ES_HOSTNAME = 'http://localhost:9222/'  # port of the local host
# Elastic Search commoncrawl2 search request
CRAWL_DATA_REPOS = 'commoncrawl2/_search?q=text:'


# list of all positive markers used for comparing the objects
POSITIVE_MARKERS = ['better', 'easier', 'faster', 'nicer', 'cooler', 'safer', 'superior to',
                    'more accessible', 'greater', 'simpler', 'smoother', 'lighter', 'quicker',
                    'friendlier', 'less complicated', 'more recommended', 'more experienced',
                    'smarter', 'cleverer', 'more intuitive', 'more secure', 'finer']
# list of all negative markers used for comparing the objects
NEGATIVE_MARKERS = ['worse', 'harder', 'slower', 'poorer', 'inferior to', 'more complicated',
                    'less accessible', 'less recommended', 'less experienced', 'less intuitive',
                    'less secure']
# list of all positive and negative markers with than used for comparing the objects
MARKERS_THAN = ['better', 'easier', 'faster', 'nicer', 'cooler', 'safer', 'worse', 'harder',
                'slower', 'poorer', '\'more accessible\'', 'greater', 'simpler', 'smoother',
                '\'more complicated\'', 'lighter', 'quicker', 'friendlier', '\'less accessible\'',
                '\'less complicated\'', '\'more recommended\'', '\'more experienced\'',
                '\'less experienced\'', 'smarter', 'cleverer', '\'more intuitive\'',
                '\'less intuitive\'', '\'more secure\'', '\'less secure\'', 'finer']
# list of all positive and negative markers without than used for comparing the objects
MARKERS_WO_THAN = ['\'superior to\'', '\'inferior to\'']
# sentences containing a negation between the objects will have their result reversed
NEGATIONS = ['didn\'t', 'couldn\'t', 'wasn\'t', 'haven\'t', 'wouldn\'t', 'can\'t',
             'did not', 'could not', 'was not', 'have not', 'would not', 'can not',
             'didnt', 'couldnt', 'wasnt', 'havent', 'wouldnt', 'cannot']
# sentences containing one of these markers will have their result reversed
OPPOSITE_MARKERS = ['not', 'no', 'nor']
STOPWORDS = set(stopwords.words('english'))
# words in this list aren't considered to be interesting for the list of linked words
NON_LINKS = ['come', 'much', 'good', 'even', 'think', 'would', 'make', 'yes', 'get', 'well',
             'like', 'also', 'nice', 'great', 'made', 'could', 'some']
# number words like 'one' aren't considered to be interesting for the list of linked words
NUMBER_STRINGS = []
p = inflect.engine()
for i in range(0, 1000):
    NUMBER_STRINGS.append(p.number_to_words(i))