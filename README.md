# AutoQuiz prototype
Just started a content-heavy unit? Studying for exams? Write your notes in a simple markup format and automatically be quizzed!

*only compatible with Windows for now.

# HOW TO USE:
1) Write your notes in a .txt file, using the following markup: 
**OR, IF YOU JUST WANT TO TRIAL THE SOFTWARE, USE SAMPLE NOTES AND SKIP THIS STEP**
  
  %Word: *its definition*%
  
  .) Begin AND end the line with %.
  
  .) Seperate the word and its definition with :
  
  ================================================
  
  EXAMPLE: basicbiology.txt
  
  %Mitochondria: The powerhouse of the cell.%
  
  %Organism: A cluster of funtioning cells.%
  
  %Golgi Bodies: An organelle which stores and distributes molecules in the cell.%
  
  %Endoplasmic Reticulum: An organelle which synthesizes molecules for the cell to use.%
  
  %Nucleus: An organelle which produces DNA and stores it.%
  
  Mitochondria produce ATP and provide energy to the cell.
  
  All organisms have mitochondria in their cells.
  
  ================================================
  
  Now you'll be tested on the definitions of "mitochondria", "organism", "Golgi Bodies", "Nucleus" and "Endoplasmic Reticulum"! **You need at least 5 definitions for the program to work.**
  
  However, you won't be tested on the last two lines: they are just notes you took.
  
  Quicker than writing flash-cards, eh?

# ---WINDOWS---
2) Ensure you have installed Python 3.

3) Download and unzip the project.

4) Open the unzipped folder in your file explorer. **Copy** its file address.

5) Open command prompt. WRITE THE FOLLOWING COMMANDS:

cd **-ctrl+V-** **-Enter-**

python run quiz.py **-Enter-**

6) Open your file explorer. Find the folder which contains your .txt file and **Copy** its address. 

OR: 

Open your file explorer. Navigate to Sample Notes and **Copy** that address.

7) Press **-Ctrl+V-** when you see: "Enter the directory of your notes: "

You're good to go!
