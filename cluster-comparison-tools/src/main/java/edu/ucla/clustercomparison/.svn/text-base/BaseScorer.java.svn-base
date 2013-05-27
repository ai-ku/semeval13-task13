/*
 * Copyright 2013 David Jurgens
 *
 * This file is part of the Cluster-Comparison package and is covered under the
 * terms and conditions therein.
 *
 * The Cluster-Comparison package is free software: you can redistribute it
 * and/or modify it under the terms of the GNU General Public License version 2
 * as published by the Free Software Foundation and distributed hereunder to
 * you.
 *
 * THIS SOFTWARE IS PROVIDED "AS IS" AND NO REPRESENTATIONS OR WARRANTIES,
 * EXPRESS OR IMPLIED ARE MADE.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, WE MAKE
 * NO REPRESENTATIONS OR WARRANTIES OF MERCHANT- ABILITY OR FITNESS FOR ANY
 * PARTICULAR PURPOSE OR THAT THE USE OF THE LICENSED SOFTWARE OR DOCUMENTATION
 * WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER
 * RIGHTS.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

package edu.ucla.clustercomparison;

import java.io.*;

import java.util.*;

import java.util.logging.*;


/**
 * The main scoring procedure for supervised evaluations.  This class handles
 * the 80/20 test-train split and sense mapping, delegating the specific form of
 * evaluation to its subclasses.
 */
public abstract class BaseScorer {
    
    static final int randomSeed = 42;

    /**
     * The source of randomness for dividing the train and test splits.  This
     * randomness is deterministic thanks to the constant seed.
     */
    static final Random rand = new Random(randomSeed);

    /**
     * Computes the score of the evaluation between the two SensEval keys file,
     * optionally performing remapping and optionally writing the remapped key
     * to {@code outputKeyFile}.
     *
     * @param goldKeyFile the SensEval key file against which the test key is to
     *        compared
     * @param testKeyFile the SensEval key file to be compared.  If the key is
     *        using a different sense inventory, {@code performRemapping} should
     *        be set to {@code true}.
     * @param outputKeyFile if {@code performRemapping} is {@code true}, the
     *        remapped key is written to this file if non-{@code null}.
     * @param performRemapping whether the test key should have its instance
     *        labels remapped into the gold key's label set
     */
    public double score(File goldKeyFile, File testKeyFile,
                        File outputKeyFile, boolean performRemapping) throws Exception {

        // Load the gold standard and induced key files
        Map<String,Map<String,Map<String,Double>>> goldKey = 
            KeyUtil.loadKey(goldKeyFile);
        Map<String,Map<String,Map<String,Double>>> testKey = 
            KeyUtil.loadKey(testKeyFile);     
        
        return score(goldKey, testKey, outputKeyFile, performRemapping);
    }

    /**
     * Computes the score of the evaluation between the two keys, optionally
     * performing remapping and optionally writing the remapped key to {@code
     * outputKeyFile}.
     *
     * @param goldKey the key against which the test key is to compared
     * @param testKey the key to be compared.  If the key is using a different
     *        sense inventory, {@code performRemapping} should be set to {@code
     *        true}.
     * @param outputKeyFile if {@code performRemapping} is {@code true}, the
     *        remapped key is written to this file if non-{@code null}.
     * @param performRemapping whether the test key should have its instance
     *        labels remapped into the gold key's label set
     */
    public double score(Map<String,Map<String,Map<String,Double>>> goldKey,
                        Map<String,Map<String,Map<String,Double>>> testKey,
                        File outputKeyFile, boolean performRemapping) throws Exception {
        
        PrintWriter outputGradedVectorKey = 
            (outputKeyFile == null) ? null : new PrintWriter(outputKeyFile);

        List<String> allInstances = new ArrayList<String>();
        for (Map<String,Map<String,Double>> m : goldKey.values())
            allInstances.addAll(m.keySet());
        
        // Create a list of all the indices of the instances in the gold key and
        // then permute that list in a deterministic manner to decide on the
        // 80/20 splits.  The shuffle avoids any potiential bias that was in the
        // original ordering.
        List<Integer> indices = new ArrayList<Integer>();
        for (int i = 0; i < allInstances.size(); ++i)
            indices.add(i);
        Collections.shuffle(indices, rand);
        
        // Create the sets of training instances by dividing the key into 80%
        // train, 20% test
        List<Set<String>> trainingSets = new ArrayList<Set<String>>();
        for (int i = 0; i < 5; ++i)
            trainingSets.add(new HashSet<String>());
        for (int i = 0; i < allInstances.size(); ++i) {
            String instance = allInstances.get(i); //.split(" ")[1];
            int toExclude = i % trainingSets.size();
            for (int j = 0; j < trainingSets.size(); ++j) {
                if (j == toExclude)
                    continue;
                trainingSets.get(j).add(instance);
            }
        }
              

        // Perform a quick sanity check with respect to the remapping
        Set<String> goldSenses = new HashSet<String>();
        for (Map.Entry<String,Map<String,Map<String,Double>>> e : goldKey.entrySet()) {
            String word = e.getKey();
            for (Map<String,Double> ratings : e.getValue().values())
                goldSenses.addAll(ratings.keySet());
        }
        
        Set<String> testSenses = new HashSet<String>();
        for (Map.Entry<String,Map<String,Map<String,Double>>> e : testKey.entrySet()) {
            String word = e.getKey();
            for (Map<String,Double> ratings : e.getValue().values())
                testSenses.addAll(ratings.keySet());
        }
        double origSize = goldSenses.size();        
        goldSenses.removeAll(testSenses);
//         if (goldSenses.size() / origSize < 0.25 && performRemapping) {
//             System.err.println("ATTENTION: " +                               
//                 "It appears that your test key is using the same sense-IDs as\n"+
//                 "the supplied gold standard key, but you are also remapping\n" +
//                 "the testing key's labels.  Are you sure you don't want to\n" +
//                 "use the --no-remapping option?");
//         }
//         else if (origSize == goldSenses.size() && !performRemapping) {
//             System.err.println("ATTENTION: " +
//                 "It appears that your test key is not using the same sense-IDs\n"+
//                 "as the supplied gold standard key, but you are not remapping\n" +
//                 "the testing key's sense labels into the gold key's sense\n" +
//                 "inventory.  Are you sure you want to use the --no-remapping\n"+
//                 "option?");
//         }


        // We approximate the number of senses for this term by examining the
        // totality of senses used for the term in the gold standard labeling.
        Map<String,Integer> termToNumberSenses = 
            new HashMap<String,Integer>();

        for (Map.Entry<String,Map<String,Map<String,Double>>> e : goldKey.entrySet()) {
            String term = e.getKey();
            Set<String> senses = new HashSet<String>();
            for (Map<String,Double> ratings : e.getValue().values())
                senses.addAll(ratings.keySet());
            termToNumberSenses.put(term, senses.size());
        }



        int numLabeledTestInstances = 0;
        for (Map<?,?> m : testKey.values())
            numLabeledTestInstances += m.size();
//         System.out.printf("Loaded %d gold standard instances, and %d test instances%n", 
//                           allInstances.size(), numLabeledTestInstances);

        // Score the test key
        Map<String,Double> instanceScores  
            = runEval(getEvaluation(), new GradedReweightedKeyMapper(), 
                      goldKey, testKey, trainingSets, 
                      allInstances, outputKeyFile, performRemapping,
                      termToNumberSenses);
        
        
        Map<String,String> instanceToWord = new HashMap<String,String>();
        for (Map.Entry<String,Map<String,Map<String,Double>>> e : goldKey.entrySet()) {
            String word = e.getKey();
            for (String instance : e.getValue().keySet())
                instanceToWord.put(instance, word);
        }

        Map<String,List<Double>> termToScores = new LinkedHashMap<String,List<Double>>();
        for (String term : goldKey.keySet())
            termToScores.put(term, new ArrayList<Double>());

        for (Map.Entry<String,Double> e : instanceScores.entrySet()) {
            String inst = e.getKey();
            String term = instanceToWord.get(inst);
            List<Double> scores = termToScores.get(term);
            scores.add(e.getValue());
        }

        // Generate the report
        double allScoresSum = 0;
        double numAnswered = 0;
        System.out.println("===================================================================");
        System.out.printf("term\taverage_score\trecall\tf-score%n");
        System.out.println("-------------------------------------------------------------------");
        for (Map.Entry<String,List<Double>> e : termToScores.entrySet()) {
            String term = e.getKey();
            double numInstances = goldKey.get(term).size();
            List<Double> scores = e.getValue();
            double recall = scores.size() / numInstances;
            numAnswered += scores.size();
            double sum = 0;
            for (Double d : scores) {
                if (Double.isNaN(d) || Double.isInfinite(d)) 
                    throw new Error();
                sum += d;
            }
            allScoresSum += sum;
            double avg = (scores.size() > 0) ? sum / scores.size() : 0;
            if (Double.isNaN(avg) || Double.isInfinite(avg)) 
                throw new IllegalStateException();
            double fscore = (avg + recall > 0) 
                ? (2 * avg * recall) / (avg + recall)
                : 0;
            
            System.out.println(term + "\t" + avg + "\t" + recall + "\t" + fscore);
        }
         System.out.println("-------------------------------------------------------------------");
        // Print out the aggregate
        double avg = (numAnswered > 0) ? allScoresSum / numAnswered : 0;
        double recall = numAnswered / allInstances.size();
        double fscore = (avg + recall > 0) 
            ? (2 * avg * recall) / (avg + recall)
            : 0;
            
         System.out.println("all\t" + avg + "\t" + recall + "\t" + fscore);        
         System.out.println("===================================================================");
        return fscore;
    }

    /**
     * Returns the evaluation to be used
     */
    protected abstract Evaluation getEvaluation();

    /**
     * Computes the evaluation over the all the test-training splits.
     */
    Map<String,Double> runEval(Evaluation evaluation,
                               KeyMapper keyMapper, 
                               Map<String,Map<String,Map<String,Double>>> goldKey,
                               Map<String,Map<String,Map<String,Double>>> testKey,
                               List<Set<String>> trainingSets,
                               List<String> allInstances,
                               File outputKey, 
                               boolean performRemapping,
                               Map<String,Integer> termToNumberSenses) throws IOException {
        
        Map<String,Double> instanceScores = new LinkedHashMap<String,Double>();

        PrintWriter outputKeyWriter = (outputKey == null) 
            ? null : new PrintWriter(outputKey);

        int round = 0;
        for (Set<String> trainingInstances : trainingSets) {

            // Map the induced senses to gold standard senses
            Map<String,Map<String,Map<String,Double>>> remappedTestKey = 
                (performRemapping)
                ? keyMapper.convert(goldKey, testKey, trainingInstances)
                : testKey;
            
            // If the user has specified that we need to produce the output key,
            // write it now
            if (outputKeyWriter != null)
                writeKey(remappedTestKey, outputKeyWriter);

            // Determine which set of instances should be tested
            Set<String> instancesToTest = new HashSet<String>();
            for (Map<String,?> m : goldKey.values())
                instancesToTest.addAll(m.keySet());
            instancesToTest.removeAll(trainingInstances);
            
            Map<String,Double> scores = 
                evaluation.test(remappedTestKey, goldKey, instancesToTest,
                                termToNumberSenses);
            instanceScores.putAll(scores);
        }

        // Finish writing the key 
        if (outputKeyWriter != null)
            outputKeyWriter.close();        
        
        return instanceScores;
    }        

    /**
     * Loads the lines in a file as a list
     */
    static List<String> loadFileAsList(File f) throws IOException {
        List<String> lines = new ArrayList<String>();
        BufferedReader br = new BufferedReader(new FileReader(f));
        for (String line = null; (line = br.readLine()) != null; )
            lines.add(line);
        br.close();
        return lines;
    }
    
    /**
     * Writes the Senseval key file for this remapping
     */
    static void writeKey(Map<String,Map<String,Map<String,Double>>> remappedTestKey,
                         PrintWriter pw) {

        for (Map.Entry<String,Map<String,Map<String,Double>>> e 
                 : remappedTestKey.entrySet()) {
            String term = e.getKey();
            Map<String,Map<String,Double>> instances = e.getValue();
            for (Map.Entry<String,Map<String,Double>> e2 
                     : instances.entrySet()) {
                String instance = e2.getKey();
                Map<String,Double> senses = e2.getValue();
                StringBuilder sb = new StringBuilder(term);
                sb.append(' ').append(instance);
                for (Map.Entry<String,Double> e3 : senses.entrySet()) {
                    sb.append(' ').append(e3.getKey())
                        .append('/').append(e3.getValue());
                }
                pw.println(sb);
            }
        }
    }
}
