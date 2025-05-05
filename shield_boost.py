from boost import Boost

class Shield(Boost):
    def apply_to_player(self, player):
        player.activate_shield()
