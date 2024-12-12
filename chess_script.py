import requests
import chess_script
import chess.engine
import sys

# Chess.com username and the path to Stockfish
USERNAME = "hymical"
STOCKFISH_PATH = "C:/Program Files/stockfish/stockfish-windows-x86-64-avx2.exe"  

def get_live_game(username):
    url = f"https://api.chess.com/pub/player/{username}/games"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data from Chess.com")
        sys.exit(1)
    
    games = response.json().get('games', [])
    for game in games:
        if game.get('time_class') == 'live' and game.get('end_time') is None:
            pgn = game.get('pgn')
            return pgn
    return None

def get_fen_from_pgn(pgn):
    board = chess_script.Board()
    moves = pgn.split("\n\n")[1].split() 
    for move in moves:
        try:
            board.push_san(move)
        except ValueError:
            break
    return board

def suggest_best_move(board, stockfish_path):
    with chess_script.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        result = engine.play(board, chess_script.engine.Limit(time=1.0))  # 1-second analysis
        return result.move

def main():
    pgn = get_live_game(USERNAME)
    if not pgn:
        print("No live games found.")
        return
    
    board = get_fen_from_pgn(pgn)
    print("Current Board Position:")
    print(board)
    
    best_move = suggest_best_move(board, STOCKFISH_PATH)
    print(f"Suggested Best Move: {best_move}")

if __name__ == "__main__":
    main()
