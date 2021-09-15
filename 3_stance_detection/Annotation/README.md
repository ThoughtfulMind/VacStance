# Stance Detection – Annotation

* `full_annotations.tsv` has the following fields for each item: 
  * `sentence` (text shown to annotators), 
  * `annotator_n`, where `n` ranges from 0-3 (annotation from the nth worker)
  * `round` (round is always 1), 
  * `batch` (batch number is always 0), 
  * `sent_id` (ID of item within each batch. IDs beginning with 's' indicate a screen item; IDs beginning with 't' indicate a true item),
  * `av_rating` (average rating over all 4 annotators, with the label mapping `{"agree": 1, "neutral": 0, "disagree": -1}`,
  * `disagree`, `agree`, `neutral` (respective probabilities that the true label is the one given by the column name, as estimated by our item-response model),
  * `MACE_pred` (true label as estimated by [MACE](https://github.com/dirkhovy/mace))

* `anon_subj_info.tsv` has the following fields for each annotator:
  * `round` (round ID, one of 1), 
  * `batch` (batch number is always 0),
  * `age`, `gender`, `education`, `party`, `state` (self-reported age, gender, level of education, political affiliation, and state of residence)
  * `poll*` (responses to each of 7 total poll questions that gauge stance toward Covid-19 vaccine, see `Annotation/poll_questions.txt` for the full questions and answer choices) 

