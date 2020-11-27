Some known problems & fixes for creating listening tests in Qualtrics.

#### AttributeError: module 'config' has no attribute...
`testmaker.py` needs each of the variables in `config.py` to exist. For question types you don't need, the paths can be set to anything, but don't comment them out.

#### The play button is disabled

Transcription questions currently have embedded JavaScript which only lets each audio file play once. This affects surrounding questions displayed on the same survey page. You should move questions of other types to a separate page of the survey.

#### MUSHRA audio HTML tags break when I edit the question

Editing the MUSHRA question/choice fields in Qualtrics will break the HTML audio tags. You should make any changes in the file `config.py` before running the script.

#### I want the order of my Multiple Choice answers to be randomised

Comment out the following lines in the `testmaker.py`:

``` python
d = basis_question_dict['mc']['Payload']<br>
basis_question_dict['mc'].update({'Payload': {i:d[i] for i in d if i!='Randomization'}})
```
