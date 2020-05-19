import json
import config
import copy
from string import Template
from collections import OrderedDict

json_filename = "random.json"
audio_html_template = "audio_template.html"
save_as = "output.qsf"


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

def make_ab_question(qid, urls, basis_question):
    new_question = copy.deepcopy(basis_question)
    # Set the survey ID
    new_question['SurveyID'] = config.survey_id
    # Change all the things that reflect the question ID
    new_question['PrimaryAttribute'] = 'QID{}'.format(qid)
    new_question['Payload']['QuestionID'] = 'QID{}'.format(qid)
    new_question['Payload']['DataExportTag'] = 'Q{}'.format(qid)

    # Set question text
    new_question["SecondaryAttribute"] = config.question_text
    new_question["Payload"]["QuestionText"] = config.question_text
    new_question["Payload"]["QuestionDescription"] = config.question_text

    # add the choices
    new_question['Payload']['Choices']['1']['Display'] = get_player_html(urls[0])
    new_question['Payload']['Choices']['2']['Display'] = get_player_html(urls[1])

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


def main():
    #config.ab_urls = [config.ab_urls[0]]
    survey_length = len(config.ab_urls)
    basis_json = get_basis_json()
    #print(json.dumps(basis_json, indent=4))

    elements = basis_json['SurveyElements']
    # Set the survey ID in all survey_elements
    elements = list(map(set_id, elements))
    # The survey elements list contains a number of things we must change
    basis_question = elements[7]
    basis_blocks = elements[0]
    basis_flow = elements[1]
    basis_survey_count = elements[6]

    basis_html = basis_question['Payload']['Choices']['1']['Display']


    # Create all the items in survey elements, with helper function where doing so is not trivial
    blocks = make_blocks(survey_length, basis_blocks)

    flow = basis_flow
    flow['Payload']['Properties']['Count'] = survey_length

    survey_count = basis_survey_count
    survey_count['SecondaryAttribute'] = str(survey_length)


    questions = []
    for i, urls in enumerate(config.ab_urls):
        # Questions are numbered from 1 (eurgh) so i+1
        q = make_ab_question(i+1, urls, basis_question)
        questions.append(q)

    # Include all the random stuff in survey elements before the questions
    elements = [blocks, flow] + elements[2:7] + questions + [elements[-1]]

    # Add the elements to the full survey
    out_json = basis_json
    out_json['SurveyElements'] = elements
    #print(json.dumps(out_json, indent=4))
    print('Generated survey with {} questions'.format(survey_length))
    with open(save_as, 'w') as outfile:
        json.dump(out_json, outfile, indent=4)


if __name__ == "__main__":
    main()
