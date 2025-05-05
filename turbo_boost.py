from boost import Boost

class TurboBoost(Boost):
    def apply_to_player(self, player):
        player.activate_speed_boost()
