import os
import openai

def read_prompt():
  try:
    file = open('prompt.txt', mode='r')
    prompt = file.read()
    file.close()
    return prompt
  except FileNotFoundError:
    return 'You will read a post from the subreddit and respond with a joke.'

def generate_response(subreddit_name, post_content):
  prompt = f'You are within the {subreddit_name} subreddit. {read_prompt()}\n\n{post_content}'
  
  try:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.8,
      max_tokens=256,
    )
  except openai.error.Timeout as e:
    #Handle timeout error, e.g. retry or log
    print(f"OpenAI API request timed out: {e}")
    return None
  except openai.error.APIError as e:
    #Handle API error, e.g. retry or log
    print(f"OpenAI API returned an API Error: {e}")
    return None
  except openai.error.APIConnectionError as e:
    #Handle connection error, e.g. check network or log
    print(f"OpenAI API request failed to connect: {e}")
    return None
  except openai.error.InvalidRequestError as e:
    #Handle invalid request error, e.g. validate parameters or log
    print(f"OpenAI API request was invalid: {e}")
    return None
  except openai.error.AuthenticationError as e:
    #Handle authentication error, e.g. check credentials or log
    print(f"OpenAI API request was not authorized: {e}")
    return None
  except openai.error.PermissionError as e:
    #Handle permission error, e.g. check scope or log
    print(f"OpenAI API request was not permitted: {e}")
    return None
  except openai.error.RateLimitError as e:
    #Handle rate limit error, e.g. wait or log
    print(f"OpenAI API request exceeded rate limit: {e}")
    return None
  except:
    print("Something bad happend.")
    return None

  response_text = response.choices[0].text

  if len(response_text) < 5:
    #too short be to be meaningful
    return None

  return response_text.strip()
