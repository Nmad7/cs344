def unique_counter(unique_list, corpus):
    '''
    add unique words from a corpus to a list
    '''
    for sample in corpus:
        for word in sample:
            # check if word in this sample has already been added
            if word not in unique_list:
                unique_list.append(word)
    return unique_list

def word_hash(corpus):
    '''
    create a hash for each word in a corpus of the number of times it appears
    '''
    count_hash = {}
    for sample in corpus:
        done = []
        for word in sample:
            # check if word in this sample has already been counted
            if word not in done:
                # check if word already has an entry and if so
                # update the new count
                if word in count_hash:
                    count_hash[word] = sample.count(word) + count_hash[word]
                else:
                    count_hash[word] = sample.count(word)
                done.append(word)
    return count_hash

def word_prob(good, bad, word, ngood, nbad):
    '''
    compute the probability that a word is spam
    '''
    g = 2 * good.get(word, 0)
    b = bad.get(word, 0)
    if g + b >= 1:
        return max(0.01, min(0.99, min(1.0, b / nbad) / (min(1.0, g / ngood) + min(1.0, b / nbad))))
    return -1


def prob_hash(good, bad, ngood, nbad, word_list):
    '''
    find the probability a word means something is spam and put this value in a hash
    '''
    spam_prob = {}
    for word in word_list:
        spam_prob[word] = word_prob(good, bad, word, ngood, nbad)
    return spam_prob

def interesting_list(mail):
    '''
    assumes the mail comes in a list of tokens
    returns the 15 most interesting tokens probability speaking (how far their spam probability is from a neutral .5)
    '''


def is_mail_spam(mail):
    '''
    a way to check if new mail is spam
    assumes the mail comes in the form of a list of tokens
    '''
    interesting_list(mail)


# a corpus has to a be a list of lists which contain strings
spam_corpus = [["i", "am", "spam", "spam", "i", "am"], ["i", "do", "not", "like", "that", "spamiam"]]
ham_corpus = [["do", "i", "like", "green", "eggs", "and", "ham"], ["i", "do"]]

# get unique words in a each corpus
word_list = []
word_list = unique_counter(word_list, ham_corpus)
word_list = unique_counter(word_list, spam_corpus)

# get count hashtable for each corpus
spam_hash = word_hash(spam_corpus)
ham_hash = word_hash(ham_corpus)
# get size of each
ngood = len(ham_corpus)
nbad = len(spam_corpus)

# generate a hash of word to probability an email with that word is spam
spam_prob_hash = prob_hash(ham_hash, spam_hash, ngood, nbad, word_list)
print(spam_prob_hash)