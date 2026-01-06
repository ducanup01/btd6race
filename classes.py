from pydantic import BaseModel
from typing import Optional


class RaceLeaderboard(BaseModel):
    error: Optional[str] = None
    success: bool
    body: list
    model: dict
    next: Optional[str] = None
    prev: Optional[str] = None
    maxPages: Optional[int] = None


class Racer(BaseModel):
    displayName: str
    score: int
    scoreParts: list
    submissionTime: int
    profile: str


class RacerProfile(BaseModel):
    error: Optional[str] = None
    success: bool
    body: dict
    model: dict
    next: Optional[str] = None
    prev: Optional[str] = None



