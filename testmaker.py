# System imports
import argparse
import json
import copy
from string import Template
from collections import OrderedDict
import datetime
# local imports
import config

json_filename = "template.json"
save_as = "output-survey.qsf"
# audio template should not be changed
audio_html_template = "audio_template.html"

def get_basis_json():
    with open(json_filename) as json_file:
        test = json.load(json_file)
    return test

def get_player_html(url):
    with open(audio_html_template) as html_file:
        html_string = html_file.read()
        html_template = Template(html_string)
        html_player = html_template.substitute(url=url)
        return html_player

# for AB tests, each question is defined by an ordered pair of audio urls# for AB tests, each question is defined by an ordered pair of audio urls
def format_ab_urls(file_1, file_2):
    with open(file_1) as f1:
        with open(file_2) as f2:
            urls = [(line1.split()[1], line2.split()[1]) for line1, line2 in zip(f1,f2)]
    return(urls)

# for ABC tests, each question is defined by an ordered set of 3 urls
def format_abc_urls(file_1, file_2, file_3):
    with open(file_1) as f1:
        with open(file_2) as f2:
            with open(file_3) as f3:
                urls = [(line1.split()[1], line2.split()[1], line3.split()[1]) for line1, line2, line3 in zip(f1, f2, f3)]
    return(urls)

# for MC & transcription tests, each question is defined by a single audio url
def format_single_urls(url_file):
    with open(url_file) as f:
        names, urls = zip(*(l.split(' ', 1) for l in f))
    return(urls, names)

def get_sentences(sentence_file):
    sentences = {}
    l = open(sentence_file, encoding="utf8").readlines()
    for line in l:
        # takes file where each line contains an audio file name and the corresponding sentence html_string
        # deliminator may differ in your file, so | below may need changed
        parts = line.split(' ', 1)
        sentences[parts[0]] = parts[1]
    return(sentences)

def make_question(qid, urls, basis_question, question_type, sentence_list=None, file_list=None):
    new_question = copy.deepcopy(basis_question)
    # Set the survey ID
    new_question['SurveyID'] = config.survey_id
    # Change all the things that reflect the question ID
    new_question['PrimaryAttribute'] = 'QID{}'.format(qid)
    new_question['Payload']['QuestionID'] = 'QID{}'.format(qid)
    new_question['Payload']['DataExportTag'] = 'Q{}'.format(qid)

    if question_type == 'ab' or question_type == 'abc':
        # Set question text
        new_question["SecondaryAttribute"] = config.ab_question_text
        new_question["Payload"]["QuestionText"] = config.ab_question_text
        new_question["Payload"]["QuestionDescription"] = config.ab_question_text

        # add the choices
        if question_type == 'ab':
            new_question['Payload']['Choices']['1']['Display'] = get_player_html(urls[0])
            new_question['Payload']['Choices']['2']['Display'] = get_player_html(urls[1])

        elif question_type == 'abc':
            new_question['Payload']['Choices']['1']['Display'] = get_player_html(urls[0])
            new_question['Payload']['Choices']['2']['Display'] = get_player_html(urls[1])
            new_question['Payload']['Choices']['3']['Display'] = get_player_html(urls[2])

    elif question_type == 'mc':
        # Set question text
        new_question["SecondaryAttribute"] = config.mc_question_text
        # <em> italicises sentence text
        new_question["Payload"]["QuestionText"] = "{0} Sentence: <em> {1} {2}</em>".format(config.mc_question_text,
        sentence_list[file_list[qid-1]], get_player_html(urls))
        new_question["Payload"]["QuestionDescription"] =  sentence_list[file_list[qid-1]]

        # add the choices

        new_question['Payload']['Choices']['1']['Display'] = "Yes"
        new_question['Payload']['Choices']['2']['Display'] = "No"

    elif question_type == 'trs':
        # Set question text
        new_question["SecondaryAttribute"] = config.trs_question_text
        new_question["Payload"]["QuestionText"] = "{0} {1}".format(config.trs_question_text, get_player_html(urls))
        new_question["Payload"]["QuestionDescription"] =  config.trs_question_text

    return new_question

def make_blocks(num_questions, basis_blocks):
    new_blocks = basis_blocks
    block_elements = []
    for i in range(1,num_questions+1):
        block_element = OrderedDict()
        block_element['Type'] = 'Question'
        block_element['QuestionID'] = 'QID{}'.format(i)
        block_elements.append(block_element)
    new_blocks['Payload'][0]['BlockElements'] = block_elements
    return new_blocks

def set_id(obj):
    obj['SurveyID'] = config.survey_id
    return obj

def print_question(filename):
    with open(filename) as json_file:
        basis_json = json.load(json_file)
    elements = basis_json['SurveyElements']
    # IMPORTANT -- assumes the first question is the seventh 'element'
    # There is no qsf standard to base this on. You may want to print ALL elements
    basis_question = elements[8]
    print(json.dumps(basis_question, indent=4))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-ab", action='store_true', help="make A/B questions (like preference test)")
    parser.add_argument("-abc", action='store_true', help="make A/B/C questions (like preference test)")
    parser.add_argument("-mc", action='store_true', help="make multiple choice questions (like error detection)")
    parser.add_argument("-trs", action='store_true', help="make transcription questions (with text field)")
    args = parser.parse_args()

    ab_urls = format_ab_urls(config.ab_file1, config.ab_file2)
    mc_urls, mc_filenames = format_single_urls(config.mc_file)
    abc_urls = format_abc_urls(config.abc_file1, config.abc_file2, config.abc_file3)
    trs_urls, trs_filenames = format_single_urls(config.trs_file)
    mc_sentences = get_sentences(config.mc_sentence_file)

    survey_length = 0
    survey_length += len(mc_urls) if args.mc else 0
    survey_length += len(ab_urls) if args.ab else 0
    survey_length += len(abc_urls) if args.abc else 0
    survey_length += len(trs_urls) if args.trs else 0

    basis_json = get_basis_json()

    elements = basis_json['SurveyElements']
    # Set the survey ID in all survey_elements
    elements = list(map(set_id, elements))

    ab_basis_question = elements[10]
    mc_basis_question = elements[7]
    trs_basis_question = elements[9]
    abc_basis_question = elements[11]

    # turns off answer order randomisation
    d = mc_basis_question["Payload"]
    edited_dict = {i:d[i] for i in d if i!='Randomization'}
    mc_basis_question.update({"Payload": edited_dict})

    basis_blocks = elements[0]
    basis_flow = elements[1]
    rs = elements[8]
    basis_survey_count = elements[6]
    mc_basis_html = mc_basis_question['Payload']['QuestionText']
    ab_basis_html = ab_basis_question['Payload']['QuestionText']
    trs_basis_html = trs_basis_question['Payload']['QuestionText']
    abc_basis_html = abc_basis_question['Payload']['QuestionText']

    # Create all the items in survey elements, with helper function where doing so is not trivial
    blocks = make_blocks(survey_length, basis_blocks)

    flow = basis_flow
    flow['Payload']['Properties']['Count'] = survey_length

    survey_count = basis_survey_count
    survey_count['SecondaryAttribute'] = str(survey_length)

    questions = []
    question_counter = 1

    if args.mc:
        for url in (mc_urls):
            q = make_question(question_counter, url, mc_basis_question, 'mc', mc_sentences, mc_filenames)
            questions.append(q)
            question_counter += 1

    if args.ab:
        for url in (ab_urls):
            q = make_question(question_counter, url, ab_basis_question, 'ab')
            questions.append(q)
            question_counter += 1

    if args.abc:
        for url in (abc_urls):
            q = make_question(question_counter, url, abc_basis_question, 'abc')
            questions.append(q)
            question_counter += 1

    if args.trs:
        for url in (trs_urls):
            q = make_question(question_counter, url, trs_basis_question, 'trs')
            questions.append(q)
            question_counter += 1

    elements = [blocks, flow] + elements[2:7]  + questions + [rs]

    # Add the elements to the full survey
    # Not strictly necessary as we didn't do deep copies of elements
    out_json = basis_json
    out_json['SurveyElements'] = elements

    print('Generated survey with {} questions'.format(survey_length))
    with open(save_as, 'w+') as outfile:
        json.dump(out_json, outfile, indent=4)


if __name__ == "__main__":
    main()
