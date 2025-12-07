from universe.ai_v6.parser import Parser
from universe.ai_v6.semantic_frame import SemanticFrame


class DiscourseMemory:
    """
    Multi-sentence context buffer.
    """

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.sentences = []
        self.parser = Parser()
        self.frame = SemanticFrame()

    def add(self, sentence):
        self.sentences.append(sentence)
        if len(self.sentences) > self.capacity:
            self.sentences.pop(0)

    def last_meaning(self, agent):
        if not self.sentences:
            return
        tree = self.parser.parse(self.sentences[-1])
        self.frame.interpret(tree, agent)
