"""异常体系"""

class StartAgentException(Exception):
    """StartAgent基础异常类"""
    pass

class LLMException(StartAgentException):
    """LLM相关异常"""
    pass

class AgentException(StartAgentException):
    """Agent相关异常"""
    pass

class ConfigException(StartAgentException):
    """配置相关异常"""
    pass

class ToolException(StartAgentException):
    """工具相关异常"""
    pass
