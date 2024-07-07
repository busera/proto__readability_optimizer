"""
## Purpose
Containing functions to pre-process the text and calculate the readability scores.
---
# Functions
"""

## Packages
import pandas as pd
import altair as alt
import streamlit as st  # to render streamlit webpage
import csv  # to process csv files
import textstat  # to calculate text statistics
import re  # to find and calculate syllables in a word
from textblob import TextBlob  # for Sentiment Analysis
from icecream import ic  # to easily print variables (testing)


# --- Global Parameters ---
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


def make_url_link(URL, text):
    """Takes a "link text", "URL target" and returns a url link in html a tag format.
    
    Args:
        URL (string): URL in the format www.somename.com/somewhere/
        text (string): The link text.

    Returns:
        link (string): a url link in html a tag format
        
    """
    
    link = f'<a target="_blank" href="{URL}">{text}</a>'
    
    return link


def load_external_lists():
    """Function to load external csv-word lists.

    Returns:
        dict_jargon (dict): Jargon phrases and words
        dict_simplewords (dict): Words which could be simplified (incl. alternatives)
        list_difficult_words (list): Difficult words which can be ignored as difficult
    """

    ## list of jargon words which should be avoided
    list_jargon_check = r"resources/list_jargon_check.csv"

    ## list of words which could be simplified
    list_simple_words = r"resources/list_simple_words.csv"

    ## list of "difficult words" which can be "ignored" as difficult
    list_difficult_words = r"resources/list_difficult_words.csv"

    with open(list_jargon_check, 'r') as list_jc:
        dict_jargon = dict(filter(None, csv.reader(list_jc, delimiter=";")))

    with open(list_simple_words, 'r') as list_sw:
        dict_simplewords = dict(filter(None, csv.reader(list_sw, delimiter=";")))

    ## load list of "difficult words" which can be "ignored"
    with open(list_difficult_words, 'r') as list_dw:
        fileimport = list_dw.read()
        list_difficult_words = fileimport.split(",")

    return dict_jargon, dict_simplewords, list_difficult_words


def count_syllables(word):
    """Custom function to calculate syllables in a word. This function is **not used** with the actual readability scores.
        
        Args:
            word (string): Single word which should be analyzed for syllables
        
        Returns:
            syllables_count (int): Number of syllables found
    """
    
    syllables_count = len(re.findall('(?!e$)[aeiouy]+', word, re.I) + re.findall('^[^aeiouy]*e$', word, re.I))

    return syllables_count


def text_statistics(i, observation):
    """Function to calculate test statistics."""
    _, _, list_difficult_words = load_external_lists()
    """Function to calculate the text statistics."""
    observation = observation.replace("\n", ". ")

    # Set language
    textstat.set_lang("en")

    # Count words
    lexiconcount = textstat.lexicon_count(observation, removepunct=True)

    # Count sentences
    sentencecount = textstat.sentence_count(observation)

    # Count syllable
    syllablecount = textstat.syllable_count(observation)

    # Ratio words to sentences
    word_sentence_ratio = int(lexiconcount/sentencecount)

    # Difficult words
    diffcultwords_list = textstat.difficult_words_list(observation)
    diffcultwords_list.sort()
    # diffcultwords_num = textstat.difficult_words(observation)
    diffcultwords_num = 0

    diffcultwords_list_string = ""
    for aword in diffcultwords_list:
        count_syll = count_syllables(aword)
        if count_syll >= 4 and aword not in list_difficult_words:
            diffcultwords_list_string = f'{diffcultwords_list_string} {aword} [{str(count_syll)}],\n\n\n'
            diffcultwords_num += 1

    observation_no = i+1  # add +1 to the observation lenght count to make it "human" readable

    return observation_no, lexiconcount, sentencecount, syllablecount, word_sentence_ratio, diffcultwords_list_string, diffcultwords_num

"""
## TODO Verify if still used??
def observation_selection_list():
    observation_selection_list = []
    for obs in range(gl_amount_of_observations):
        observation_selection_list.append(str(obs+1))
    observation_selected = st.sidebar.selectbox(
        "Observation No. selected:", observation_selection_list)

    return(observation_selected)
"""

def readability_gfogs(i, observation):
    """Function to calculate the Gunning FOG score and rank."""
    # Gunning FOG score
    gfs = ""
    gfsrank = ""
    gfs = textstat.gunning_fog(observation)

    # Rank Gunning FOG score
    if gfs < 6:
        gfsrank = "Below sixth grade."
    elif gfs >= 6 and gfs < 7:
        gfsrank = "6th grade level."
    elif gfs >= 7 and gfs < 8:
        gfsrank = "7th grade level."
    elif gfs >= 8 and gfs < 9:
        gfsrank = "8th grade level."
    elif gfs >= 9 and gfs < 10:
        gfsrank = "High school freshman level."
    elif gfs >= 10 and gfs < 11:
        gfsrank = "High school sophomore level."
    elif gfs >= 11 and gfs < 12:
        gfsrank = "High school junior level."
    elif gfs >= 12 and gfs < 13:
        gfsrank = "High school senior level."
    elif gfs >= 13 and gfs < 14:
        gfsrank = "College freshman level."
    elif gfs >= 14 and gfs < 15:
        gfsrank = "College sophomore level."
    elif gfs >= 15 and gfs < 16:
        gfsrank = "College junior level."
    elif gfs >= 16 and gfs < 17:
        gfsrank = "College senior level."
    elif gfs >= 17 and gfs < 18:
        gfsrank = "College graduate level."
    elif gfs >= 18:
        gfsrank = "Beyond college graduate level."

    #observation_stats_list[i]['gunning_fog_score'] = int(gfs)
    #observation_stats_list[i]['gunning_fog_rank'] = gfsrank
    #observation_stats_list[i]['gunning_fog_score_rank'] = f"{str(int(gfs))}: {gfsrank}"
    gunning_fog_score_rank = f"{str(int(gfs))}: {gfsrank}"

    return int(gfs), gfsrank, gunning_fog_score_rank


def text_cleanup(observation):
    """Function to do some simple text clean-up. TODO: replace with a regex pattern.
    """
    observation = observation.replace("approx.", "approx")
    observation = observation.replace("1.", "1")
    observation = observation.replace("2.", "2")
    observation = observation.replace("3.", "3")
    observation = observation.replace("4.", "4")
    observation = observation.replace("5.", "5")
    observation = observation.replace("e.g.", "eg")
    observation = observation.replace("i.e.", "ie")
    observation = observation.replace("min.", "min")
    observation = observation.replace("max.", "max")
    observation = observation.replace("dept.", "dept")
    observation = observation.replace("misc.", "misc")
    observation = observation.replace("p.a.", "pa")
    observation = observation.replace("p.m.", "pm")
    observation = observation.replace("avg.", "avg")
    observation = observation.replace("fig.", "fig")
    observation = observation.replace("vs.", "vs")
    observation = observation.replace("etc.", "etc")
    observation = observation.replace(".", "")
    observation = observation.replace("•", "-")
    observation = observation.replace("       ", " ")
    print("clean obs:",observation)  # testing

    return observation


def eflaw(i, observation):
    """Function to calculate the McAlpine EFLAW score and rank.

    Args:
        i (int): Iterator
        observation (string): Observation text
    
    Returns:
        eflaw_score (int): eflaw score
        eflaw_rank (string): eflaw rank
        eflaw_score_rank (string): eflaw score and rank
        count_sentences (int): Number of sentences in this text.
        sentence_length_dict (dict): Sentence position + sentence length
        count_miniwords (int): Number of identified mini words 
    """
    observation = text_cleanup(observation)
    observation = observation.replace(". ", "\n")
    # using "\n " for splitting to avoid to break e.g. or 1. into sentences
    sentences_list = observation.split("\n")

    while '' in sentences_list:
        sentences_list.remove('')
    while ' ' in sentences_list:
        sentences_list.remove(' ')

    # Let W, M and S be the number of words, miniwords and sentences in a text.
    # Then EFLAW Score = (W+M)/S.
    # The lower the score, the fewer the flaws, she says and recommends a score of 25 or lower.
    # And here is the scale:
    # 1-20 (very easy to understand);
    # 21-25 (quite easy to understand);
    # 26-29 (a little difficult); and 30+ (very confusing).
    eflaw_rank = ""
    eflaw_score = ""
    word_list = []
    count_words = 0
    count_miniwords = 0
    count_sentences = 0
    sentence_length_dict = {}

    for sentence in range(len(sentences_list)):
        word_list = sentences_list[sentence].split()
        if len(word_list) > 4:  # to avoid to count headlines as sentences; only count sentences with words > 4
            count_sentences += 1
            # Set dictionary to store sentence no, lenght and actual sentence under "SentNo. x"
            sentence_length_dict['SentNo.'+str(count_sentences)] = {}
            sentence_length_dict['SentNo.' +
                                 str(count_sentences)]['Sentence No'] = int(count_sentences)
            # add sentence no and word count to dict
            sentence_length_dict['SentNo.' +
                                 str(count_sentences)]['Words'] = len(word_list)
            sentence_length_dict['SentNo.' +
                                 str(count_sentences)]['Sentence'] = sentences_list[sentence]
        count_words += len(word_list)

        for word in word_list:
            if len(word) <= 3:
                #print(word)  # testing
                count_miniwords += 1
    eflaw_score = (count_words+count_miniwords)/count_sentences

    # Rank EFLAW score
    if eflaw_score <= 20:
        eflaw_rank = "Very easy to understand."
    elif eflaw_score > 20 and eflaw_score <= 25:
        eflaw_rank = "Easy to understand."
    elif eflaw_score > 25 and eflaw_score <= 29:
        eflaw_rank = "Difficult to understand."
    elif eflaw_score > 29:
        eflaw_rank = "Very confusing."

    eflaw_score_rank = f"{int(eflaw_score)}: {eflaw_rank}"

    return int(eflaw_score), eflaw_rank, eflaw_score_rank, int(count_sentences), sentence_length_dict, int(count_miniwords)


def long_sentences(i, observation):
    """Function to find long sentences according to the threshold."""
    sentences_list = []
    observation = text_cleanup(observation)
    observation = observation.replace(". ", "\n")
    sentences_list = observation.split("\n")

    # Removing empty list entries such as "" and " "
    sentences_list = [sentence for sentence in sentences_list if len(sentence) > 1]
    #ic(sentences_list)
    
    word_list = []
    count_long_sentences = 0

    for sentence in range(len(sentences_list)):
        word_list = sentences_list[sentence].split()
        ic(len(word_list))
        if len(word_list) > recommended_sentence_lengh_max:
            count_long_sentences += 1

    return count_long_sentences


def jargon_checker(i, observation):
    """Function to find jargon phrases."""
    dict_jargon, _, _ = load_external_lists()

    # text cleansing for jargon checker
    observation_cleaned = observation.replace("\n", " ").lower()
    observation_cleaned = observation_cleaned.replace(",", "")
    observation_cleaned = observation_cleaned.replace("  ", " ")

    jargon_checklist = ""
    jargon_checklist_dict = dict()
    for jargon in dict_jargon.keys():
        if jargon in observation_cleaned:
            jargon_checklist += (f"{jargon} >> {dict_jargon[jargon]}\n\n")
            jargon_checklist_dict[jargon] = dict_jargon[jargon]
    if jargon_checklist == "":
        jargon_checklist = "No jargon found."
    #observation_stats_list[i]['jargon_checklist'] = jargon_checklist
    #bservation_stats_list[i]['jargon_checklist_dict'] = jargon_checklist_dict

    return jargon_checklist, jargon_checklist_dict


def simplewords_checker(i, observation):
    """Function to find word which could be replaced with simpler versions."""
    _, dict_simplewords, _ = load_external_lists()

    # text cleansing for jargon checker
    observation_cleaned = observation.replace("\n", " ").lower()
    observation_cleaned = observation_cleaned.replace(",", "")
    observation_cleaned = observation_cleaned.replace("  ", " ")

    simplewords_checklist = ""
    simplewords_checklist_dict = dict()
    for simpleword in dict_simplewords.keys():
        if simpleword in observation_cleaned:
            simplewords_checklist += (
                f"{simpleword} >> {dict_simplewords[simpleword]}\n\n")
            simplewords_checklist_dict[simpleword] = dict_simplewords[simpleword]

    if simplewords_checklist == "":
        simplewords_checklist = "No words be simplified."
    #observation_stats_list[i]['simplewords_checklist'] = simplewords_checklist
    #observation_stats_list[i]['simplewords_checklist_dict'] = simplewords_checklist_dict
    return simplewords_checklist, simplewords_checklist_dict


def improvement_suggestions(i, observation_stats_list):
    """Function to define/formualte the improvement suggestions based on the thresholds."""
    improvement_suggestions = ""
    if observation_stats_list[i]['eflaw_score'] > recommended_score_eflaw:
        if observation_stats_list[i]['jargon_checklist'] != "No jargon found.":
            improvement_suggestions += "Review and replace the jargons, where possible (see table below).\n\n"
        # if observation_stats_list[i]['word_sentence_ratio'] > recommended_sentence_lengh_max :
        improvement_suggestions += f"Reduce the size of the {observation_stats_list[i]['long_sentences']} lengthy sentences.\n\n"
        improvement_suggestions += f"Reduce the use of the {observation_stats_list[i]['eflaw_miniwords_count']} mini words (words with less <= 3 characters).\n\n"
        improvement_suggestions += "\n\n"
    else:
        improvement_suggestions = "None. All good here."

    #observation_stats_list[i]['improvement_suggestions'] = improvement_suggestions
    return improvement_suggestions


def sentiment_analysis(i, observation):
    """Function to calculate the sentiment."""
    # Textblob Sentiment Analysis
    # TextBlob Scoring:
    # The polarity score is a float within the range [-1.0, 1.0].
    # The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
    # polarity is >0, it is considered positive,
    # <0 -is considered negative and
    # ==0 is considered neutral.
    result_sentiment = ''
    blob = TextBlob(observation)
    result_sentiment = blob.sentiment

    bob_result_polarity = ""
    bob_result_subjectivity = ""

    if result_sentiment[0] <= -0.5:
        bob_result_polarity = "very negative"
    elif result_sentiment[0] >= -0.5 and result_sentiment[0] < -0.25:
        bob_result_polarity = "negative"
    elif result_sentiment[0] >= -0.25 and result_sentiment[0] < 0.25:
        bob_result_polarity = "neutral"
    elif result_sentiment[0] >= 0.25 and result_sentiment[0] < 0.5:
        bob_result_polarity = "postive"
    elif result_sentiment[0] >= 0.75:
        bob_result_polarity = "very postive"

    if result_sentiment[1] >= 0 and result_sentiment[1] < 0.25:
        bob_result_subjectivity = "very objective"
    elif result_sentiment[1] >= 0.25 and result_sentiment[1] < 0.5:
        bob_result_subjectivity = "objective"
    elif result_sentiment[1] >= 0.5 and result_sentiment[1] < 0.75:
        bob_result_subjectivity = "subjective"
    elif result_sentiment[1] >= 0.75:
        bob_result_subjectivity = "very subjective"

    #observation_stats_list[i]['bob_result_polarity'] = bob_result_polarity
    #observation_stats_list[i]['bob_result_subjectivity'] = bob_result_subjectivity
    return bob_result_polarity, bob_result_subjectivity


def export_csv(df_obs):
    """Export CSV file to specified folder.

        Args:
            df_obs (dataframe): Dataframe with observation details
        
        Returns:
            None
    """

    # Define export path and file name
    export_file_name = "observation-full-table.csv"
    export_path = r'c:/pyBOTS/rcBOT/reports/'
    export01 = export_path+export_file_name

    # Create export df and write csv file
    #df_export= df_obs.drop(['sentence_length_dict','observation_summary_result','diffcult_words_list','jargon_checklist_dict','simplewords_checklist_dict','eflaw_score','eflaw_rank','sentences'], axis=1)
    df_export = df_obs[['Observation No.', 'eflaw_score_rank', 'gunning_fog_score_rank', 'improvement_suggestions',
                        'eflaw_sentencecount', 'eflaw_miniwords_count', 'words', 'long_sentences', 'jargon_checklist', 'simplewords_checklist', 'bob_result_polarity', 'bob_result_subjectivity']]
    df_export.to_csv(export01, index=None, header=True)


def render_bar_chart(i, observation_stats_list):
    """Creates a bar chart to display the length of each sentence.

    Args:
        i (int): Iterator
        observation_stats_list (list): List of dictionaries

    Returns:
        bar_chart (LayerChart): Altair layered bar chart
    """

    barchartdata = pd.DataFrame(observation_stats_list[i]['sentence_length_dict'])
    barchartdata = barchartdata.transpose()
    hline = alt.Chart(pd.DataFrame({'Limit': [recommended_sentence_lengh_max]})).mark_rule(color="red").encode(y='Limit')
    barchartwordcount = alt.Chart(barchartdata).mark_bar().encode(
        x=alt.X('Sentence No:O', sort=None), y='Words:Q', tooltip=['Sentence No', 'Words', 'Sentence']).properties(
        width=670,
        height=300
    )
    
    bar_chart = barchartwordcount + hline

    return bar_chart
