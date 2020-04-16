# blinov-research
This repository contains the Python scripts for controlling the National Instrument (NI) Data Acquition Card (DAQ). We utilise [Spinmob](https://github.com/Spinmob/spinmob/wiki)
 and [NI-DAQmx Python Modules](https://nidaqmx-python.readthedocs.io/en/latest/). 

Please refer to the end of the README for instructions on how to easily integrate github.

Here are the details for each of the scripts and its patch/release notes.

## File Information / Release Notes

### Ion-Trap-Main.py
- Original file written by Alex Kato

### ion-trap-scrippy-v0.py
- Rearrange the codes to make sure clean modular patterns
- Removed any redunant codes

### ion-trap-scrippy-v0_1.py
- Finished rearranging the codes
- Works without any compiling issues

### ion-trap-scrippy-v0_2.py
- Some minor bug fixes

### ion-trap-scrippy-v1.py
- Added voltage sending function

### ion-trap-scrippy-v1_1.py
- Added label and functioning step buttons along with number box

### ion-trap-scrippy-v2.py
- Refractored codes for efficiency
- Added comments

## GitHub Integration Instruction

#### Simple but essential Git Commands
- To change your directory/folder use the command `cd`
    For Example, you can use `cd Desktop/` to move into the Desktop folder
    Also, if you use the command `cd ..` it will move you out of the current folder to the previous folder

- To view all the files in your current folder or to check which folder you are currently in, you can use the command `ls`

- To clone a Git folder into your local machine, you can use the command `git clone` followed by the clone link to the repository

- To add all the new files you have created or modified you can use the command `git add .` which will add all the files in the folder
    If you want to update or upload one specific file instead of using the full stop, type in the file name as such, `git add EXAMPLE.py`

- Git requires you to make a commit before you can push the code. To commit you also need to type in some comment about the commit/changes you are making.
For example, `git commit -m "Made some changes to the GUI"`. The command for the commit is `git commit -m` and the comment would be `"Made some changes to the GUI"`.
Comments do not have to be specific but the more specific it is the easier for your collaborators to understand what changes you have made.

### Using Command Line Interface (CLI) / Terminal
1. First, please ensure you have GitHub account and you are authorised to access/modify these files.
2. (*Optional*) If you are using Windows, you need to download [Git BASH](https://gitforwindows.org/)
3.
3. Get the clone link from repository website (Green Button) and copy it. Then go to your command line (Git BASH for Windows and Terminal for Mac) and type in the command `git clone` followed by pasting in the clone link and press return
4. 

### Using GitHub Desktop Client
- If you can't be bothered to use the CLI, you can download [GitHub Desktop](https://desktop.github.com/) 

### Was my explanation hard to follow? Want to learn more?
- If my explanation was hard to follow or you want to learn more tricks and skills for Git, you can visit [Codecademy's Git Course](https://www.codecademy.com/learn/learn-git)!