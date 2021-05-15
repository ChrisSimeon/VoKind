# General

## What is this for?
Vokind is an Application to help you learn your vocabulary. I came up with the idea while I was myself in France struggeling to learn the language. I'm not a big fan of vocabulary lists. Language is a very personal and private thing you won't find the specific vocabulary needed in your enviroment in any vocabulary lists. The best way to learn a language is to confront yourself with it in your ordinary life: with books, movies and of course (if possible) people.
But, as I am not what you would call "a natural" with languages I needed to hear or read a word multiple times before I beginn to remember it. As you can imagine I was a slow learner. 
I tried multiple techniques to be better in french. I used Anki for several years now and it is a great application to learn vocabulary. Make it a habit to learn 20 Minutes a day and you will progress rapidly. The problem was how to get the stuff in Anki. I already said that I'm not a fan of vocabulary lists so I had to make them on my own, which took a lot of time just copy and pasting. I also had to remember which words I would have to learn. For some weeks I always ran around with a notebook, writing down all vocabulary I did not know to add it to my Anki later. But this caused a lot of friction: to with every book I had to stop and write down unknown vokabulary, during lectures I always had to look up words, follow the lecture and write down on an extra list the words I did not know only to look it up again later that day to make my cards. 

At least for books I read on my Kindle I found a solution: there is an app to import the vocabulary into your Anki libary. But the translations were mediocre at best and I had to rework every second card. So I wrote a first version of Vokind (in Excel with Virtual Basic) which exported the vocabulary from Kindle into an Excel table and scraped translations. From this point on I started to continue to work on the app, changed from VBA to Python, implemented a workflow for Alfred to lookup and save my vokabs and so on. 

The idea of Vokind started to take shape: An application that was easy accessible at any time so you would have a personal vocabulary list with all the words you need most. To reduce the friction of copy and pasting it in your Anki this list will search for translations and make a card itself. This card would also give you context: where did you hear or read this word? As words can change their meaning depending on the context, it was important to not only translate the word but also gather information about what the word could mean in which context. In general it is better to learn a word in context because it is conrete and imaginable.

# Remarks
This Application is nothing but a first draft and probably won't work on your comupter without changing the code to work in your specific envirorement.

I won't take any responsibility for any harm caused by this application on your devices and I strongly recommend to not use this application if you don't know exactly what you're doing.

Nethertheless I'm thankful for any input to help me code better.

# Roadmap
## Version 1.0
2. [ ] Readme
    - [ ] How-to installation
3. [ ] GUI


## Version 2.0 - Rework the Code Base
10. [ ] Commment and clean up code
5. [ ] Rework the Database 
6. [ ] Reduce redundancy
9. [ ] Use Wiki API instead of Webscraping
12. [ ] Automate Installation Prozess
    1.  [ ] Cards in Anki

## Later Versions
1. Build an Android Version (iOS isn't planned as I don't have an iPhone and can't test it. If anybody wan't to build an iOS Version please contact me) 
2. Direct Feedback to Wikipedia. -> Directly propose alternative translations in the App and send it to wikipedia to improve the translation Database for all. 
7. Maybe a possibility to connect to the calendar to get context for what you did when you searched for a specific word. Let's say you meet Cécilia in a Café from 10 - 11 and you search for a word in this period. Vokind will write on your card that you searched for the word while being in the café with Cécilia so you habe a context for this word.  
