import os

from llama_index.core.agent import AgentRunner, FunctionCallingAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI

from hyperpocket_llamaindex import PocketLlamaindex


def build():
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    pocket = PocketLlamaindex(
        tools=[
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/slack/get-messages",
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/slack/post-message",
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/linear/get-issues",
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/google/get-calendar-events",
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/google/get-calendar-list",
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/google/insert-calendar-events",
            "https://github.com/vessl-ai/hyperpocket/tree/main/tools/github/list-pull-requests",
        ]
    )
    tools = pocket.get_tools()

    memory = ChatMemoryBuffer.from_defaults(chat_history=[], llm=llm)

    agent = FunctionCallingAgent.from_tools(
        tools=tools, llm=llm, memory=memory, verbose=True
    )

    return agent


def run(agent: AgentRunner):
    while True:
        print("user(q to quit) : ", end="")
        user_input = input()
        if user_input == "q":
            print("bye")
            break
        elif user_input == "":
            continue

        agent.chat(user_input)


if __name__ == "__main__":
    agent = build()
    run(agent)
