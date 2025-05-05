from boost import Boost

class HealBoost(Boost):
    def apply_to_player(self, player):
        player.hits += 20
        if player.hits > 100:  # Max zdravie (ak chceš limit)
            player.hits = 100
