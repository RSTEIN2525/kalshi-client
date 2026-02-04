import pandas as pd
from pydantic import BaseModel

def pydantic_model_to_dataframe(models: list[BaseModel]) -> pd.DataFrame:
    # Pydantic Model -> Python Dictionary for Each in List
    # Then Pandas Can Directly Ingest Dictionaries to Create DF
    return pd.DataFrame([m.model_dump() for m in models])
