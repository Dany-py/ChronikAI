
from infrastructure.db.models import EventCreate, Event, Session, SessionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.database import get_db
from apps.watcher import Tracker
from datetime import datetime
import asyncio
import secrets

class DB_Insert:
    """Analyseur d'activité utilisateur."""
    
    def __init__(self):
        self.tracker = Tracker(idle_threshold=10, verbose=True, blacklist_app = [], duration = 60, replay = True)
        self.thread = None
        
    def start(self):
        """Démarre l'analyseur."""
        self.tracker.run() 
    
    def stop(self):
        """Arrête l'analyseur."""
        self.tracker.stop()

    def get_stats(self):
        """Génère des statistiques d'utilisation."""
        data = self.tracker.get_activity_data()
        stats = {
            'total_windows': len(data),
            'windows_with_writing': sum(1 for d in data.values() if d['write']),
            'total_phrases': sum(len(d['text']) for d in data.values())
        }
        return stats
    

    async def export_to_db(self):
        """Exporte les données en base de données."""
        tracker_data = self.tracker.get_activity_data()
        tracker_session_uid = secrets.token_hex(6)
        session__uid = SessionCreate(
            session_uid = tracker_session_uid
        )
        async for session in get_db():
            db: AsyncSession = session
            try:
                for key, value in tracker_data.items():
                    content = "".join(tracker_data[key]['text'])
                    
                    event = EventCreate(
                        app_name=value['app_name'],
                        timestamp=int(value['timestamp']),
                        window_title=str(value['title']),
                        duration=int(value['duration']),
                        entry=content,
                        session_uid=tracker_session_uid,
                        is_consulted=bool(value['consulted']),
                        is_written=bool(value['write']),
                    )
                    
                    # Convertir le modèle Pydantic en modèle SQLAlchemy
                    db_event = Event(**event.model_dump())
                    db.add(db_event)

                db_session = Session(**session__uid.model_dump())
                db.add(db_session) 
                await db.commit()
            except Exception as e:
                await db.rollback()
                print(f"Erreur lors de l'export en base de données: {e}")
                raise
    

if __name__ == "__main__":
    db_insert = DB_Insert()
    db_insert.start()    
    asyncio.run(db_insert.export_to_db())
    db_insert.stop()
