from ..services.world import WorldService


class ContextManager:
    # Application Level Services
    world_service: WorldService | None = None

    def __init__(self, world_service: WorldService):
        if self.world_service is None:
            self.world_service = world_service
            print("[ContextManager] assigned new world service")
        else:
            print("[ContextManager] world service already assigned")


context = ContextManager(world_service=WorldService())
