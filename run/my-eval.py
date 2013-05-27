#!/usr/bin/env python

from collections import defaultdict as dd
import gzip
from itertools import count, izip, permutations
from math import log
from optparse import OptionParser
import sys

def open_file(f):
    if f == '-':
        return sys.stdin
    elif f.endswith('.gz'):
        return gzip.open(f)
    else:
        return open(f)

def process_file(f):
    targets = dd(lambda: dd(list))
    for line in open_file(f):
        line = line.split()
        targets[line[0]][line[1]].extend(line[2:])
    return targets

def process_target(target):
    counts = dd(int)
    values = dd(float)
    for target_id, vector in target.iteritems():
        for i in xrange(len(vector)):
            sense_value = vector[i].split("/") + [1.0]
            counts[sense_value[0]] += 1
            values[sense_value[0]] += float(sense_value[1])
            vector[i] = (sense_value[0], float(sense_value[1]))
    return counts, values

def enumerate_instances(target, valid_senses, size):
    c = count()
    mapping = dd(lambda: c.next())
    new_target = {}
    empty_vector = [0.0] * size
    for target_id, vector in target.iteritems():
        new_vector = [0.0] * size
        for sense, value in vector:
            if valid_senses.get(sense):
                new_vector[mapping[sense]] = value
        if new_vector == empty_vector:
            new_vector = [1.0] * size
        new_target[target_id] = new_vector
    return new_target, mapping

def prob_normalize(vector):
    s = sum(vector)
    return [v / s for v in vector]

def len_normalize(vector):
    l = sum((v * v for v in vector)) ** 0.5
    return [v / l for v in vector]

def cosine_similarity(v0, v1, mapping):
    return abs(sum((v0[i] * v1[mapping[i]] for i in xrange(len(v0)))) - 1) * 0.5

def kl_divergence(p, q):
    s = 0
    for p, q in izip(p, q):
        if p != 0:
            s += log(p / q) * p
    return s

def js_similarity(v0, v1, mapping):
    p = v0
    q = [v1[mapping[i]] for i in xrange(len(v1))]
    m = [(p[i] + q[i]) / 2 for i in xrange(len(p))]
    return (kl_divergence(p, m) + kl_divergence(q, m))

parser = OptionParser(usage="New scoring script")
parser.add_option('-g', '--gold', dest='gold', help='gold keys, - for reading gold from stdin')
parser.add_option('-a', '--answer', dest='answer', help='answer keys, - for reading answer from stdin')
parser.add_option('-s', '--similarity', dest='similarity', help='similarity function, cos or js. default cos')
parser.add_option('-r', '--remove', dest='remove', help='remove extra senses in answer, count or value. default removes lowest values')

(options, args) = parser.parse_args()

assert(options.gold)
assert(options.answer)
assert(options.similarity in set(['cos', 'js', None]))
assert(options.remove in set(['count', 'value', None]))

gold_targets = process_file(options.gold)
ans_targets = process_file(options.answer)

if options.similarity in set(['cos', None]):
    normalize = len_normalize
    similarity = cosine_similarity
else:
    normalize = prob_normalize
    similarity = js_similarity

if options.remove in set(['value', None]):
    remove_counts = False
else:
    remove_counts = True

target_scores = {}
for target in gold_targets.iterkeys():
    if ans_targets.get(target) == None: continue

    gold_target = gold_targets[target]
    gold_counts, gold_values = process_target(gold_target)

    ans_target = ans_targets[target]
    ans_counts, ans_values = process_target(ans_target)

    # print "============================================="
    # print gold_target
    # print "---------------------------------------------"
    # print gold_counts
    # print "---------------------------------------------"
    # print gold_values
    # print "============================================="
    # print ans_target
    # print "---------------------------------------------"
    # print ans_counts
    # print "---------------------------------------------"
    # print ans_values

    if len(gold_counts) < len(ans_counts):
        if remove_counts:
            ans_counts = dict(sorted(ans_counts.iteritems(), key=lambda x: x[1], reverse=True)[:len(gold_counts)])
        else:
            ans_counts = dict(sorted(ans_values.iteritems(), key=lambda x: x[1], reverse=True)[:len(gold_counts)])

    gold_target, gold_mapping = enumerate_instances(gold_target, gold_counts, len(gold_counts))
    ans_target, ans_mapping = enumerate_instances(ans_target, ans_counts, len(gold_counts))

    # print "============================================="
    # print gold_target
    # print "---------------------------------------------"
    # print gold_mapping
    # print "============================================="
    # print ans_target
    # print "---------------------------------------------"
    # print ans_mapping
    # break

    gold_vectors = []
    ans_vectors = []
    for t in gold_target.iterkeys():
        if ans_target.get(t):
            gold_vectors.append(normalize(gold_target[t]))
            ans_vectors.append(normalize(ans_target[t]))

    min_mapping = (float('inf'), None)
    for mapping in permutations(xrange(len(gold_counts))):
        score = sum((similarity(gold_vectors[i], ans_vectors[i], mapping) for i in xrange(len(gold_vectors))))
        min_mapping = min(min_mapping, (score, mapping))

    target_scores[target] = (min_mapping[0], len(gold_vectors))

for target, score in sorted(target_scores.iteritems()):
    print "%s\t%d\t%.2f" % (target, score[1], score[0])

total_count = sum((x[1] for x in target_scores.itervalues()))
total_score = sum((x[0] for x in target_scores.itervalues()))
print "total\t%d\t%.2f" % (total_count, total_score)
