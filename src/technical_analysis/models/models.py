from pydantic import BaseModel

class Data(BaseModel):
    start_ts: int
    end_ts: int
    open: float
    close : float
    high : float
    low : float
    volume : float
    ask : float
    bid : float
    spread : float
    midprice : float
    open_interest : float
