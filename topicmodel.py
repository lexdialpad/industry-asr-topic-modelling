import os
os.environ["TOKENIZERS_PARALLELISM"] = "false" 
import spacy
import string
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bertopic import BERTopic
from nltk.corpus import stopwords
nltk.download("stopwords")

nlp = spacy.load("en_core_web_sm")

# Create a list of transcript texts 
directory = "/Users/lexkonnelly/Documents/Projects/OKR 2.1 Industry ASR/transcript_text_files"
documents = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            documents.append(file.read())

# Initialize stopwords
stop_words = set(word.strip().lower() for word in stopwords.words("english"))
with open('custom_stopwords.txt', 'r') as file:
    custom_stopwords = set(line.strip().lower() for line in file.readlines())
stop_words.update(custom_stopwords)

def preprocess_document(doc):
    # Convert texts to lowercase, remove punctuation
    doc = doc.lower()
    doc = doc.translate(str.maketrans("", "", string.punctuation))
    doc_spacy = nlp(doc)
    
    # Lemmatize, remove stopwords, and rejoin to a single string
    words = [token.lemma_ for token in doc_spacy if token.is_alpha and token.lemma_.lower() not in stop_words]
    return " ".join(words)

preprocessed_documents = [preprocess_document(doc) for doc in documents]

# Initialize BERTopic and fit the model
topic_model = BERTopic(min_topic_size=50, nr_topics=10)
topics, _ = topic_model.fit_transform(preprocessed_documents)

# Filter to exclude any outliers
valid_topic_indices = [i for i, topic in enumerate(topics) if topic != -1]
filtered_documents = [preprocessed_documents[i] for i in valid_topic_indices]
filtered_topics = [topics[i] for i in valid_topic_indices]

# Save the intertopic distance visualization to an HTML file
topic_model.visualize_topics().write_html("topic_map.html")
print("Intertopic distance map saved.")

# Save the topic distribution to an HTML file
filtered_topic_info = topic_model.get_topic_info()
filtered_topic_info = filtered_topic_info[filtered_topic_info["Topic"] != -1]
filtered_topic_info.to_html('topic_distribution.html')
print("Topic distribution saved.")

# Generate word clouds with the top frequency words in each topic
topic_words = topic_model.get_topics()
output_dir = "wordclouds"
os.makedirs(output_dir, exist_ok=True)

for topic_id, words in topic_words.items():
    if topic_id == -1:  
        continue
    word_freq = {word: weight for word, weight in words}
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    
    file_path = os.path.join(output_dir, f"topic_{topic_id}_wordcloud.png")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Topic {topic_id}")
    plt.savefig(file_path, format="png")
    plt.close()
    
print("Word clouds saved to 'wordclouds' directory.")
print("Topic modeling complete.")