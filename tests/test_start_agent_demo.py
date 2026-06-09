from start_agent import SimpleAgent, ToolRegistry
from start_agent.tools.builtin.calculator import CalculatorTool, calculate


class FakeLLM:
    """Small LLM stub for tests that should not call external services."""

    provider = "fake"

    def __init__(self, response: str = "demo response"):
        self.response = response
        self.calls = []

    def invoke(self, messages, **kwargs):
        self.calls.append({"messages": messages, "kwargs": kwargs})
        return self.response


def test_calculator_demo():
    tool = CalculatorTool()

    assert tool.name == "python_calculator"
    assert tool.run({"input": "2 + 3 * 4"}) == "14"
    assert calculate("sqrt(16)") == "4.0"


def test_tool_registry_function_demo():
    registry = ToolRegistry()
    registry.register_function(
        name="echo",
        description="Return the input text unchanged.",
        func=lambda text: text,
    )

    assert registry.list_tools() == ["echo"]
    assert registry.execute_tool("echo", "hello start-agent") == "hello start-agent"
    assert "echo" in registry.get_tools_description()


def test_simple_agent_demo_without_real_llm():
    llm = FakeLLM(response="StartAgent is ready.")
    agent = SimpleAgent(
        name="demo-agent",
        llm=llm,
        system_prompt="You are a concise assistant.",
        enable_tool_calling=False,
    )

    result = agent.run("Say hello.")

    assert result == "StartAgent is ready."
    assert len(agent.get_history()) == 2
    assert agent.get_history()[0].role == "user"
    assert agent.get_history()[1].role == "assistant"
    assert llm.calls[0]["messages"][0]["role"] == "system"
    assert llm.calls[0]["messages"][-1]["content"] == "Say hello."
