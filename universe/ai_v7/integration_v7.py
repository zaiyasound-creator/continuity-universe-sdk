from universe.ai_v6.grammar_rules import GrammarRules
from universe.ai_v6.lexicon import Lexicon
from universe.ai_v6.parser import Parser
from universe.ai_v6.semantic_frame import SemanticFrame
from universe.ai_v6.sentence import Sentence
from universe.ai_v7.composer import Composer
from universe.ai_v7.discourse_engine import DiscourseEngine
from universe.ai_v7.dialect_engine import DialectEngine
from universe.ai_v7.drift_engine import DriftEngine
from universe.ai_v7.glyph_evolution import GlyphEvolution
from universe.ai_v7.language_family import LanguageFamily
from universe.ai_v7.language_state import LanguageState
from universe.ai_v7.morphology import Morphology
from universe.ai_v7.phonology import Phonology


class AIPackV7:
    """
    Integration scaffold for AI Pack v7 (full language evolution).
    Expects agents to support emotion and an intent strength attribute when inflecting.
    """

    def __init__(self, engine, region_id: int = 0):
        self.engine = engine
        self.lang_state = LanguageState()
        self.morph = Morphology()
        self.phono = Phonology()
        self.evolve = GlyphEvolution()
        self.discourse = DiscourseEngine()
        self.drift = DriftEngine()

        self.family = LanguageFamily()
        self.dialect = DialectEngine(region_id)
        self.family.register(region_id, self.dialect)

        self.lexicon = Lexicon()
        self.parser = Parser()
        self.grammar = GrammarRules()
        self.composer = Composer()
        self.frame = SemanticFrame()

    def process_sentence(self, agent, sentence):
        glyphs = sentence.glyphs

        # Morphology
        for g in glyphs:
            strength = getattr(agent, "intent_strength", 0.5)
            g.shape_id, g.tag = self.morph.inflect(g, getattr(agent, "emotion", None), strength)

        # Phonology
        for g in glyphs:
            g.shape_id = self.phono.prosody_shift(g, getattr(agent, "emotion", None))

        # Dialect
        for g in glyphs:
            self.dialect.apply(g)

        # Drift/mutation
        for g in glyphs:
            self.evolve.mutate(g)

        self.lang_state.increment()

    def reply(self, agent, last_sentence):
        words = self.discourse.reply(agent, last_sentence)
        if not words:
            return None
        sentence = self.composer.compose(words, self.lexicon)
        if not self.grammar.is_valid_sequence(sentence.glyphs):
            return None
        return sentence
