import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import Markdown



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key="AIzaSyDUsioafMtEVN6nE4bi30fJ0HPoarLoVAE")

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("i need help")


print(response.text)
