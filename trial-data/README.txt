===============================================================================

SemEval-2013 Task 13: Word Sense Induction for Graded and Non-Graded Senses

David A. Jurgens and Ioannis P. Klapaftis.  August 1, 2012

This README.txt file describes the trial data for SemEval-2013 Task 13. For
information about SemEval-2013 Task 13, see the task website
http://www.cs.york.ac.uk/semeval-2013/task13/.


TASK OVERVIEW:

Previous SemEval tasks on word senses have largely assumed that each usage of a
word is best labeled by a single sense.  In contrast, Task 13 proposes that
usages should be labeled by all senses that apply, with weights indicating the
degree of applicability.  This multi-sense labeling effectively captures both
cases where related senses from a fine-grain sense inventory apply and where
contextual ambiguity enables alternate interpretations.  We illustrate this with
three example sentences:

 1. The student loaded paper into the printer
 2. The student submitted her paper by email.
 3. The student handed her paper to the teacher at the beginning of class

according to the first two senses of paper in WordNet 3.1:

 1) paper - a material made of cellulose pulp derived mainly from wood or rags
    or certain grasses
 2) paper - an essay, especially one written as an assignment

The first sentence refers to the material sense of paper, while the second
sentence refers to the essay sense of paper.  In contrast, both senses are
possible interpretations in the third sentence, though with different degrees;
here, the usage evokes separate properties of the concept of its form (a
cellulose material) and purpose (an assignment), which are themselves distinct
senses of paper.  Similar multi-label conditions may also be constructed for
word uses where a reader perceives multiple, unrelated interpretations due to
contextual ambiguity.  While most previous work on WSD makes a best guess as to
which interpretation is correct, Task 13 opts to make explicit the ambiguity
explicit in the multi-sense labeling.


TASK:

Task 13 evaluates Word Sense Induction (WSI) and Unsupervised WSD systems in two
settings (1) a WSD task for Unsupervised WSD and WSI systems, (2) a clustering
comparison setting that evaluates the similarity of the sense inventories for
WSI systems.  Participants are presented examples contexts of each word and
asked to label each usage with as many senses as they think are applicable,
along with numeric weights denoting the relative levels of applicability.


DATA PACKAGE SUMMARY:  (v1.2)

This download package contains the necessary data for testing and evaluating
Graded WSD systems that use induced senses.

data/ - an XML file containing the trial data, along with its graded word
        sense annotations

evaluation/ - programs for running different evaluations

evaluation/unsupervised - programs for running the unsupervised evaluations

evaluation/supervised - programs for running the supervised evaluations

evaluation/keys/gold-standard - two gold standard keys for the trial data set.
                                See the trial data section below for more information

evaluation/keys/baselines - baseline keys for use with the evaluation programs
                            and comparison with new responses

TRAINING DATA:

Because WSI is a fundamentally unsupervised technique, no human-labeled training
data is provided.  However, a common corpus, the ukWaC, will be used by all
participants.  The ukWaC is a 2-billion word web-gathered corpus, which has also
been released in POS-tagged and dependency parsed formats. The corpus is
available for download from the WaCky group here:

http://wacky.sslmit.unibo.it/

Participants may select their data from some or all of the ukWaC.  Furthermore,
unlike in previous WSI tasks, we will allow participants to use additional
contexts not found in the ukWaC under the condition that they submit systems for
both using only the ukWaC and with their augmented corpora. This option is
designed for evaluating the impact of target corpora for improving the quality
of the induced senses.


TRIAL DATA:

The SemEval-2013 Task 13 trial data is a redistribution of the Graded Sense and
Usage data set provided by Katrin Erk, Diana McCarthy, and Nicholas Gaylord (Erk
et al., 2009).  The data set contains 50 contexts for eight terms: three nouns,
three verbs, and two adjectives, all with moderate polysemy (4-7 senses).  Full
details of the data set and annotation methodology are available at:

  http://www.katrinerk.com/graded-sense-and-usage-annotation

Each context was annotated by three annotators using a rating scale of 1 to 5,
where 1 indicates the sense is not applicable and 5 indicates that the sense
completely matches the meaning in context.

From their annotations, we derived the gold standard sense key as follows.  The
mean sense rating was used as the true sense applicability.  If in a given
context, a sense had a mean rating of 1 (i.e., rated not applicable by all
annotators), it was not included in the gold standard key for that context.  All
other senses are included.


TESTING:

Once the sense inventory has been built, participants must annotation each
instance of the target words with one or more of their induced senses, and
optionally with those senses' applicabilities.

The annotation key will use the traditional key format used in prior Senseval
and SemEval WSD tasks (details here: http://www.senseval.org/senseval3/scoring).
Each line is the annotation for a particular instance, formatted as:

lemma.partOfSpeech instance-id sense/rating

For example, a rating might appear as:

win.v br-c17.snum=62 win.v.mysense.1/1.0

where win.v.mysense.1 is the name of a particular induced sense.  The sense
applicability ratings may be any positive value.  All ratings will be normalized
to sum to 1.


The Trial Data 1.2 release contains four supervised and two unsupervised
evaluations.  The unsupervised evaluations capture two diverging aspects of
clusterings:

  1. Fuzzy Normalized Mutual Information (NMI): We extend the notion of mutual
     information to the fuzzy clustering setting.  Fuzzy NMI captures the
     alignment of the two clusterings independent of the cluster sizes and
     therefore serves as an effective measure of the ability of an approach to
     accurately model rare senses.

  2. Fuzzy B-Cubed: We adapt the overlapping B-Cubed definition from Amigo et
     al.  (2009) to the fuzzy clustering setting.  Fuzzy B-Cubed provides an
     item-based evaluation that is sensitive to the cluster size skew and
     effectively captures the expected performance of the system on a dataset
     where the cluster (i.e., sense) distribution would be equivalent.

The supervised objectives are grouped into three objectives:

Detection: Determining which of a word's senses are applicable

  1. The Jaccard Index 

Ranking: Ranking a word's senses according to applicability

  1. Goodman and Kruskal's gamma is a nonparametric rank correlation
     coefficient similar to Kendall's tau and Speaman's rho.  The gamma
     statistic handles tied ranks better than tau or rho (Siegel and Castellan
     Jr., 1988), which are frequent in the GWS data set of Erk et al. (2009).

  2. The task places more importance on the ranking of the most present senses.
     Goodman and Kruskal's gamma penalizes all rank differences equally.
     Therefore, as an alternative, we use a positionally-weighted Kendall's Tau,
     adapted from the tau-distance described in Kumar and Vassilvitskii (2010).
     Weighted tau discounts deviations in the lower ranks, which is better
     aligned with the objectives of this task.

Applicability: Quantifying the applicability levels of each sense

  1. Previous methods of comparing the numeric ratings used either the
     Jensen-Shannon Divergence (Erk and McCarthy, 2009) or cosine similarity
     (Jurgens 2012).  However, these methods insufficiently distinguished good
     ratings from bad in certain cases.  Therefore, we adopt a new measure,
     Weighted Normalized Discounted Cumulative Gain (Weighted NDCG), which is
     adapted from Discounted Cumulative Gain (DCG) described by Moffat and Zobel
     (2008).  Weighted NDCG takes both the ranking and difference in weight into
     account when scoring solutions.

All supervised evaluations use an 80/20 testing-training split to learn the
mapping from induced senses to gold standard senses.  Note that unlike in
previous SemEval WSI tasks, the split value is maintained internally and so
doesn't need to be specified on the command line.  The resulting scores reflect
the average score for all testing instances across all five splits.

Each of the evaluations are run through a command-line Java program.  For example:

java -jar perception.jar gold-standard.key my-ratings.key

java -jar ranking.jar gold-standard.key mfs.key

GOLD STANDARD:

The trial data contains two gold standard keys for the same dataset.  The
annotations provided by Erk et al. (2009) varied considerably in their
agreement.  Kripperdorff's alpha values ranged from 0.072 for win.v to 0.470 for
ask.v.  In the initial 1.0 release, we included a gold standard key that used
the same methodology as Erk and McCarthy (2009) and computed the gold sense
rating using the mean of the annotators' ratings.  However, after some review,
we have also included a second key where the rating is the median of the
ratings.  The median appears to be slightly more robust to systematic
disagreements by a single annotator over the applicability of a sense.

BASELINES:

Several baselines have been included in 1.2 release:

1) mfs.key - The most frequent sense baseline, where each instance is assigned a
   single sense according to which of its senses is most frequent in the gold
   standard annotations

2) highest-rated.key - An analog to the mfs.key, where each instance is assigned
   the sense that had the highest average rating (but is not necessarily the
   most frequent).

3) all-senses.key - Each instance is assigned all the senses with equal
   applicability

4) all-senses.freq-ranked.key - Each instance is assigned all senses with
   applicability equal to their frequency in the gold standard annotations

5) all-senses.avg-rating.key - Each instance is assigned all senses with each
   sense being rated with its average applicability rating in the gold standard

6) random.2-senses.key - Each instance is assigned randomly one of two senses
   with equal applicability

7) random.3-senses.key - Each instance is assigned randomly one of three senses
   with equal applicability

8) random.n-senses.key - Each instance is assigned randomly one of n senses with
   equal applicability, where n is the true number of senses for the word.




CONTACT:

For questions, comments, or bug reports, please contact the SemEval-2013 Google
groups: semeval-2013-task-13@groups.google.com

For specific questions, please contact the organizers

David Jurgens - jurgens@cs.ucla.edu 
Ioannis P. Klapaftis - klapaftis@outlook.com


VERSIONS:

1.0 - Initial release of trial data, baseline keys, and two supervised evaluations

1.1 - Addition of two unsupervised evaluations (Fuzzy B-Cubed and Fuzzy NMI),
    - Addition of two supervised evaluations (Weighted Tau and Weighted NDCG)
    - Revised perception.jar to jaccard-index.jar and ranking.jar to
      gk-gamma.jar for clarity
    - Updated with new task number and Google Group
    - Added new baseline key for trial data
    - Updated task and trial data description 

1.2 - Corrected the output for the jaccard-index.jar, weighted-tau.jar and
      weighted-ndcg.jar to report the per-word error rates and column headers.
    - Updated task description 


REFERENCES:

Enrique Amigo, Julio Gonzalo, Javier Artiles, and Felisa Verdejo. 2009. A
comparison of extrinsic clustering evaluation metrics based on formal
constraints. In- formation Retrieval, 12(4):461–486.

Katrin Erk and Diana McCarthy. 2009. Graded word sense assignment. In
Proceedings of the 2009 Conference on Empirical Methods in Natural Language
Processing: Volume 1, pages 440–449. Association for Computational Linguistics.

Katrin Erk, Diana McCarthy, and Nicholas Gaylord. 2009. Investigations on word
senses and word usages. In Proceedings of the Joint Conference of the 47th
Annual Meeting of the ACL and the 4th International Joint Conference on Natural
Language Processing of the AFNLP: Volume 1, pages 10–18. Association for
Computational Linguistics.

R. Kumar and S. Vassilvitskii. 2010. Generalized distances between rankings. In
Proceedings of the 19th international conference on World wide web, pages 571-
580. ACM.

A. Moffat and J. Zobel. 2008. Rank-biased precision for measurement of retrieval
effectiveness. ACM Transactions on Information Systems (TOIS), 27(1):2.

Sidney Siegel and N. John Castellan Jr. 1988. Nonparametric Statistics for the
Behavioral Sciences. McGraw-Hill, second edition.

===============================================================================
