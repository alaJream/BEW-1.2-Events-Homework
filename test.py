from events_app.models import *
from events_app import db
from datetime import datetime

user1 = Guest(name='Charlie', email='charlieg1103@gmail.com', phone='209-2092')
event1 = Event(title='Fun Event', description='this is a fun event :)', date_and_time=datetime.now())

user1.events_attending.append(event1)
db.add