"""
Minimal demo wiring UniverseEngineV6 (CPU fallback) with a couple of entities.

Run with:
    python demos/demo_v6_cpu.py
GPU hardware is optional; if CUDA is missing the engine will fall back to CPU integration.
"""

from universe.components.position import Position
from universe.components.velocity import Velocity
from universe.engine.universe_engine_v6 import UniverseEngineV6
from universe.entities.entity import Entity


def main():
    engine = UniverseEngineV6(max_entities=10)

    e1 = Entity()
    e1.add_component(Position(0.0, 0.0, 0.0))
    e1.add_component(Velocity(1.0, 0.5, 0.0))
    engine.add_entity(e1)

    e2 = Entity()
    e2.add_component(Position(5.0, -2.0, 0.0))
    e2.add_component(Velocity(-0.5, 0.8, 0.0))
    engine.add_entity(e2)

    for step in range(5):
        engine.step(0.5)
        print(f"Step {step}:")
        for ent in engine.entities.values():
            pos = ent.get_component(Position)
            print(f"  Entity {ent.id}: pos=({pos.x:.2f}, {pos.y:.2f})")


if __name__ == "__main__":
    main()
