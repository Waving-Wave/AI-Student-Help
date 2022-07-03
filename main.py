from curses import echo
import os
import openai
from torch import true_divide

#Create a file storage for AI presets

promptLength = int(input("How long you would like your response? (In character length; 1-4000) "))
promptRandomness = float(("0." + input("How random would you like your prompt? (1-10) ")))
promptMessage = input("Prompt: ")

openai.api_key = "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"

response = openai.Completion.create(
  model="text-davinci-002",
  prompt=promptMessage,
  temperature=promptRandomness,
  max_tokens=promptLength,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response["choices"][0]["text"])