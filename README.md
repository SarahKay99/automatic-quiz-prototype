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
  
  Mitochondria produce ATP and provide energy to the cell.
  All organisms have mitochondria in their cells.
  
  ================================================
  Now you'll be tested on the definitions of "mitochondria" and "organism"!
  Better than writing flash-cards, eh?

# ---WINDOWS---
2) Open command prompt.

3) WRITE THE FOLLOWING COMMANDS:
cd *the directory where automatic-quiz-prototype is saved*
python run quiz.py

4) Copy the address of your .txt file.
Get ready to paste it when prompted. 
You're good to go!
