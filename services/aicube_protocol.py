from .cube_protocol import CubeProtocol

class AICubeProtocol(CubeProtocol):
    """
    AI-specific specialization.
    Can override preprocessing for text, prompt-ready formats, etc.
    Currently inherits all core behavior from CubeProtocol.
    """
    pass
