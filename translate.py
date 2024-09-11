# -*- coding: utf-8 -*-
"""chat_gpt.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bLbEsozeICdOI087z48zh1JJtD6vxDxs
"""


from openai import OpenAI

class ChatAPI:
  def __init__(self, prompt=None):
        self.prompt = prompt
      



  def chatgptAPI(self, api_key=None):
      client = OpenAI(
      # defaults to os.environ.get("OPENAI_API_KEY")
      api_key = api_key,
      )
      response = client.chat.completions.create(
          model="gpt-4o",
          messages=[{"role": "user", "content": self.prompt}]
      )
      return response.choices[0].message.content.strip()

