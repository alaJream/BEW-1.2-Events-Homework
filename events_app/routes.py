"""Import packages and modules."""
import email
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""

    # TODO: Get all events and send to the template
    events = Event.query.all()

    return render_template('index.html', events=events)


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')

        # TODO: Create a new event with the given title, description, & 
        # datetime, then add and commit to the database
        event = Event(title=new_event_title, description=new_event_description, date_and_time=date_and_time)
        db.session.add(event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""

    # TODO: Get the event with the given id and send to the template
    event = Event.query.filter_by(id=event_id).first()
    print(event.date_and_time)
    date_time = event.date_and_time
    date = f'{date_time.month}/{date_time.day}/{date_time.year}'
    time = f'{date_time.hour}:{date_time.minute}'
    
    return render_template('event_detail.html', event=event, date=date, time=time)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # TODO: Get the event with the given id from the database
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')
    event = Event.query.filter_by(id=event_id).first()

    if is_returning_guest:
        # TODO: Look up the guest by name. If the guest doesn't exist in the 
        # database, render the event_detail.html template, and pass in an error
        # message as `error`.
        guest_found = Guest.query.filter_by(name=guest_name).first()
        if not guest_found:
            return render_template('event_detail.html', error='guest does not exist')

        # TODO: If the guest does exist, add the event to their 
        # events_attending, then commit to the database.
        event.guests.append(guest_found)
        db.session.commit()

    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        # TODO: Create a new guest with the given name, email, and phone, and 
        # add the event to their events_attending, then commit to the database.
        new_guest = Guest(name=guest_name, email=guest_email, phone=guest_phone)
        event.guests.append(new_guest)

    db.session.commit()
    
    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # TODO: Get the guest with the given id and send to the template
    found_guest = Guest.query.filter_by(id=guest_id).first()\
    
    return render_template('guest_detail.html', guest=found_guest)
