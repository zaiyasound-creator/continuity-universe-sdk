class DiscourseEngine:
    """
    Multi-sentence interaction logic to produce replies.
    """

    def reply(self, agent, last_sentence):
        if not last_sentence:
            return None

        glyphs = last_sentence.glyphs
        if len(glyphs) < 2:
            return None

        sub = glyphs[0].tag
        act = glyphs[1].tag

        if act == "migrate":
            return ["group", "follow", "leader"]
        if act == "danger":
            return ["group", "flee", "danger"]
        return ["group", "acknowledge", "leader"]
