# **VacStance** 
**Detecting Stance in a Polarized Media Environment: 
The Covid-19 Vaccine Case in the United States**

The introduces VacStance, a dataset of 2,000 stance-labeled Covid-19 vaccine sentences extracted from 169,432 sentences drawing from 15,750 news articles covering left-leaning and right-leaning media outlets. A trained BERT classifier analyzes aspects of argumentation, how the different sides of the vaccine debate represent their own and each other’s opinions. 

This repository contains code and data for the capstone project.

It is based on a paper and code by:
> Luo, Y., Card, D. and Jurafsky, D. (2020). DeSMOG: Detecting Stance in Media On Global Warming. In *Findings of the Association for Computational Linguistics: EMNLP 2020*. 
> GitHub: https://github.com/yiweiluo/GWStance 
```
```
## Getting started
1. Create and activate a Python 3.6 environment.
2. Run `pip install -r requirements.txt`.
3. Re-install neuralcoref with the `--no-binary` option: 
```
pip uninstall neuralcoref
pip install neuralcoref --no-binary neuralcoref
```
4. Download SpaCy's English model: `python -m spacy download en`
5. Update the `config.json` file with your local OS variables.

## Repository structure

* The **dataset VacStance** itself can be accessed via `vacstance.tsv` in the main directory. The dataset contains tab-separated fields for each of the following:
	1. `sentence`: the sentence 
	2. `annotator_0`, ..., `annotator_3`: ratings from each of the 4 annotators for the stance of the sentence
	3. `disagree`: the probability that the sentence expresses disagreement with the target opinion (that Covid-19 vaccine is safe.), as estimated by our Bayesian model
	4. `agree`: the probability that the sentence expresses agreement with the target opinion (that Covid-19 vaccine is safe.)
	5. `neutral`: the probability that the sentence is neutral to the target opinion (that Covid-19 vaccine is safe.)
	6. `guid`: a unique ID for each sentence
	7. `in_held_out_test`: whether the sentence was used in our held-out-test set for model and baseline evaluation

* The **lexicons of framing devices** are located in `4_analyses/lexicons`.
* The sequence of code to replicate the results can be found in the individual READMEs of the numbered sub-directories.
