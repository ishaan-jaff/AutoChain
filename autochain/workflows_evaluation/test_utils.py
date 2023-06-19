import argparse
import logging
from typing import List, Optional

from autochain.agent.support_agent.support_agent import SupportAgent
from autochain.chain.chain import Chain
from autochain.memory.base import BaseMemory
from autochain.memory.buffer_memory import BufferMemory
from autochain.models.base import BaseLanguageModel
from autochain.models.chat_openai import ChatOpenAI
from autochain.tools.base import Tool


def get_test_args():
    """Adding arguments for running test"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interact",
        "-i",
        action="store_true",
        help="if run interactively",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="if show detailed contents, such as intermediate results and prompts",
    )
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    return args


def create_chain_from_test(
    tools: List[Tool],
    memory: Optional[BaseMemory] = None,
    llm: Optional[BaseLanguageModel] = None,
    agent_cls=SupportAgent,
    **kwargs
):
    """
    Create Chain for running tests
    Args:
        tools: list of autochain tools
        memory: memory store for chain
        llm: model for agent
        agent_cls: metadata class for instantiating agent
    Returns:
        Chain
    """
    llm = llm or ChatOpenAI(temperature=0)
    memory = memory or BufferMemory()
    agent = agent_cls.from_llm_and_tools(llm=llm, tools=tools, **kwargs)
    return Chain(agent=agent, memory=memory)