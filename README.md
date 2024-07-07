# Readability Optimiser

## Overview

Originally developed in my free time to practice Python, Readability Optimizer is a **prototype tool** designed to help authors improve the readability of their texts. This project marked one of my first endeavors in preparation for my upcoming Master's in Applied Data Science (MADS) at the University of Michigan.

The prototype created here later served as the foundation for an in-house solution, particularly for internal audit reports. This solution was expanded to **import** the audit report template and analyze all observation paragraphs for readability.

The tool employs various readability tests and analyses to provide insights and suggestions for enhancing text clarity and comprehension, thereby improving written communication in professional settings.

As part of the quick prototyping approach, the solution utilizes Streamlit, a popular Python library for building interactive web applications. It's worth noting that at the time of development in 2021, Streamlit did not support multipage navigation. Consequently, a custom workaround was implemented to achieve a multipage-like navigation experience within the application.

| Feature | Description |
|---------|-------------|
| Quick Check | Offers on-the-go text analysis |
| Readability Scores | Provides scores based on McAlpine EFLAW and Gunning Fog Index tests |
| Sentence Analysis | Checks sentence length |
| Sentiment Analysis | Analyzes sentiment and objectivity |
| Improvement Suggestions | Offers suggestions to enhance readability |
| Visual Statistics | Provides visual representation of analysis results |
| Jargon Check | Identifies potential jargon |
| Word Simplification | Suggests simpler alternatives for complex words |

## Future Development

There are several plans to enhance and expand the Readability Optimiser:

1. **Code Refactoring**: 
   - Review and refactor the existing codebase for improved clarity and efficiency.
   - Transition towards a more function-based approach to enhance modularity and maintainability.

2. **Integration of Local Large Language Models (LLMs)**:
   - Incorporate local LLMs to provide additional readability evaluation.
   - Leverage LLMs to generate more sophisticated improvement suggestions based on the results of rule-based readability tests.
   
3. **Adjusting scoring and rating thresholds**

These developments aim to make the Readability Optimiser more powerful, accurate, and user-friendly. Contributions and suggestions in these areas are welcome.

## Project Structure

    ├── README.md             <- The top-level README for developers using this project.
    ├── LICENSE               <- The license file for the project.
    ├── environment_conda.yml <- The requirements file for conda environments.
    │
    ├── data
    │
    ├── docs                  <- Documentation folder
    │
    ├── resources
    │   ├── list_difficult_words.csv
    │   ├── list_jargon_check.csv
    │   ├── list_simple_words.csv
    │   ├── rcBOT_config.ini
    │   └── release_notes.txt
    │
    ├── scripts
    │   ├── app.py
    │   ├── app1.py
    │   ├── app2.py
    │   └── func_readability.py
    │
    ├── .gitattributes
    └── .gitignore

## Installation

It's recommended to use `conda` as the foundation because it simplifies the management of required Python versions.

To create the project's conda environment, use:

```bash
conda env create -f environment_conda.yml
```

Once the environment is created, activate it:

```bash
conda activate readability
```

## Usage

1. Start the application with: `streamlit run scripts/app.py` from the project root folder
2. Choose Quick Check
3. Input your text
4. Review the analysis results and suggestions

## Readability Tests

### Readability and Readability Formulas

- Readability refers to how easy a piece of writing can be read. This depends on a range of factors including content, structure, style, layout and design.
- A readability formula is one of many methods of measuring or predicting the difficulty level of a text by analyzing the text.
- A conventional readability formula measures average word length and sentence length to provide a grade-level score.

**Advantages and Disadvantages**

| Pros | Cons |
|------|------|
| Measures grade-level readability | Readability ≠ understandability |
| Provides information to reach target audience | Cannot measure "real" word/phrase complexity |
| Saves time by predicting reader understanding | Results may vary between formulas |
| Easy-to-use, text-based formulas | Cannot measure context, prior knowledge, or concept difficulty |
| Helps convert to plain language | |
| Can increase reader retention and comprehension | |

### Thresholds and Scoring

The Readability Optimiser uses the following thresholds for various readability checks:

| Measure | Recommended Threshold |
|---------|------------------------|
| Maximum Sentence Length | 20 words or lower |
| Flesch Reading Ease Score (FRES) | 49 or higher |
| EFLAW Score | 25 or lower |
| Gunning Fog Score (GFS) | 17 or lower |
| Consensus Score | 18 or lower |

These thresholds serve as benchmarks for evaluating the readability of the text. Scores that meet or exceed these thresholds (in the appropriate direction) indicate better readability.

### McAlpine EFLAW

The McAlpine EFLAW test helps to determine the readability for individuals for which English is a foreign language. The test is based on two significant and typical flaws:
- long sentences and
- a high proportion of mini-words (3 or fewer characters).

Both these flaws could confuse readers:
- Long sentences are normally decreasing the readability for people who are learning English as a foreign language.
- Mini-words are confusing because they have many meanings and are often a sign of wordiness or idioms.

The EFLAW formula is:

```
EFLAW Score = (total words + miniwords) / total sentences
```

| Score | Rank |
|-------|------|
| 1-20  | very easy to understand |
| 21-25 | (quite) easy to understand |
| 26-29 | a little difficult |
| 30+   | very confusing |

### Gunning Fog Index

The Gunning Fog formula generates a grade level between 0 and 20. It estimates the education level required to understand the text on first reading. A Gunning Fog score of 6 is easily readable for sixth-graders. Text aimed at the public should aim for a grade level of around 8. Text above a 17 has a graduate level.

The Gunning Fog formula is:

```
Fog Index = 0.4 x [(total words / total sentences) + 100 (complex words / total words)]
```

| Fog Index | Reading level by grade |
|-----------|------------------------|
| > 18      | Beyond college graduate |
| 17        | College graduate |
| 16        | College senior |
| 15        | College junior |
| 14        | College sophomore |
| 13        | College freshman |
| 12        | High school senior |
| 11        | High school junior |
| 10        | High school sophomore |
| 9         | High school freshman |
| 8         | Eighth grade |
| 7         | Seventh grade |
| 6         | Sixth grade |

## Sentence Length

The recommended sentence length is 20 words following the "Audit Report Writing Style Guide".
The following sources also support this recommended length:

### American Press Institute (API)
The longer the sentences, the less readers understand, according to research by the American Press Institute (API). The research, based on studies of 410 newspapers, correlated the average number of words in a sentence with reader comprehension. They found:

| Sentence Length | Reader Comprehension |
|-----------------|----------------------|
| 8 words or less | 100% |
| 14 words | 90% |
| 43 words or more | Less than 10% |

### Oxford Guide to Plain English
Author Martin Cutts makes the following recommendation in the Oxford Guide To Plain English:
"…make the average sentence length 15–20 words… More people fear snakes than full stops, so they recoil when a long sentence comes hissing across the page."

Source: https://read.amazon.co.uk/kp/embed?asin=B00FZSX76G&preview=newtab&linkCode=kpe&ref_=cm_sw_r_kb_dp_aFkyCbSKPGCZN

### Plainlanguage.gov
Write short sentences: Sentences loaded with dependent clauses and exceptions confuse the audience by losing the main point in a forest of words.

Source: https://www.plainlanguage.gov/guidelines/concise/write-short-sentences/

## Sentiment and Objectivity

Sentiment analysis is the process of determining the attitude or the emotion of the writer, i.e., whether it is positive or negative or neutral.

The tool uses the TextBlob library to determine the sentiment and objectivity. For this analysis Textblob returns two properties, polarity, and subjectivity:

| Measure | Range | Interpretation |
|---------|-------|----------------|
| Polarity | -1 to 1 | -1 (negative) to 1 (positive) |
| Subjectivity | 0 to 1 | 0 (objective) to 1 (subjective) |

Texblob uses its own lexicon for sentiment analysis: https://github.com/sloria/TextBlob/blob/eb08c120d364e908646731d60b4e4c6c1712ff63/textblob/en/en-sentiment.xml

Each word in the lexicon has scores for:
- polarity: negative vs. positive (-1.0 => +1.0)
- subjectivity: objective vs. subjective (+0.0 => +1.0)
- intensity: (x0.5 => x2.0)

TextBlob goes along finding words and phrases it can assign polarity and subjectivity to, and it averages them all together for longer text.

## Jargon to be Reviewed

Based on a jargon list compiled from different sources:
- Gartner: Writing Cheat Sheet (internal document)
- EY: Impactful Reporting for Internal Auditors (internal document)

This is not directly linked to one of the readability scores. However, avoiding jargon should improve the readability in general.

## Words to be Simplified

- Simple word list based on plainlanguage.gov: https://www.plainlanguage.gov/guidelines/words/use-simple-words-phrases/ 
This is not directly linked to one of the readability scores. However, using "simpler" words should improve the readability in general.

