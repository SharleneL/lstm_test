__author__ = 'luoshalin'

import random

class Sampler:
    def __init__(self, prob_table):
        total_prob = 0.0
        if type(prob_table) is dict:
            for key, value in prob_table.items():
                total_prob += value
        elif type(prob_table) is list:
            prob_table_gen = {}
            for key in prob_table:
                prob_table_gen[key] = 1.0 / (float(len(prob_table)))
            total_prob = 1.0
            prob_table = prob_table_gen
        else:
            print("__init__ takes either a dict or a list as its first argument")
        if total_prob <= 0.0:
            raise ValueError("Probability is not strictly positive.")
        self._keys = []
        self._probs = []
        for key in prob_table:
            self._keys.append(key)
            self._probs.append(prob_table[key] / total_prob)

    def __call__(self):
        sample = random.random()
        seen_prob = 0.0
        for key, prob in zip(self._keys, self._probs):
            if (seen_prob + prob) >= sample:
                return key
            else:
                seen_prob += prob
        return key


def generate_nonsense(word = ""):
    # generate samplers
    samplers = {
    "punctuation": Sampler({".": 0.49, ",": 0.5, ";": 0.03, "?": 0.05, "!": 0.05}),
    "stop": Sampler({"the": 10, "from": 5, "a": 9, "they": 3, "he": 3, "it" : 2.5, "she": 2.7, "in": 4.5}),
    "noun": Sampler(["cat", "broom", "boat", "dog", "car", "wrangler", "mexico", "lantern", "book", "paper", "joke","calendar", "ship", "event"]),
    "verb": Sampler(["ran", "stole", "carried", "could", "would", "do", "can", "carry", "catapult", "jump", "duck"]),
    "adverb": Sampler(["rapidly", "calmly", "cooly", "in jest", "fantastically", "angrily", "dazily"])
    }

    # generate nonsense
    if word.endswith("."):
        return word
    else:
        if len(word) > 0:
            word += " "
        word += samplers["stop"]()
        word += " " + samplers["noun"]()
        if random.random() > 0.7:
            word += " " + samplers["adverb"]()
            if random.random() > 0.7:
                word += " " + samplers["adverb"]()
        word += " " + samplers["verb"]()
        if random.random() > 0.8:
            word += " " + samplers["noun"]()
            if random.random() > 0.9:
                word += "-" + samplers["noun"]()
        if len(word) > 500:
            word += "."
        else:
            word += " " + samplers["punctuation"]()
        return generate_nonsense(word)


def generate_dataset(total_size, ):
    sentences = []
    for i in range(total_size):
        sentences.append(generate_nonsense())
    return sentences