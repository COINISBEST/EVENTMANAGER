from sqlalchemy import Index

class Event(Base):
    # Add indexes
    Index('idx_event_start_date', Event.start_date)
    Index('idx_event_status', Event.status)
    Index('idx_event_organizer', Event.organizer_id) 