import os
from dotenv import load_dotenv
load_dotenv()

print('LANGCHAIN_TRACING_V2:  {}'.format(os.environ['LANGCHAIN_TRACING_V2']))
print('LANGCHAIN_API_KEY: {}'.format(os.environ['LANGCHAIN_API_KEY']))
print('ANTHROPIC_API_KEY:     {}'.format(os.environ['ANTHROPIC_API_KEY']))

#!/usr/bin/env python
from typing import List
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langserve import add_routes

# 1. Create prompt template
system_template = "Translate the following into {language}:"
human_template = "{text}"

prompt = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", human_template)
    ])

# 2. Create model
model = ChatAnthropic(model="claude-3-sonnet-20240229")

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)