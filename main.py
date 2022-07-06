from curses import echo
import os
import openai
from torch import true_divide

#Create a file storage for AI presets






#Gets the user's basic parameters for text completion/generation.
promptLength = int(input("How long you would like your response? (In character length; 1-4000) "))
promptRandomness = float(("0." + input("How random would you like your prompt? (1-10) ")))
promptMessage = input("Prompt: ")

#Sets my OpenAI unique key, account reqiured to submit prompts
openai.api_key = "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"

#Send the pre-set information to the OpenAI server to return the text completion
response = openai.Completion.create(
  model="text-davinci-002",
  prompt=promptMessage,
  temperature=promptRandomness,
  max_tokens=promptLength,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

#This eliminates all the outside information that is given as a response by the OpenAI completion
print(response["choices"][0]["text"])