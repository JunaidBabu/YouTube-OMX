from sqlalchemy import *

engine = create_engine('sqlite:///videos.db', echo=True)

meta = MetaData()

videos = Table('videos', meta,
    Column('item_id', Integer, primary_key=True),
    Column('video_id', String),
    Column('video_title', String(60)),
    Column('video_url', String, nullable=True)
)
videos.create(engine)