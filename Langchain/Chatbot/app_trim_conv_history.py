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

#Managing Conversation History by filtering old messages

from langchain_core.runnables import RunnablePassthrough


def filter_messages(messages, k=10):
    return messages[-k:]

system_template = "You're an assistant who speaks in {language}. Respond in 20 words or fewer. Answer all questions to the best of your ability."

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = (
    prompt
    | model
)
demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="messages",
)

from langchain_core.runnables import RunnablePassthrough


def trim_messages(chain_input):
    stored_messages = demo_ephemeral_chat_history_for_chain.messages
    if len(stored_messages) <= 2:
        return False

    demo_ephemeral_chat_history_for_chain.clear()

    for message in stored_messages[-2:]:
        demo_ephemeral_chat_history_for_chain.add_message(message)

    return True


chain_with_trimming = (
    RunnablePassthrough.assign(messages_trimmed=trim_messages)
    | chain_with_message_history
)

config = {"configurable": {"session_id": "abc99"}}

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="hi! I'm Ajay")], "language": "English"},
    config=config,
)

print(response.content)
print(demo_ephemeral_chat_history_for_chain.messages)

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="whats my name?")], "language": "English"},
    config=config,
)

print(response.content)
print(demo_ephemeral_chat_history_for_chain.messages)

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="I like vanilla ice cream")], "language": "English"},
    config=config,
)

print(response.content)
print(demo_ephemeral_chat_history_for_chain.messages)

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="whats 2 + 2?")], "language": "English"},
    config=config,
)

print(response.content)
print(demo_ephemeral_chat_history_for_chain.messages)

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="having fun?")], "language": "English"},
    config=config,
)

print(response.content)
print(demo_ephemeral_chat_history_for_chain.messages)

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="what's my fav ice cream")], 
     "language": "English"
    },
    config=config,
)

print(response.content)
print(demo_ephemeral_chat_history_for_chain.messages)

response = chain_with_trimming.invoke(
    {"messages": [HumanMessage(content="what's my name")], 
     "language": "English"
    },
    config=config,
)

print(response.content)

print(demo_ephemeral_chat_history_for_chain.messages)