import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import string
import requests
import collections
import io
import tarfile
import urllib.request
import nltk
from nltk.corpus import stopwords

# Disable eager execution
tf.compat.v1.disable_eager_execution()

# Check and download NLTK stopwords if needed
try:
    stops = stopwords.words('english')
except LookupError:
    print("NLTK stopwords not found. Downloading...")
    nltk.download('stopwords')
    stops = stopwords.words('english')

sess = tf.compat.v1.Session()

batch_size = 50
embedding_size = 200
vocabulary_size = 10000
generations = 50000
print_loss_every = 500
num_sampled = int(batch_size/2)
window_size = 2
stops = stopwords.words('english')
print_valid_every = 2000
valid_words = ['cliche', 'love', 'hate', 'silly', 'sad']

# The rest of your script continues here...


def load_movie_data():
    save_folder_name = 'temp'
    pos_file = os.path.join(save_folder_name, 'rt-polarity.pos')
    neg_file = os.path.join(save_folder_name, 'rt-polarity.neg')
    
    # Check if files are already downloaded
    if not os.path.exists(save_folder_name):
        os.makedirs(save_folder_name)
    
    if not os.path.exists(pos_file) or not os.path.exists(neg_file):
        # If not downloaded, download and save 
        movie_data_url = 'http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz'
        stream_data = urllib.request.urlopen(movie_data_url)
        tmp = io.BytesIO()
        while True:
            s = stream_data.read(16384) 
            if not s:
                break
            tmp.write(s)
        stream_data.close()
        tmp.seek(0)
        tar_file = tarfile.open(fileobj=tmp, mode='r:gz')

        pos = tar_file.extractfile('rt-polaritydata/rt-polarity.pos')
        neg = tar_file.extractfile('rt-polaritydata/rt-polarity.neg')

        # Save pos/neg reviews
        pos_data = []
        for line in pos: 
            pos_data.append(line.decode('ISO-8859-1').encode('ascii', errors='ignore').decode())

        neg_data = []
        for line in neg: 
            neg_data.append(line.decode('ISO-8859-1').encode('ascii', errors='ignore').decode())

        tar_file.close()
        
        # Write to file
        with open(pos_file, 'w') as pos_file_handler: 
            pos_file_handler.write(''.join(pos_data))
        with open(neg_file, 'w') as neg_file_handler: 
            neg_file_handler.write(''.join(neg_data))
    
    texts = pos_data + neg_data 
    target = [1]*len(pos_data) + [0]*len(neg_data)
    
    return texts, target

texts, target = load_movie_data()

def normalize_text(texts, stops):
    # Lower case
    texts = [x.lower() for x in texts]
    
    # Remove punctuation
    texts = [''.join(c for c in x if c not in string.punctuation) for x in texts]
    
    # Remove numbers
    texts = [''.join(c for c in x if c not in '0123456789') for x in texts]
    
    # Remove stopwords
    texts = [' '.join([word for word in x.split() if word not in stops]) for x in texts]
    
    # Trim extra whitespace
    texts = [' '.join(x.split()) for x in texts]
    
    return texts

texts = normalize_text(texts, stops)
target = [target[ix] for ix, x in enumerate(texts) if len(x.split()) > 2]
texts = [x for x in texts if len(x.split()) > 2]

def build_dictionary(sentences, vocabulary_size):
    # Turn sentences (list of strings) into lists of words
    split_sentences = [s.split() for s in sentences]
    words = [x for sublist in split_sentences for x in sublist]
    # Initialize list of [word, word_count] for each word, starting with unknown count
    count = [['RARE', -1]]
    # Now add most frequent words, limited to the N-most frequent (N=vocabulary size)
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
    word_dict = {}
    # Now create the dictionary
    for word, word_count in count:
        word_dict[word] = len(word_dict)
    return word_dict

word_dictionary = build_dictionary(texts, vocabulary_size)
word_dictionary_rev = dict(zip(word_dictionary.values(), word_dictionary.keys()))

def text_to_numbers(sentences, word_dict):
    # Initialize the returned data
    data = []
    for sentence in sentences:
        sentence_data = []
        # For each word, either use selected index or rare word index
        for word in sentence:
            if word in word_dict:
                word_ix = word_dict[word]
            else:
                word_ix = 0
            sentence_data.append(word_ix)
        data.append(sentence_data)
    return data

text_data = text_to_numbers(texts, word_dictionary)

valid_examples = [word_dictionary[x] for x in valid_words]

valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

embeddings = tf.Variable(tf.random.uniform([vocabulary_size, embedding_size], -1.0, 1.0))

x_inputs = tf.compat.v1.placeholder(tf.int32, shape=[batch_size, 2*window_size])
y_target = tf.compat.v1.placeholder(tf.int32, shape=[batch_size, 1])
valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

embed = tf.zeros([batch_size, embedding_size])
for element in range(2*window_size):
    embed += tf.nn.embedding_lookup(embeddings, x_inputs[:, element])

nce_weights = tf.Variable(tf.random.normal([vocabulary_size, embedding_size],
                                           stddev=1.0 / np.sqrt(embedding_size)))
nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights,
                                     biases=nce_biases,
                                     labels=y_target,
                                     inputs=embed,
                                     num_sampled=num_sampled,
                                     num_classes=vocabulary_size))

optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)

norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
normalized_embeddings = embeddings / norm

valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
similarity = tf.matmul(valid_embeddings, normalized_embeddings, transpose_b=True)

init = tf.compat.v1.global_variables_initializer()
sess.run(init)

loss_vec = []
loss_x_vec = []

for i in range(generations):
    batch_indices = np.random.choice(len(text_data), size=batch_size)
    batch_inputs = [text_data[ix] for ix in batch_indices]
    batch_target = [target[ix] for ix in batch_indices]

    feed_dict = {x_inputs: batch_inputs, y_target: np.array(batch_target).reshape(-1, 1)}

    sess.run(optimizer, feed_dict=feed_dict)

    if (i+1) % print_loss_every == 0:
        loss_val = sess.run(loss, feed_dict=feed_dict)
        loss_vec.append(loss_val)
        loss_x_vec.append(i+1)
        print("Loss at step {} : {}".format(i+1, loss_val))

    if (i+1) % print_valid_every == 0:
        sim = sess.run(similarity, feed_dict=feed_dict)
        for j in range(len(valid_words)):
            valid_word = word_dictionary_rev[valid_examples[j]]
            top_k = 5
            nearest = (-sim[j, :]).argsort()[1:top_k+1]
            log_str = "Nearest to {} :".format(valid_word)
            for k in range(top_k):
                close_word = word_dictionary_rev[nearest[k]]
                log_str = "{} {}".format(log_str, close_word)
            print(log_str)

