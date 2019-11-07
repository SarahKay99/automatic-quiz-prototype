# AutoQuiz prototype
Just started a content-heavy unit? Studying for exams? Write your notes in a simple markup format and automatically be quizzed!

*only compatible with Windows for now.

# HOW TO USE:
1) Write your notes in a .txt file, using the following markup: 
  
  %Word: *its definition*%
  
  .) Begin AND end the line with %.
  
  .) Seperate the word and its definition with :
  
  ================================================
  
  EXAMPLE: basicbiology.txt
  
  %Mitochondria: The powerhouse of the cell.%
  
  %Organism: A cluster of funtioning cells.%
  
  %Golgi Bodies: An organelle which stores and distributes molecules in the cell.%
  
  Mitochondria produce ATP and provide energy to the cell.
  
  All organisms have mitochondria in their cells.
  
  ================================================
  
  Now you'll be tested on the definitions of "mitochondria", "organism" and "Golgi Bodies"!
  
  However, you won't be tested on the last two lines: they are just notes you took.
  
  Quicker than writing flash-cards, eh?

# ---WINDOWS---
2) Ensure you have installed Python 3.

3) Click "clone or download". Unzip the file.

4) Open the unzipped folder in your file explorer. **Copy** its file address.

5) Open command prompt. WRITE THE FOLLOWING COMMANDS:

cd **//Paste file address with ctrl+V//** **//Press Enter//**

python run quiz.py **//Press Enter//**

6) Copy the address of your .txt file.

Get ready to paste it when prompted. 

You're good to go!
