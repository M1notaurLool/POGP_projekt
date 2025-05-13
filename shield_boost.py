from boost import Boost

class Shield(Boost):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.id = f"shield:{x},{y}"

    def apply_to_player(self, player):
        player.activate_shield()
