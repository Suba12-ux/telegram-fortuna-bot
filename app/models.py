from pydantic import BaseModel

class PaperAnalysis(BaseModel):
        title: str
        abstract_summary: str