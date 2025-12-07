from universe.ai_v6.composer import Composer
from universe.ai_v6.discourse_memory import DiscourseMemory
from universe.ai_v6.grammar_rules import GrammarRules
from universe.ai_v6.lexicon import Lexicon
from universe.ai_v6.parser import Parser
from universe.ai_v6.semantic_frame import SemanticFrame


class AIPackV6:
    """
    Integration scaffold for AI Pack v6 (glyph grammar + compositional language).
    Requires agents to expose: emotion (optional), intent (optional).
    """

    def __init__(self, engine):
        self.engine = engine
        self.lexicon = Lexicon()
        self.parser = Parser()
        self.grammar = GrammarRules()
        self.composer = Composer()
        self.frame = SemanticFrame()
        self.discourse = DiscourseMemory()

    def speak(self, agent, *words):
        sentence = self.composer.compose(words, self.lexicon)
        if self.grammar.is_valid_sequence(sentence.glyphs):
            return sentence
        return None

    def hear(self, agent, sentence):
        tree = self.parser.parse(sentence)
        self.frame.interpret(tree, agent)
        self.discourse.add(sentence)
