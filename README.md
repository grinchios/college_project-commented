# Business management software
## Callum Pritchard

This software is to be run on a linux distro
due it's linux file calling functions within
the login form

This repo does not work due to the comments however
in the folder called working is the working version
without the objective comments

## Admin credentials

username: admin
password: a12345678@

## Secretary credentials

username: dan
password: d@nisamaz90

Moderator can press the moderator button to automatically
be placed as an admin within the program, Moderator credentials
don't exist they just load the main menu directly for ease

## Requirements

Requirements are listed in req.txt,
they must be installed with pip3,
may need pre-pending with sudo -H

pip3 install -r req.txt

If any error arises you will need to install the
requirements manually with the below command

pip3 install <name-of-package>

To install PyQt5 you must use the command

pip3 install pyqt5

## File structure

root: holds README, initial script, file for backing up and requirements
bin: holds forms and python shared routines
bin/forms: holds forms

## Backing up

You will need to obtain a new version of a file called client_secrets.json
instructions can be found here:

https://cloud.google.com/genomics/downloading-credentials-for-api-access

The file must be stored in project root and named as listed above to work

## Issues

Backing up must be completed when started or the GUI will crash
this couldn't be put in a different thread as the drive integration
would not start

## Execution

The program must be run from project root and with command
python3 login.py

The program loads with 1280x720 resolution and works best on any
resolution equal to or better than it, it doesn't support scaling

## Acknowledgements

The email regular expression used is from

emailregex.com

The postcode regular expression is an optimised version of the below (page 6)

https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/488478/Bulk_Data_Transfer_-_additional_validation_valid_from_12_November_2015.pdf
