from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import os  

bot = ChatBot('Lindy')

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

print('Finished training')
