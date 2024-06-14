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

# Customizing with Prompts
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system_template = "You're an assistant who speaks in {language}. Respond in 20 words or fewer. Answer all questions to the best of your ability."

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

response = chain.invoke(
    {"messages": [HumanMessage(content="hi! I'm bob")], "language": "Spanish"}
)

print(response.content)

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

config = {"configurable": {"session_id": "abc5"}}

response = with_message_history.invoke(
    {"messages": [HumanMessage(content="hi! I'm todd")], "language": "English"},
    config=config,
)

print(response.content)

response = with_message_history.invoke(
    {"messages": [HumanMessage(content="whats my name?")], "language": "English"},
    config=config,
)

print(response.content)