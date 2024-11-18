class GameState:
    def __init__(self, game, current_player):
        self.game = game  # The current game instance
        self.current_player = current_player  # The index of the current player (0 or 1)

    def get_possible_moves(self):
        moves = []
        current_player = self.game.players[self.current_player]
        for move_pion in [current_player.pion1, current_player.pion2]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx, dy) != (0, 0):
                        if current_player.isValidMovement(move_pion, dx, dy):
                            for build_pion in [current_player.pion1, current_player.pion2]:
                                build_pion_test = build_pion.pionCopy()
                                build_pion_test.x = move_pion.x + dx
                                build_pion_test.y = move_pion.y + dy
                                for bx in [-1, 0, 1]:
                                    for by in [-1, 0, 1]:
                                        if (bx, by) != (0, 0):
                                            if build_pion_test.isValidBuilding(bx, by):
                                                moves.append((move_pion.pionID, dx, dy, build_pion.pionID, bx, by))
        return moves

    def apply_move(self, move):
        move_pion_id, dx, dy, build_pion_id, bx, by = move
        new_game = self.game.gameCopy()  # Create a deep copy of the game
        move_pion = new_game.players[self.current_player].pion1 if move_pion_id == 1 else new_game.players[self.current_player].pion2
        build_pion = new_game.players[self.current_player].pion1 if build_pion_id == 1 else new_game.players[self.current_player].pion2
        movePlayer = new_game.players[self.current_player]
        print("Applying move: ", move_pion_id, dx, dy, build_pion_id, bx, by)
        print("Current player apply: ", movePlayer.name)
        # Move the pion, ensuring the move is valid
        if movePlayer.isValidMovement(move_pion, dx, dy):
            print("Moving pion")
            movePlayer.move(move_pion, dx, dy)
        else:
            print("Invalid move")
        # Build if valid
        if build_pion.isValidBuilding(bx, by):
            print("build in", build_pion.x + bx, build_pion.y + by)
            build_pion.build(bx, by)
            print("Building")
            new_game.printBoard()
        else:
            print("Invalid building")
        return GameState(new_game, (self.current_player + 1) % 2)  # Return the new game state with the next player

    def is_terminal(self):
        if not hasattr(self.game, 'players') or not self.game.players:
            print("Error: Game has no players!")
            return False
        for player in self.game.players:
            print(f"Checking player {player.name}")
            for pion in [player.pion1, player.pion2]:
                if self.game.tableau_de_jeu[pion.x][pion.y] == 3:
                    print("Player ", player.name, " has won!")
                    return True  # A player has won by reaching the third level
        # Check if the current player can move or build
        if not self.get_possible_moves():
            print(f"Player {self.game.players[self.current_player].name} has no valid moves and loses!")
            return True
        print("No player has won yet")
        return False

    def evaluate(self):
        score = 0
        for player in self.game.players:
            for pion in [player.pion1, player.pion2]:
                score += self.game.tableau_de_jeu[pion.x][pion.y]  # Sum the heights of the buildings
        return score if self.current_player == 0 else -score  # Positive score for player 0, negative for player 1

    def stateCopy(self):
        new_game = self.game.gameCopy()
        return GameState(new_game, self.current_player)

def minimax(state, depth, alpha, beta, maximizing_player):
    print("Depth: ", depth)
    print("Current player:", state.current_player)
    if depth == 0 or state.is_terminal():
        return state.evaluate(), []

    moves = state.get_possible_moves()
    if maximizing_player:
        max_eval = float('-inf')
        best_move_sequence = []
        for move in moves:
            new_state = state.apply_move(move)
            eval, move_sequence = minimax(new_state, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move_sequence = [move] + move_sequence
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        print("Best move sequence: ", best_move_sequence)
        return max_eval, best_move_sequence
    else:
        min_eval = float('inf')
        best_move_sequence = []
        for move in moves:
            new_state = state.apply_move(move)
            eval, move_sequence = minimax(new_state, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move_sequence = [move] + move_sequence
            beta = min(beta, eval)
            if beta <= alpha:
                break
        print("Best move sequence: ", best_move_sequence)
        return min_eval, best_move_sequence
