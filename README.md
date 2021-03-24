This is a tool for automating the process of creating online listening tests in Qualtrics. If you have any issues using it please submit here https://github.com/CSTR-Edinburgh/qualtreats/issues

# Background
This tool reduces number of manual steps required to create a functioning test. It works by generating a JSON file which Qualtrics will interpret to  produce a survey. It was originally created for use in evaluating text-to-speech systems, but has wider applications in speech technology and other audio-related fields.

This is not supported in any way by Qualtrics and is 100% unofficial.

###### Guide contents:
- [Functionality](#functionality)
- [Instructions](#instructions)
  * [Python dependencies](#python-dependencies)
  * [Getting the script](#getting-the-script)
  * [Configuration](#configuration)
    + [`config.py`](#-configpy-)
    + [Default Settings](#default-settings)
      - [For all question types:](#for-all-question-types-)
      - [Transcription questions:](#transcription-questions-)
      - [MUSHRA questions:](#mushra-questions-)
  * [Running the script](#running-the-script)
  * [Importing to Qualtrics](#importing-to-qualtrics)
- [Manual steps](#manual-steps)

# Functionality

It currently supports:
- A/B preference questions (‘Which speech sample sounds more natural?’)
- A/B/C preference questions (as above but with 3 choices)
- Multiple choice questions (‘Does this speech sample contain any errors?’)
- Transcription questions (‘Listen to this audio clip and type what you hear.’)
- MUSHRA style questions (MUltiple Stimuli with Hidden Reference and Anchor)
- MOS test questions (Mean Opinion Score, with 1:5 slider scale)

See a demo test showcasing each question type [here](https://edinburghinformatics.eu.qualtrics.com/jfe/form/SV_0PrKc4KQ7jDXxLn).

<img src="https://raw.githubusercontent.com/evelyndjwilliams/readme-gifs/main/finished-testmaker.gif" width="500" height="370">


<br>A MUSHRA test question created using the testmaker script.

# Instructions

The file `help.md` contains solutions to some issues we encountered while generating surveys.
A Wiki with more comprehensive instructions for setting up listening tests in Qualtrics is [here](https://www.wiki.ed.ac.uk/pages/viewpage.action?spaceKey=CSTR&title=Qualtrics+Listening+Tests)

## Python dependencies

This tool only uses packages from the Python standard library.

## Getting the script

Clone the <Name> GitHub repository with the command:

`git clone https://github.com/jacobjwebber/qualtrics-listening-test-maker.git`

## Configuration

### `config.py`

The script expects the folder `/resources` to contain `.txt` files with lists of your audio URLs.  Some test files are included by default. The necessary file format varies between question types. Requirements for each type are detailed in `config.py`.

Before running the script, the file `config.py` should be updated to contain the correct paths for your URLs, and the correct text for your questions.
(This only applies to the question types included in your test, which you will specify using command line flags. The others won't be executed, so can remain as the default.)


### `combined-template.json`

This file contains the basic building blocks for every available question type. You don't need to modify this file to run the script.

 If you want to extend the script's functionality to include more question types, you should generate a new JSON template file. You can do this by manually creating a survey in Qualtrics which meets your requirements, and exporting the survey file (Tools --> Export).


### Number of questions
The number of questions in the survey is taken automatically from the number of filenames in your lists.

### Default Settings
Default question settings are determined by the template file `combined-template.JSON`. These settings include:

#### For all question types
- Answer choices are presented in random order (except for multiple choice questions).
- Force response, so all questions must be answered before proceeding.

#### Transcription questions
- Audio playback is disabled for transcription tests (so each audio clip can be played only once).

#### MUSHRA questions
- The default HTML5 audio player is replaced by a simple play/pause button, as the hidden reference could be identified by its duration.
- At least one sample must be rated == 100 (in line with the guidelines set out in ITU-R BS.1534-1).

Changing these settings requires either editing the template file (`combined-template.JSON`) or creating a new template by creating a question in Qualtrics with the correct specifications and exporting the survey file.


## Running the script

The script is run from the command line, using flags to specify the desired question types.

Flags:
- `-ab` = A/B preference
- `-abc` = A/B/C preference
- `-mc` = multiple choice
- `-trs` = audio transcription
- `-mushra` = MUSHRA
- `mos` = MOS

Questions will be added to the output test in the order you supply the flags.

E.g. to create a test with MUSHRA then audio transcription questions, use the command:

`python testmaker.py -mushra -trs`

<img src="https://raw.githubusercontent.com/evelyndjwilliams/readme-gifs/main/run-testmaker.gif" width="420" height="200">

<br>


Running the script will create a .qsf (Qualtrics Survey Format) file called `output-survey.qsf`.

## Importing to Qualtrics
This file can be imported to Qualtrics (following the steps [here](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/)) and will be converted to a working listening test.

<img src="https://raw.githubusercontent.com/evelyndjwilliams/readme-gifs/main/import-testmaker.gif" width="420" height="330">



# Manual steps

While this script generates test questions, other elements of the test still have to be configured manually in Qualtrics. These include consent forms and instructions, as well as specific flow settings, like randomly assigning participants to groups.
