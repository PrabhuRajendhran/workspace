import os
from dotenv import load_dotenv
load_dotenv()

print('LANGCHAIN_TRACING_V2:  {}'.format(os.environ['LANGCHAIN_TRACING_V2']))
print('LANGCHAIN_API_KEY: {}'.format(os.environ['LANGCHAIN_API_KEY']))
print('ANTHROPIC_API_KEY: {}'.format(os.environ['ANTHROPIC_API_KEY']))

from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-3-sonnet-20240229")

from langchain_core.messages import HumanMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

#Simple Persistence Layer

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "abc5"}}

response = with_message_history.invoke(
    [HumanMessage(content="Hi! I'm Bob")],
    config=config,
)

print(response.content)


response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print(response.content)