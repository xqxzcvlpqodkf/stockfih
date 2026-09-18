from fastapi import FastAPI, Query, HTTPException
import chess
import chess.engine

app = FastAPI()
STOCKFISH_PATH = "/usr/local/bin/stockfish"

@app.get("/")
async def evaluate(
    fen: str, 
    time: float = Query(default=1.5, le=2.0), 
    depth: int = Query(default=20, le=25)
):
    try:
        board = chess.Board(fen)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid FEN string")

    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    try:
        result = engine.analyse(board, chess.engine.Limit(time=time, depth=depth))
        best_move = result["pv"][0].uci() if "pv" in result and result["pv"] else None
        score_obj = result["score"].relative
        eval_score = f"mate {score_obj.mate()}" if score_obj.is_mate() else round(score_obj.score() / 100.0, 2)

        return {
            "best_move": best_move,
            "eval": eval_score,
            "time_spent": time,
            "depth_reached": result.get("depth")
        }
    finally:
        engine.quit()
