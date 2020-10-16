This is a tool for automating the process of creating online listening tests in Qualtrics.

# Background
This tool reduces number of manual steps required to create a functioning test. It works by generating a JSON file which Qualtrics will interpret to  produce a survey. It was originally created for use in evaluating text-to-speech systems, but has wider applications in speech technology and other audio-related fields.


This is not supported in any way by Qualtrics and is 100% unofficial.

# Functionality

It currently supports:
- A/B preference questions (‘Which speech sample sounds more natural?’)
- A/B/C preference questions (as above but with 3 choices)
- Multiple choice questions (‘Does this speech sample contain any errors?’)
- Transcription questions (‘Listen to this audio clip and type what you hear.’)
- MUSHRA style questions (MUltiple Stimuli with Hidden Reference and Anchor)

A demo test showcasing each question type is available [here](https://edinburghinformatics.eu.qualtrics.com/jfe/form/SV_01EWlEINsQDssVD).

<img src="https://raw.githubusercontent.com/evelyndjwilliams/readme-gifs/main/finished-testmaker.gif" width="500" height="370">


<br>A MUSHRA test question created using the testmaker script.

# Instructions
## Configuration

### `config.py`
Before running the script, the file `config.py` should be updated to contain the correct paths for your urls, the correct text for your questions.
(This only applies to the question types included in your test, which you will specify using command line flags. The others won't be executed, so can remain as the default.)

The required url file format depends on the question type you are generating. Requirements for each type are detailed in `config.py`.

### Default Settings
Default question settings are determined by the template file `combined-template.JSON`. These settings include:

#### For all question types:
- Answers are presented in random order (except for multiple choice questions).
- Force response, so all questions must be answered before proceeding.

#### Transcription questions:
- Audio playback is disabled for transcription tests (so each audio clip can be played only once).

#### MUSHRA questions:
- The default HTML5 audio player is replaced by a simple play/pause button, as the hidden reference could be identified by its duration.
- At least one sample must be rated == 100 (in line with the guidelines set out in ITU-R BS.1534-1).

Changing these settings requires either editing the template file (`combined-template.JSON`) or creating a new template by creating a question in Qualtrics with the correct specifications and exporting the survey file.


## Running the Script

The script is run from the command line, using flags to specify the desired question types.

Flags:
- `-ab` = A/B preference
- `-abc` = A/B/C preference
- `-mc` = multiple choice
- `-trs` = transcription
- `-mushra` = MUSHRA

The order of the flags will determine the order of the questions in the output test.

E.g. to create a test with MUSHRA then audio transcription questions, use the command:

`python testmaker.py -mushra -trs`

<img src="https://raw.githubusercontent.com/evelyndjwilliams/readme-gifs/main/run-testmaker.gif" width="420" height="200">

<br>

Running the script will create a .qsf (Qualtrics Survey Format) file called `output-survey.qsf`.
This file can be imported to Qualtrics, and will be converted to a working listening test.

<img src="https://raw.githubusercontent.com/evelyndjwilliams/readme-gifs/main/import-testmaker.gif" width="420" height="330">



# Manual steps

While this script generates test questions, other elements of the test still have to be configured manually in Qualtrics. These include consent forms and instructions, as well as specific flow settings, like randomly assigning participants to groups.
