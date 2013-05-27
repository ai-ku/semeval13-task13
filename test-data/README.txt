===============================================================================

SemEval-2013 Task 13: Word Sense Induction for Graded and Non-Graded Senses

David A. Jurgens and Ioannis P. Klapaftis.  February 27, 2013

This README.txt file describes the test data for SemEval-2013 Task 13. For
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


TASK

Task 13 evaluates Word Sense Induction (WSI) and Unsupervised WSD systems in two
settings (1) a WSD task for Unsupervised WSD and WSI systems, (2) a clustering
comparison setting that evaluates the similarity of the sense inventories for
WSI systems.  Participants are presented examples contexts of each word and
asked to label each usage with as many senses as they think are applicable,
along with numeric weights denoting the relative levels of applicability.


TRAINING DATA:

Because the task is focused on unsupervised approaches for both WSI and WSD, no
training data is provided.  However, WSI systems will use a common corpus, the
ukWaC, to build their sense inventories.  The ukWaC is a 2-billion word
web-gathered corpus, which has also been released in POS-tagged and dependency
parsed formats. The corpus is available for download from the WaCky group here:

http://wacky.sslmit.unibo.it/

Participants may select their data from some or all of the ukWaC.  Furthermore,
unlike in previous WSI tasks, we will allow participants to use additional
training contexts not found in the ukWaC under the condition that they submit
systems for both using only the ukWaC and with their augmented corpora. This
option is designed for evaluating the impact of specialized corpora for
improving the quality of the induced senses.


TESTING DATA:

Testing data is provided as a set of XML files, with one file for each of the 50
test terms.  The XML files contain one context per test item and are formatted
as follows:

<instances lemma="win" partOfSpeech="v">
  <instance id="win.v.1" lemma="win" partOfSpeech="v" token="win" tokenEnd="21" tokenStart="18">instance text<</instance>
  ...
</instances>

Instance attributes are defined as follows:

-  "id" is the particular ID associated with that test and is used
  to report the senses
- "lemma" is the lemmatized target term
- "pos" is the part of speech of the target term
- "token" is the lexical form of the target term as it appears in the text itself
- "tokenStart" and "tokenEnd" indicate the sentence position of the token for
  the target term in the sentence.

Instances are drawn from both written, spoken, and web-based text, and therefore
may include a variety of sentence structures (or even be fragments).  


TESTING:

Using either the WordNet 3.1 sense inventory or an induced sense inventory,
participants must annotate each instance of a target word with one or more of
their senses, and optionally with those senses' applicabilities.

The annotation key will use the traditional key format used in prior Senseval
and SemEval WSD tasks (details here: http://www.senseval.org/senseval3/scoring).
Each line is the annotation for a particular instance, formatted as:

lemma.partOfSpeech instance-id sense-name/applicability-rating

For example, a rating might appear as:

win.v win.v.instance.1 win.v.1/1.0 win.v.2/4.7

Unsupervised systems should use the WordNet numbering convention for their
senses such that the first reported sense for a lemma is labeled as sense 1,
e.g., win.v.1 or win.v#1 (either is acceptable).

Sense induction systems may use a naming convention of their choice for their
senses so long as each sense has a unique label that does not contain the '/'
character.

The sense applicability ratings may be any positive value.  All ratings will be
normalized so the maximum value is 1, indicating completely applicable.  Senses
without ratings are assumed to have maximum applicability.


SUBMISSION:

1. Teams will upload each of their submissions to the FTP server at
   semeval2013.ku.edu.tr .  Log in information should be provided when
   registering the team on the SemEval website www.cs.york.ac.uk/semeval-2013 .

2. Each of a team's submissions should be contained in a different archive,
   e.g., a .zip or .tar.gz.  Please note that we ask teams to submit at most
   three submissions.

3. Submissions should be named using the format "task13-TEAM-APPROACH.zip".
   TEAM is the name of your team, which is used only for distinguishing your
   submissions from those of other teams.  APPROACH is a short name that
   distinguishes between your team's submissions, if you choose to submit
   multiple solutions.  

4. Teams should include both a .key file in the SemEval WSD format noted above
   (http://www.senseval.org/senseval3/scoring) and a .txt file with a short
   system description.  The description should include (1) the general approach,
   (2) whether the system uses Unsupervised WSD or WSI (3) the types of features
   for sense disambiguation, and (4) in the case of WSI systems, which features,
   methods, and corpora were used to induce the senses.  This description
   greatly helps us in summarizing the participants in the task description
   paper.


CONTACT:

For questions, comments, or bug reports, please contact the SemEval-2013 Google
groups: semeval-2013-task-13@groups.google.com

For specific questions, please contact the organizers

David Jurgens - jurgens@di.uniroma1.it
Ioannis P. Klapaftis - klapaftis@outlook.com


VERSIONS:

1.0 - Initial release of test data and README

===============================================================================
