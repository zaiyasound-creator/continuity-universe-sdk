from universe.ai_v6.syntax_tree import SyntaxTree


class Parser:
    """
    Converts sentences into syntax trees (minimal S-A-O parsing).
    """

    def parse(self, sentence):
        glyphs = sentence.glyphs
        if len(glyphs) == 2:
            return SyntaxTree(subject=glyphs[0], action=glyphs[1])
        if len(glyphs) >= 3:
            return SyntaxTree(subject=glyphs[0], action=glyphs[1], object=glyphs[2])
        return SyntaxTree()
