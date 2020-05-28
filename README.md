# README

This generates a json config (aka Qualtrics Survey Format (.qsf)) file for a quatrics survey.
User generation of these files is not encouraged by Qualtrics, it could theoretically break things, check it 
works before recruiting people etc.


## Use

Currently supports only AB testing.

Host your audio urls somewhere (e.g. homepages server or S3).

In config.py add urls as a list of ordered pairs in audio_urls.
Add your question text in question_text

run 

```
python testmaker.py
```

import the output qsf file into a blank Qualtrics survey.


## Add a new kind of test!


To add a new kind of question, create an example survey on qualtrics with one question in the style you want.
You should add randomisation etc.

Then download the qsf file by doing 
Tools -> Import/Export -> Export Survey

Run

```
python print_question.py <MySurveyName>.qsf
```

This _should_ print the json object of the question. You can then create more in this style by creating an
equivalent python object.
The whole process is pretty ugly (sorry). But, it can hopefully save a lot of time and inaccuracies.

```
    {
        "SurveyID": "SV_79AC1q1rFKNcfRz",
        "Element": "SQ",
        "PrimaryAttribute": "QID1",
        "SecondaryAttribute": "Which of the following sounds the most natural?",
        "TertiaryAttribute": null,
        "Payload": {
            "QuestionText": "Which of the following sounds the most natural?",
            "DataExportTag": "Q1",
            "QuestionType": "MC",
            "Selector": "SAVR",
            "SubSelector": "TX",
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "QuestionDescription": "Which of the following sounds the most natural?",
            "Choices": {

```
_continues_

The output from this should look something like above, although this is a AB example.

This assumes the first question is the 7th element in the 'SurveyElements' attribute of the qsf file. It may also be the eighth...

testmaker.py contains make_ab_test, which generates a AB test question. Make another helper function in this style and use appropriately.


