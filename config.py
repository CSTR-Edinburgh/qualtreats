# survey_id can remain unchanged
survey_id = "SV_4TLSPrwNIjymdh3"

# the below variables should be set according to your survey specifications

# this text will appear in each question
ab_question_text = "Which of the following sounds the most natural?"
mc_question_text= "Are there any errors in this speech sample?"
trs_question_text = "Please type the sentence you hear in this audio sample."
mushra_question_text = "How natural are the following speech recordings? <br> Reference: "

# these files contain the urls to be embedded in questions/choices
# each file should have a filename and url per line, separated by whitespace
ab_file1 = "ab-urls-True.txt"
ab_file2 = "ab-urls-False.txt"
abc_file1 = "abc-urls-1.txt"
abc_file2 = "abc-urls-2.txt"
abc_file3 = "abc-urls-3.txt"
mc_file = "mc-urls.txt"
trs_file = "trs-urls.txt"

# mushra filenames should be the same across folders
# audiofile urls should vary only by folder name
# any number of folders can be specified
mushra_files = "mushra-urls.txt"
mushra_root = "http://www.dummy-website.com"
# a hidden reference folder should be included in both mushra_folders and mushra_ref_folder
mushra_folders = ["folder1/","folder2/","folder3/","folder4/", "ref/"]
mushra_ref_folder = "ref/"

# MC questions have sentence text embedded
# this file should have a filename and corresponding sentence string per line,
mc_sentence_file = "sentences.txt"
