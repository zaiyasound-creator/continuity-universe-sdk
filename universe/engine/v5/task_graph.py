class TaskNode:
    def __init__(self, subsystem):
        self.subsystem = subsystem
        self.dependents = []


class TaskGraph:
    def __init__(self):
        self.nodes = []

    def add(self, subsystem):
        node = TaskNode(subsystem)
        self.nodes.append(node)
        return node

    def link(self, parent: TaskNode, child: TaskNode):
        parent.dependents.append(child)

    def roots(self):
        return [n for n in self.nodes if all(n not in c.dependents for c in self.nodes)]
