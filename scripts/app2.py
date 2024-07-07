"""
## Purpose
Section to anaylze input text **ad-hoc (quick check)**.
The user can type or paste text into the **input field**.
Readability scores are calculated after the `[Analyze]` button is pressed.


## Key Elements/Variables
### observation_stats_list (list)
All results, statistics and details are stored in a **dictionary** within a **list**, the **observation_stats_list**. The list was used to create a dictionary per 
observation paragraph and append it to the list (this was relevant for the analyzing all observations of an audit report.)
A list of dictionaries.
\n\n
In case of the **Quick Check** the list only contains **one dictionary** with the following **keys**:
```shell
dict_keys(['Observation No.', 
           'eflaw_score', 
           'eflaw_rank', 
           'eflaw_score_rank', 
           'eflaw_sentencecount', 
           'sentence_length_dict', 
           'eflaw_miniwords_count',
           'gunning_fog_score', 
           'gunning_fog_rank',
           'gunning_fog_score_rank', 
           'observation_no', 
           'words', 
           'sentences', 
           'syllables', 
           'word_sentence_ratio', 
           'diffcult_words_list', 
           'diffcult_words_num', 
           'long_sentences',
           'jargon_checklist', 
           'jargon_checklist_dict', 
           'simplewords_checklist', 
           'simplewords_checklist_dict', 
           'improvement_suggestions', 
           'bob_result_polarity', 
           'bob_result_subjectivity'
           ])
```

#### Example
Input text: `This is a quick reader check test.`
```py3
[{'Observation No.': 1,
  'bob_result_polarity': 'postive',
  'bob_result_subjectivity': 'subjective',
  'diffcult_words_list': ' readability [5],
  'diffcult_words_num': 1,
  'eflaw_miniwords_count': 2,
  'eflaw_rank': 'Very easy to understand.',
  'eflaw_score': 9,
  'eflaw_score_rank': '9: Very easy to understand.',
  'eflaw_sentencecount': 1,
  'gunning_fog_rank': '8th grade level.',
  'gunning_fog_score': 8,
  'gunning_fog_score_rank': '8: 8th grade level.',
  'improvement_suggestions': 'None. All good here.',
  'jargon_checklist': 'No jargon found.',
  'jargon_checklist_dict': {},
  'long_sentences': 0,
  'observation_no': 1,
  'sentence_length_dict': {'SentNo.1': {'Sentence': 'This is a quick readability check test.',
                                        'Sentence No': 1,
                                        'Words': 7
                                        }
                          },
  'sentences': 1,
  'simplewords_checklist': 'No words be simplified.',
  'simplewords_checklist_dict': {},
  'syllables': 10,
  'word_sentence_ratio': 7,
  'words': 7}]
```
---
# Functions
"""


# Importing packages
import streamlit as st  # to render streamlit webpage
import pandas as pd  # to store text, stats, scores and results
import func_readability as rc  # to import the readability algorithms
import func_logging as func_logging  # for logging functionality


# --- Global Parameters ---
## Thresholds for the various readability checks
recommended_sentence_lengh_max = 20  # or lower
recommended_score_fres = 49  # or higher
recommended_score_eflaw = 25  # or lower
recommended_score_gfs = 17  # or lower
recommended_score_cons = 18  # or lower
# --- Global Parameters ---


# --- Global Variables ---
observation_no = 0
observation = ""
gl_data = []
gl_amount_of_observations = 0
observation_stats_list = []
# --- Global Variables ---


def check_word_count(observation_input):
    """Splite the input text on space " " and calculates the list length.
    This check is required, because for the readability calcualtion the text length needs to be 5 words or longer.
    A quick (and dirty) check is sufficient. No text clean-up is required for this function/check.

    Args:
        observation_input (string): Input text

    Returns:
        word_list_len (int): Length of the word list
    """

    word_list_len = len(observation_input.split(" "))

    return word_list_len


def app():
    """Main function which renders the streamlit webpage and calls the functions."""

    st.subheader('Quick Check Page')

    observation_input = st.text_area(
        'Text to be analyzed:', '')

    ## If the "Analyze" button is pressed, execute the following:
    if st.button('Analzye'):  

        # The quick check input text needs a minimum length of 5 words
        if check_word_count(observation_input) < 5:
            st.error('Attention: Sentence needs to have 5 or more words.')
        else:

            ## Starting logging (primarily for bot usage statistics)
            message = 'QUICK CHECK triggered.'
            func_logging.trigger_logging(message)

            ## Calculate scores and render readability report
            st.title("Readability Report")
            observation_no = 0  # For the quick check this is a static number
            i = int(observation_no)
            observation = observation_input

            ## Add first empty dictionary to observation stats list
            observation_stats_list.append({})

            ## Assign observation No.: iterator
            observation_stats_list[i]['Observation No.'] = i+1

            ## Getting eflaw-based stats and score from the "eflaw" function
            observation_stats_list[i]['eflaw_score'], observation_stats_list[i]['eflaw_rank'], observation_stats_list[i]['eflaw_score_rank'], observation_stats_list[i][
                'eflaw_sentencecount'], observation_stats_list[i]['sentence_length_dict'], observation_stats_list[i]['eflaw_miniwords_count'] = rc.eflaw(i, observation)

            ## Getting the gunning_fog-based stats and score from the "readability_gfogs" function
            observation_stats_list[i]['gunning_fog_score'], observation_stats_list[i][
                'gunning_fog_rank'], observation_stats_list[i]['gunning_fog_score_rank'] = rc.readability_gfogs(i, observation)

            ## Getting stats from the "text_statistics" function
            observation_stats_list[i]['observation_no'], observation_stats_list[i]['words'], observation_stats_list[i]['sentences'], observation_stats_list[i]['syllables'], observation_stats_list[
                i]['word_sentence_ratio'], observation_stats_list[i]['diffcult_words_list'], observation_stats_list[i]['diffcult_words_num'] = rc.text_statistics(i, observation)

            ## Getting long sentence count from the "long_sentences" function
            observation_stats_list[i]['long_sentences'] = rc.long_sentences(i, observation)

            ## Getting jargon words from the "jargon_checker" function
            observation_stats_list[i]['jargon_checklist'], observation_stats_list[i]['jargon_checklist_dict'] = rc.jargon_checker(i, observation)
            
            ## Getting word to be simplified from the "implewords_checker" function
            observation_stats_list[i]['simplewords_checklist'], observation_stats_list[i]['simplewords_checklist_dict'] = rc.simplewords_checker(i, observation)

            ## Getting improvement suggestions from the "improvement_suggestions" function
            observation_stats_list[i]['improvement_suggestions'] = rc.improvement_suggestions(i, observation_stats_list)

            ## Getting sentiment from the "sentiment_analysis" function
            observation_stats_list[i]['bob_result_polarity'], observation_stats_list[i]['bob_result_subjectivity'] = rc.sentiment_analysis(i, observation)
            
            print("observation_stats_list:", observation_stats_list[i])  # for testing

            ## -------------------------------------------------------------------------
            ## Render/Display Readability Report
            ## -------------------------------------------------------------------------

            ## Render/Display Readability Scores ---------------------------------------
            st.subheader('Readability Scores')

            # Defining two columns with a 1 to 3 ratio
            col_rs1, col_rs2 = st.columns([1, 3])

            ## Print scores and rand
            ## Assigning dictionary values in separate variables for an easier reference
            eflaw_score = observation_stats_list[i]['eflaw_score']
            eflaw_rank = observation_stats_list[i]['eflaw_rank']
            gfog_score = observation_stats_list[i]['gunning_fog_score']
            gfog_rank = observation_stats_list[i]['gunning_fog_rank']

            if int(observation_stats_list[i]['eflaw_score']) > recommended_score_eflaw:
            ## If score above threshold print red box (error) box
                col_rs1.error(f'EFLAW: {eflaw_score}')
                col_rs2.error(
                    f'{eflaw_rank} Target is {recommended_score_eflaw} or lower.')

            else:
            ## If score below threshold print green (success) box
                col_rs1.success(f'EFLAW: {eflaw_score}')
                col_rs2.success(eflaw_rank)

            if int(observation_stats_list[i]['gunning_fog_score']) > recommended_score_gfs:
                ## If score above threshold print red box (error) box
                col_rs1.error(f'GFOGS: {gfog_score}')
                col_rs2.error(
                    f'{gfog_rank} Target is {recommended_score_gfs} or lower.')

            else:
                ## If score below threshold print green (success) box
                col_rs1.success(f'GFOGS: {gfog_score}')
                col_rs2.success(gfog_rank)


            st.write('')
            st.write('')

            ## Render/Display Sentence Length Result ---------------------------------------
            st.subheader('Sentence Length')
            if int(observation_stats_list[i]['long_sentences']) > 0:
                long_sen = observation_stats_list[i]['long_sentences']
                total_sen = observation_stats_list[i]['eflaw_sentencecount']
                st.error(f'{long_sen} out of {total_sen} sentences are longer than the recommended {recommended_sentence_lengh_max} words.\n\n')
            else:
                st.success(f'All sentences are within the recommended length of {recommended_sentence_lengh_max} words.')

            st.write('')
            st.write('')

            ## Render/Display Sentiment and Objectivity ---------------------------------------
            st.subheader('Sentiment and Objectivity')
            st.write('Analysis is based on public library (not audit-specific, yet):')
            polarity = observation_stats_list[i]['bob_result_polarity']
            objectivity = observation_stats_list[i]['bob_result_subjectivity']

            if polarity == "neutral":
                st.success(f'The text has a {polarity} sentiment.')
            else:
                st.error(f'The text has a {polarity} sentiment.')

            if objectivity == "objective" or objectivity == "very objective":
                st.success(f'The text is written in an {objectivity} manner.')
            else:
                st.error(f'The text is written in an {objectivity} manner.')

            st.write('')
            st.write('')

            ## Render/Display Improvement Suggestions ---------------------------------------
            st.subheader('Improvement Suggestions')
            st.write(observation_stats_list[i]['improvement_suggestions'])

            st.write('')
            st.write('')

            ## Render/Display Text Statistics and Bar Chart ---------------------------------------
            st.subheader('Text Statistics')

            ## Creating a dataframe based on the observation_stats_list, to display details as table
            df_obs = pd.DataFrame(observation_stats_list)
            st.table(df_obs.loc[i, ['words', 'eflaw_sentencecount', 'word_sentence_ratio', 'long_sentences']])
            st.write(' \n\n')

            ## Render/display bar chart for sentence length
            bar_chart = rc.render_bar_chart(i, observation_stats_list)
            st.write(bar_chart)

            st.write('')
            st.write('')

            ## Render/Display Jargon to be Reviewed ---------------------------------------
            st.subheader('Jargon to be Reviewed')

            ## Creating a dataframe based on the observation_stats_list, to display details as table
            df_jargon = pd.DataFrame(observation_stats_list[i]['jargon_checklist_dict'].items(
            ), columns=['Jargon', 'Replace with'])
            st.table(df_jargon)

            st.write('')
            st.write('')

            ## Render/Display Words to be Simplified ---------------------------------------
            st.subheader('Words to be Simplified')

            ## Creating a dataframe based on the observation_stats_list, to display details as table
            df_simplewords = pd.DataFrame(observation_stats_list[i]['simplewords_checklist_dict'].items(
            ), columns=['Words', 'Replace with'])
            st.table(df_simplewords)

            ## Render/Display Content for SIDEBAR ---------------------------------------
            st.sidebar.write('')
            st.sidebar.write('---')
            st.sidebar.subheader("Recommended Scores")
            st.sidebar.write(f'Sentence lenght: {recommended_sentence_lengh_max} or shorter')
            st.sidebar.write(f'EFLAW: {recommended_score_eflaw} or lower')
            st.sidebar.write(f'GFOGS: {recommended_score_gfs} or lower')
            st.sidebar.write('---')
            st.sidebar.subheader("Abbreviations")
            st.sidebar.write('EFLAW: McAlpine EFLAW Score')
            st.sidebar.write('GFOGS: Gunning Fog Score')

            st.sidebar.write('---')
            URL = ''
            text = 'user manual'
            link = rc.make_url_link(URL, text)
            st.sidebar.subheader("Readability Test Insights")
            st.sidebar.write(f'More insights regarding EFLAW and GFOGS are available in the {link}. See section "Readability Tests".', unsafe_allow_html=True)
