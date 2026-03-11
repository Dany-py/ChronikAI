
from infrastructure.db.models import EventCreate, Event, Session, SessionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.database import get_db
from sqlalchemy.future import select
from apps.watcher import Tracker
from datetime import datetime
import asyncio
import secrets


class DB_Extract:
    
    def __init__(self, limit = 10, table = Event):
        self.limit = limit
        self.table = table
    
    async def extract_in_db(self, page_number: int):
        page_size = self.limit
        offset = (page_number - 1) * page_size
        async for session in get_db():
            query = (
                select(self.table)
                .order_by(self.table.timestamp)
                .offset(offset)
                .limit(page_size)
            )
            try:
                db: AsyncSession = session
                result = await db.execute(query)
                content = result.scalars().all()
                #print('Contenu retourné :', content)
                event_list = []
                for event in content:
                    timestamp = event.timestamp[0]# if isinstance(event.timestamp, int) else int(event.timestamp)
                    event_date = datetime.fromtimestamp(timestamp)
                    event_list.append({
                        "id": event.id,
                        "session": event.session_uid,
                        "date": event_date.strftime("%Y-%m-%d_%H-%M-%S"),
                        "app_name": event.app_name,
                        "window_title": event.window_title,
                        "entry": event.entry
                    })
                print("Donnée formatée :", event_list)
            except Exception as e:
                await db.rollback()
                print(f"Erreur lors de l'export en base de données: {e}")
                raise
            finally:
                await db.close()

if __name__ == "__main__":
    db_extract = DB_Extract(10, Event)
    asyncio.run(db_extract.extract_in_db(1))