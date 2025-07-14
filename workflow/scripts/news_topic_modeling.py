import pandas as pd
import gensim
from gensim import corpora
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Load and clean data
df = pd.read_csv('data/clean/google_news_clean.csv')
texts = df['clean_title'].dropna().tolist()

# Tokenize and remove stopwords
stops = set(stopwords.words('english'))
texts = [[word for word in t.split() if word not in stops and len(word) > 2] for t in texts]

# Build dictionary and corpus
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# LDA Topic Modeling (adjust num_topics if you want)
lda = gensim.models.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=15, random_state=42)

topics = lda.print_topics(num_words=8)
print("Google News Top Topics (LDA):\n")
for i, topic in topics:
    print(f"Topic {i+1}: {topic}")
