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
- To change your directory/folder use the command `cd`.
    
    For Example, you can use `cd Desktop/` to move into the Desktop folder
    Also, if you use the command `cd ..` it will move you out of the current folder to the previous folder

- To view all the files in your current folder or to check which folder you are currently in, you can use the command `ls`

- To clone a Git folder into your local machine, you can use the command `git clone` followed by the clone link to the repository

- To add all the new files you have created or modified you can use the command `git add .` which will add all the files in the folder
    If you want to update or upload one specific file instead of using the full stop, type in the file name as such, `git add EXAMPLE.py`

- Git requires you to make a commit before you can push the code. To commit you also need to type in some comment about the commit/changes you are making.
For example, `git commit -m "Made some changes to the GUI"`. The command for the commit is `git commit -m` and the comment would be `"Made some changes to the GUI"`.
Comments do not have to be specific but the more specific it is the easier for your collaborators to understand what changes you have made.

### Setting up Command Line Interface (CLI) / Terminal
1. First, please ensure you have GitHub account and you are authorised to access/modify these files.
2. (*Optional*) If you are using Windows, you need to download [Git BASH](https://gitforwindows.org/) and finished the installation by following the instruction .
3. Get the clone link from repository website (Green Button) and copy it. 

4. Then in your command line (Git BASH or Terminal) and make sure you navigate the command line to where you want to store the GitHub folder using `cd` command.

5. After you successfully navigate to where you want to store the GitHub folder, use the command `git clone` followed by the copied clone link and press return.

For example, `git clone https://github.com/rayjaelee/blinov-research.git` should be entered if you are copying this repository.

4. Now, all the GitHub respository is store in your local machine. Now let's move on to working on the respository.

### Making changes to the respository
- It is important you talk your supervisor or graduate student to ensure which way to proceed
- The best practice is to use the branch feature of Git to make changes and push them to the repository [more information here](https://www.atlassian.com/git/tutorials/using-branches)
- When you initially setup the respository the branch is set to master
- You should change to the desired branch you want to work on or create your own

- You can change the branch you are on by using `git checkout` followed by the branch name.

For example, if the desired branch you want to work is named *voltage-function*, use `git checkout voltage-function` in your command line.

You can also see all the branches by using the command `git branch --list`

If you want to create a new branch to work from follow these steps:

1. First ensure the repository is the most current master, otherwise there can be a huge merging problem.
2. You can pull the most recent repository by using `git pull`.
3. Then use the command `git checkout -b` followed by the branch name.

For example, if you want to create a branch name called *trappers-trap*, the command would be `git checkout -b trappers-trap`

4. If you use the above command, after creating the branch it will automatically checkout (switch to) to the created branch

5. Now you can start working on the file(s)! Let's say you made all the changes you need. Let's move on to pushing your changes to GitHub!

### Pushing your changes and merging repository
- Pushing and merging the changes can sometimes be frsutrating and bothersome. Some issues might be unique to your machine due to environment setting.

## Push help
1. After making all the changes and saving all your changes, you should check the repository status in your command line by using the command `git status`
2. If you have create a new file, you want to use the command `git add ` followed by the file name or you can also use the `.` after the command to add all files.

For example, if you have created a file called `ion-trapperz.py`, the command should look like `git add ion-trapperz.py`. If you have created multiple files or if you can't be bothered to type out the
file name, you can use the command `git add .` to add all the files. Personally, I use `git add .` no matter what (even if I didn't create any new files).

3. After adding all the file(s), you want to commit your changes using the command `git commit -m` followed by the commit message/note.

For example, if you want to add commit message of *I'm in my house trapping*, the command should look like `git commit -m "I'm in my house trapping"`

4. After successful commit, use the command `git push` to push your code into the repository.

You may run into some trouble using `git push`, this may be due to your origin of repository not set up correctly. There should be a follow up message in the command line recommending how you should proceed. Follow that recommendation and if it still doesn't work, search Google. There are a lot of useful help in Stack Overflow!

## Merge help
- Merging in general should be done by who has the authority and access
- Before merging, checking the branch timelines using GitHub Desktop or any other graphical interface can sometimes help your understanding of the repository.


### General advice
In my personal experience and opinion, the best option for troubleshooting when you come across an issue is to 
1. Search in Google. Search results from StackOverflow can be very useful!
2. Ask your supervisor or any one of your colleagues who has experience with Git to help you out! 
3. If none of the above works, create an issue ticket in the [respository website issue tab](https://github.com/rayjaelee/blinov-research/issues) describing your issues/troubles!

Bear in mind that not everyone's setup is same as your's. Your issue can be unique due to your working environment!

### Using GitHub Desktop Client
- If you can't be bothered to use the CLI, you can download [GitHub Desktop](https://desktop.github.com/) 

### Was my explanation hard to follow? Want to learn more?
- If my explanation was hard to follow or you want to learn more tricks and skills for Git, you can visit [Codecademy's Git Course](https://www.codecademy.com/learn/learn-git)!