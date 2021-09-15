**VacStance – Detecting Stance in a Polarized Media Environment: 
The Covid-19 Vaccine Case in the United States**

We examine U.S. news media coverage on Covid-19 vaccine topic as an illustration of a debate in a polarized environment through the stance in the media on vaccine safety. Specifically, we analyze opinion-framing in the Covid-19 vaccine debate as a way of attributing a statement or belief to someone else. We focus on self-affirming and opponent-doubting discourse and analyze if Left-leaning and Right-leaning media engage in self-affirming or opponent-doubting discourse. For example, a health expert would say that “The leading researchers agree that Covid-19 vaccines are safe and effective” while a vaccine skeptic would say that “Mistaken researchers claim that Covid-19 vaccines are safe and effective”.

Using SerpApi and Media Cloud API , we extracted and filtered 15,750 articles covering left-leaning and right-leaning media. The articles were removed to cover the period from January 2020 to July 2021 using a list of 71 keywords (see Appendix B). The articles come from all the content published in the mainstream media, including some newswires and op-ed articles from which we extracted 169,432 quotes (also referred to as opinion spans or sentences). These quotes were further filtered using the main keywords Covid Vaccine and Coronavirus vaccine to 14,512 quotes. We then randomly selected and manually processed a total of 2,000 quotes (1,000 for Left-leaning and 1,000 for Right-leaning) which became our final dataset annotated by volunteer annotators.
A trained BERT classifier analyzed aspects of argumentation, how the different sides of the vaccine debate represent their own and each other’s opinions to determine if Left-Leaning and Right-Leaning media use framing devices and opinion attribution.  

**Our primary contributions are:**
1.	VacStance – a dataset of 2,000 stances annotated sentences.
2.	BERT – classifying the stance of a sentence, competitive with human performance,
3.	We provide a detailed analysis of generated data of the 169,432 Covid-19 vaccine opinions dataset, as well as the first diachronic analysis of the sources.


**GitHub Repository:** (https://github.com/ThoughtfulMind/VacStance)

**Annotation - Label Studio:** (http://annotation.vacstance.com/projects/)
**Note:** in order to be able to annotate data, you need to have a Label Studio account.











[Link](url) and ![Image](src)
```
