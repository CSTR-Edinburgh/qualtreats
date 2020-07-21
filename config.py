# change the text you want to appear in your questions
ab_question_text = "Which of the following sounds the most natural?"
mc_question_text= "Are there any errors in this speech sample?"
trs_question_text = "Please type the sentence you hear in this audio sample."

# each file should have a fileame and url per line

ab_file1 = "ab-urls-True.txt"
ab_file2 = "ab-urls-False.txt"

mc_file = "mc-urls.txt"

abc_file1 = "abc-urls-1.txt"
abc_file2 = "abc-urls-2.txt"
abc_file3 = "abc-urls-3.txt"

trs_file = "trs-urls.txt"

# mc_sentence_file should be changed to your filename/sentence text file
# this file should have a filename and corresponding sentence string per line
mc_sentence_file = "sentences.txt"


# TODO implement force response--> currently changed setting to 'ON' in template.son
force_response = 'ON' # or 'OFF'

# TODO, replace survey ID in template json with bespoke one defined here
survey_id = "SV_112345677889912"
survey_id = "SV_4TLSPrwNIjymdh3"


# # the following functions format files into sets of urls
#
#
# # for AB tests, each question is defined by an ordered pair of audio urls# for AB tests, each question is defined by an ordered pair of audio urls
# def format_ab_urls(file_1, file_2):
#     with open(file_1) as f1:
#         with open(file_2) as f2:
#             urls = [(line1.split()[1], line2.split()[1]) for line1, line2 in zip(f1,f2)]
#     return(urls)
#
# # for ABC tests, each question is defined by an ordered set of 3 urls
# def format_abc_urls(file_1, file_2, file_3):
#     with open(file_1) as f1:
#         with open(file_2) as f2:
#             with open(file_3) as f3:
#                 urls = [(line1.split()[1], line2.split()[1], line3.split()[1]) for line1, line2, line3 in zip(f1, f2, f3)]
#     return(urls)
#
# # for MC & transcription tests, each question is defined by a single audio url
# def format_single_urls(url_file):
#     with open(url_file) as f:
#         names, urls = zip(*(l.split(' ', 1) for l in f))
#     return(urls, names)
#
# ab_urls = format_ab_urls(ab_file1, ab_file2)
# mc_urls, mc_filenames = format_single_urls(mc_file)
# abc_urls = format_abc_urls(abc_file1, abc_file2, abc_file3)
# trs_urls, trs_filenames = format_single_urls(trs_file)
