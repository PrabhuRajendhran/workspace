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

# Simple Persistence Layer

# with_message_history = RunnableWithMessageHistory(model, get_session_history)

# response = with_message_history.invoke(
#     [HumanMessage(content="Hi! I'm Bob")],
#     config=config,
# )

# print(response.content)


# response = with_message_history.invoke(
#     [HumanMessage(content="What's my name?")],
#     config=config,
# )

# print(response.content)


# Customizing with Prompts
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# system_template = "You are a helpful assistant. Answer all questions to the best of your ability."

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_template),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

# chain = prompt | model

# response = chain.invoke(
#     {"messages": [HumanMessage(content="hi! I'm bob")], "language": "Spanish"}
# )

# print(response.content)

# with_message_history = RunnableWithMessageHistory(chain, get_session_history)

# config = {"configurable": {"session_id": "abc5"}}

# response = with_message_history.invoke(
#     [HumanMessage(content="Hi! I'm Jim")],
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     [HumanMessage(content="What's my name?")],
#     config=config,
# )

# print(response.content)


#Adding complexity by providing multiple input keys

# system_template = "You're an assistant who speaks in {language}. Respond in 20 words or fewer"

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_template),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

# chain = prompt | model

# with_message_history = RunnableWithMessageHistory(
#     chain,
#     get_session_history,
#     input_messages_key="messages",
# )

# config = {"configurable": {"session_id": "abc26"}}

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="hi! I'm todd")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="whats my name?")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

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
    RunnablePassthrough.assign(messages=lambda x: filter_messages(x["messages"]))
    | prompt
    | model
)

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

# config = {"configurable": {"session_id": "abc99"}}

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="hi! I'm Ajay")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="whats my name?")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="I like vanilla ice cream")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="whats 2 + 2?")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="having fun?")], "language": "Spanish"},
#     config=config,
# )

# print(response.content)

# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="what's my fav ice cream")], 
#      "language": "Spanish"
#     },
#     config=config,
# )

# print(response.content)

#Streaming

config = {"configurable": {"session_id": "abc15"}}
for r in with_message_history.stream(
    {
        "messages": [HumanMessage(content="hi! I'm todd. tell me a joke")],
        "language": "Spanish",
    },
    config=config,
):
    print(r.content, end="")

#To store message history in AWS DynamoDB , Refer : https://python.langchain.com/v0.2/docs/integrations/memory/aws_dynamodb/