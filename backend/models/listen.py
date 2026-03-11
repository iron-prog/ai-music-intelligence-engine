from dataclasses import dataclass
from datetime import datetime


@dataclass
class Listen:

    track_name: str
    artist_name: str
    album_name: str
    played_at: datetime