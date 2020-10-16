# System imports
import argparse
import json
import copy
from string import Template
from collections import OrderedDict
import os
import sys
# local imports
import config

# new template files can be created in Qualtrics by creating a
# question with your specifications and exporting the survey file
json_filename = "combined-template.json"
save_as = "output-survey.qsf"
# audio templates should not be changed
audio_html_template = "audio_template.html"
play_button = "play_button.html"

# load JSON template from file
def get_basis_json():
    with open(json_filename) as json_file:
        return json.load(json_file)

# standard audio player for all question types except MUSHRA
def get_player_html(url):
    with open(audio_html_template) as html_file:
        return Template(html_file.read()).substitute(url=url)

# audio player with only play/pause controls for MUSHRA tests
# to prevent participants identifying hidden reference by duration
def get_play_button(url, n): # player n associates play button with a specific audio
    with open(play_button) as html_file:
        return Template(html_file.read()).substitute(url=url, player=n)

# makes lists of formatted urls from the filenames in the config file
def format_urls(question_type, file_1, file_2=None, file_3=None):
    with open(file_1) as f1:
        try:
            with open(file_2) as f2: # only -ab & -abc have >1 url file
                if question_type == 'ab': # returns list of url pairs
                    return [(line1.split()[1],line2.split()[1])\
                            for line1, line2 in zip(f1,f2)]
                elif question_type == 'abc':
                    with open(file_3) as f3: # returns list of url trios
                        return [(line1.split()[1],line2.split()[1],line3.split()[1])\
                                for line1, line2, line3 in zip(f1, f2, f3)]
        except:
            if question_type == 'mc' or question_type == 'trs':
                names, urls = zip(*(l.split(' ', 1) for l in f1))
                return urls, names
            elif question_type == 'mushra': # returns test & reference url lists
                lines = f1.readlines() # ref audio is embedded in the question
                ref_url_list =  [os.path.join
                                        (config.mushra_root,
                                        config.mushra_ref_folder,
                                        line.replace("\n", ""))
                                for line in lines]
                # creates list containing sets of urls which vary only by folder name
                test_url_list = [[os.path.join(config.mushra_root, folder,
                                line.replace("\n", "")) for folder in config.mushra_folders]
                                for line in lines]
                return test_url_list, ref_url_list

# load sentences from text file, to be embedded into MC question text
def get_sentences(sentence_file):
    lines = open(sentence_file, encoding="utf8").readlines()
    return {line.split(' ', 1)[0] : line.split(' ', 1)[1].replace('\n', '') for line in lines}

# make a new question using basis question and urls
def make_question(qid, urls, basis_question, question_type,
                  question_function, question_text):
    new_question = copy.deepcopy(basis_question)
    # Set the survey ID
    new_question['SurveyID'] = config.survey_id
    # Change all the things that reflect the question ID
    new_question['Payload']['QuestionID'] = f'QID{qid}'
    new_question['Payload']['DataExportTag'] = f'QID{qid}'
    new_question['PrimaryAttribute'] = f'QID{qid}'
    new_question["SecondaryAttribute"] = f'QID{qid}: {question_type}'
    new_question["Payload"]["QuestionDescription"] = f'QID{qid}: {question_type}'
    # set the question text
    new_question["Payload"]["QuestionText"] = question_text
    try: # call handler function for each question type
        question_function(new_question, urls, qid)
    except TypeError:
        pass
    return new_question

# handler function for mc questions
def mc_q(new_question, urls=None, qid=None):
    new_question['Payload']['Choices']['1']['Display'] = "Yes"  # add the choices
    new_question['Payload']['Choices']['2']['Display'] = "No"
    return new_question

# handler function for ab/abc questions
def ab_q(new_question, urls, qid=None):
    choice_template = new_question['Payload']['Choices']['1']# make choice template
    # empty 'Choices' so flexible number can be added using Choice template
    new_question['Payload']['Choices'] = {}
    for i, url in enumerate(urls):
        choice = copy.deepcopy(choice_template)
        choice['Display'] = get_player_html(url) # add audio player as choice
        new_question['Payload']['Choices'][f'{i+1}'] = choice
    return new_question

 # handler function for mushra questions
def mushra_q(new_question, urls, qid):
    choice_template = new_question['Payload']['Choices']['1']# make choice template
    # empty 'Choices' so flexible number can be added using Choice template
    new_question['Payload']['Choices'] = {}
    for i, url in enumerate(urls):
        choice = copy.deepcopy(choice_template)
        choice['Display'] = get_play_button(url, str(i)) # add audio player as choice
        new_question['Payload']['Choices'][f'{i+1}'] = choice
        # set the choice logic to require that 1+ audio samples are rated == 100
        logic = new_question['Payload']['Validation']['Settings']\
                    ['CustomValidation']['Logic']['0'][f'{i}']
        logic['QuestionID'] = f"QID{qid}"
        logic["QuestionIDFromLocator"] = f"QID{qid}"
        logic["ChoiceLocator"] = f"q://QID{qid}/ChoiceNumericEntryValue/{i+1}"
        logic["LeftOperand"] = f"q://QID{qid}/ChoiceNumericEntryValue/{i+1}"
        new_question['Payload']['Validation']['Settings']\
                    ['CustomValidation']['Logic']['0'][f'{i}'] = logic
    return new_question

# make n new blocks according to the survey_length
def make_blocks(num_questions, basis_blocks):
    new_blocks = basis_blocks
    block_elements = []
    for i in range(1,num_questions+1):
        block_element = OrderedDict()
        block_element['Type'] = 'Question'
        block_element['QuestionID'] = f'QID{i}'
        block_elements.append(block_element)
    new_blocks['Payload'][0]['BlockElements'] = block_elements
    return new_blocks

def set_id(obj):
    obj['SurveyID'] = config.survey_id
    return obj

def main():
    parser = argparse.ArgumentParser() # add question types
    parser.add_argument("-ab", action='store_true',
                        help="make A/B questions "
                        "(like preference test)")
    parser.add_argument("-abc", action='store_true',
                        help="make A/B/C questions"
                        "(like preference test)")
    parser.add_argument("-mc", action='store_true',
                        help="make multiple choice questions"
                        "(like error detection)")
    parser.add_argument("-trs", action='store_true',
                        help="make transcription questions"
                        "(with text field)")
    parser.add_argument("-mushra", action='store_true',
                        help="make MUSHRA questions with sliders")
    args = parser.parse_args()

    # create dictionary with question type : url list
    url_dict = {'ab':format_urls('ab',
                                 config.ab_file1,
                                 config.ab_file2),
                'abc':format_urls('abc',
                                  config.abc_file1,
                                  config.abc_file2,
                                  config.abc_file3)}

    # create new dictionary key and variable, when function returns 2 url sets
    url_dict['mc'], mc_filenames = format_urls('mc', config.mc_file)
    url_dict['trs'], trs_filenames = format_urls('trs', config.trs_file)
    url_dict['mushra'], ref_urls = format_urls('mushra', config.mushra_files)

    # get sentences from file to embed in multiple choice questions
    mc_sentences = get_sentences(config.mc_sentence_file)

    # get json to use as basis for new questions
    basis_json = get_basis_json()
    elements = basis_json['SurveyElements']

    # Set the survey ID in all survey_elements
    elements = list(map(set_id, elements))

    # get question template blocks from elements JSON
    # element order is survey-dependent- check if you're using a new template
    basis_question_dict = {'ab': elements[11],
                           'mc': elements[7],
                           'trs':elements[10],
                           'abc': elements[12],
                           'mushra': elements[9]}
    basis_blocks = elements[0]
    basis_flow = elements[1]
    rs = elements[8]
    basis_survey_count = elements[6]

    #  turn off answer order randomisation for MC questions (ie Yes/No)
    # comment out these 2 lines to add randomisation
    d = basis_question_dict['mc']["Payload"]
    basis_question_dict['mc'].update({"Payload": {i:d[i] for i in d if i!='Randomization'}})

    # store question text set in config.py, add an audio player where required
    q_text_dict = { 'ab': config.ab_question_text,
                    'abc': config.ab_question_text,
                    'mc': f"{config.mc_question_text} Sentence: <em>\
                            {'$sentence'}{get_player_html('$urls')}</em>",
                    'trs': f"{config.trs_question_text}\
                             {get_player_html('$urls')}",
                    'mushra': f"{config.mushra_question_text}\
                                {get_play_button('$ref_url', 'ref')}"}

    handler_dict = {'ab': ab_q,
                    'abc': ab_q,
                    'mc': mc_q,
                    'trs': None,
                    'mushra': mushra_q}

    # create list to store generated question blocks
    questions = []

    # create counters to use when indexing optional lists
    q_counter = 1 # qualtrics question numbering starts at 1
    mc_counter = 0
    mushra_counter = 0

    for arg in vars(args):
        for url_set in url_dict[arg]: # for each set of urls for that question type
            # embed the relevant urls or sentence into the question-specific text (if applicable)
            text = Template(q_text_dict[arg]).substitute(
                                ref_url=ref_urls[mushra_counter],
                                urls=url_set,
                                sentence=mc_sentences[mc_filenames[mc_counter]]
                                )
            # make a new question and add it to the list of questions
            questions.append(make_question(
                                # question number (starting at 1)
                                qid=q_counter,
                                # set of audio urls
                                urls=url_set,
                                # template for that question type
                                basis_question=basis_question_dict[arg],
                                question_type=arg,
                                # handler function for that question type
                                question_function=handler_dict[arg],
                                question_text=text  # as set above
                                ))
            q_counter += 1
            # increment counters when a question of that type is created
            # except for the last question (to prevent IndexError)
            mc_counter += (1 if arg == 'mc' and
                          mc_counter+1 < len(mc_filenames) else 0)
            mushra_counter += (1 if arg == 'mushra' and
                              mushra_counter+1 < len(ref_urls) else 0)

        # survey_length is determined by number of questions created
        survey_length = len(questions)

    # Create all the items in survey elements, with helper function where doing so is not trivial
    blocks = make_blocks(survey_length, basis_blocks)
    flow = basis_flow
    flow['Payload']['Properties']['Count'] = survey_length
    survey_count = basis_survey_count
    survey_count['SecondaryAttribute'] = str(survey_length)
    # add all the created elements together
    elements = [blocks, flow] + elements[2:7]  + questions + [rs]

    # Add the elements to the full survey
    # Not strictly necessary as we didn't do deep copies of elements
    out_json = basis_json
    out_json['SurveyElements'] = elements

    print(f'Generated survey with {survey_length} questions')
    with open(save_as, 'w+') as outfile:
        json.dump(out_json, outfile, indent=4)

if __name__ == "__main__":
    main()
