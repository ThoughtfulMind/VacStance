# **VacStance** 
**De**tecting **S**tance in **M**edia **O**n **C**ovid-19 Vaccine

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

* Our **dataset VacStance** itself can be accessed via `vacstance.tsv` in the main directory. The dataset contains tab-separated fields for each of the following:
	1. `sentence`: the sentence 
	2. `annotator_0`, ..., `annotator_3`: ratings from each of the 4 annotators for the stance of the sentence
	3. `disagree`: the probability that the sentence expresses disagreement with the target opinion (that Covid-19 vaccine is safe.), as estimated by our Bayesian model
	4. `agree`: the probability that the sentence expresses agreement with the target opinion (that Covid-19 vaccine is safe.)
	5. `neutral`: the probability that the sentence is neutral to the target opinion (that Covid-19 vaccine is safe.)
	6. `guid`: a unique ID for each sentence
	7. `in_held_out_test`: whether the sentence was used in our held-out-test set for model and baseline evaluation

Note: The first 5 rows are the 5 screen sentences we use to make sure that annotators correctly understand the task, and thus do not have estimated probability distributions.
* Our **lexicons of framing devices** are located in `4_analyses/lexicons`.
* The sequence of code to replicate our results can be found in the individual READMEs of the numbered sub-directories.
