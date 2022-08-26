from datetime import date
from distutils.log import error
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from sqlalchemy.orm.attributes import flag_modified
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Hours, Note, Schedule
from flask_mail import Mail, Message
from . import db
import json

views = Blueprint('views', __name__)

#home route, initializes available hours
@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): #note
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    hhh = Hours.query.all() #run a query to see if data already exists
    if len(hhh) >= 1:
        print("already data")
    else: #otherwise prepopulate available horus in the database
        sethours = Hours(hourss = "09:00 AM")
        db.session.add(sethours)
        sethours = Hours(hourss = "10:00 AM")
        db.session.add(sethours)
        sethours = Hours(hourss = "11:00 AM")
        db.session.add(sethours)
        sethours = Hours(hourss = "12:00 PM")
        db.session.add(sethours)
        sethours = Hours(hourss = "01:00 PM")
        db.session.add(sethours)
        sethours = Hours(hourss = "02:00 PM")
        db.session.add(sethours)
        sethours = Hours(hourss = "03:00 PM")
        db.session.add(sethours)
        sethours = Hours(hourss = "04:00 PM")
        db.session.add(sethours)
        db.session.commit()
    return render_template("home.html", user=current_user)


#Route to show and push new bookings to the database
#also do validation, if a schedule already exists
#or if a time slot is already booked, prompt user the 
#time is not available
@views.route('/schedule', methods=['POST', 'GET'])
def schedule():
    if request.method == "POST":
        date1 = request.form['startdatetime']
        eqp = request.form['userName']
        hours = request.form['comp_select']
        hourExists = db.session.query(db.exists().where(Schedule.hours == hours)).scalar()
        dateExists = db.session.query(db.exists().where(Schedule.startTime == date1)).scalar()
        nameExists = db.session.query(db.exists().where(Schedule.name == eqp)).scalar()
        if date1 == "": #validations to check  if date empty
            flash("Please Select a valid date!", category='error')
        elif hourExists and dateExists: #if booking already exists check:
            flash("Sorry time not available! Pick another time", category='error')
        elif nameExists: #if booking name already exists check:
            flash("Sorry you already have a booking!", category='error')
        elif eqp == "": #if name is empty prompt:
            flash("Please enter a valid first and last name!", category='error')
        elif hours == "Select Hour": #if hours not selected prompt:
            flash("Please select valid hours!", category='error')
        else: #if all previous checks are validated, then go ahead and commit to database:
            postit = Schedule(startTime=date1, name=eqp, hours=hours)
            db.session.add(postit)
            db.session.commit()
            flash('Booking made!', category='success')
    hourlist = Hours.query.all()
    return render_template("schedule.html",hourlist=hourlist, user=current_user)

#shows all existing bookings/schedules
@views.route('/schedule-list')
def schedule_list():
    sList = Schedule.query.all()
    return render_template("schedule_list.html", tasks=sList, user=current_user)

#calendar view
@views.route('/calendar')
def calendar():
    result_dict = [u.__dict__ for u in Schedule.query.all()]
    return render_template("calendar.html", result_dict = result_dict ,user=current_user)

#deleting a schedule
@views.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):#run a query get the specific record
    taskToDelete = Schedule.query.get_or_404(id)
    try: #a try catch statement, then delete record/booking
        db.session.delete(taskToDelete)
        db.session.commit()
        sList = Schedule.query.all()
        return render_template("schedule_list.html",tasks=sList, user=current_user)
    except:
        flash("errorrr")

#updating a schedule
@views.route('/updateSched/<int:id>', methods=['POST', 'GET'])
def updateSched(id):#run a query to get the specific record to update
    taskToUpdate = Schedule.query.get_or_404(id)
    hourlist = Hours.query.all()
    if request.method == 'POST': #get new updated values and commit to db
        taskToUpdate.startTime = request.form['startdatetime']
        taskToUpdate.name = request.form['userName']
        taskToUpdate.hours = request.form['comp_select']
        hourExists = db.session.query(db.exists().where(Schedule.hours == request.form['comp_select'])).scalar()
        dateExists = db.session.query(db.exists().where(Schedule.startTime == request.form['startdatetime'])).scalar()
        try:
            db.session.flush()
            db.session.commit()
            sList = Schedule.query.all()
            return render_template("schedule_list.html",tasks=sList,lists=hourlist, user=current_user)
        except:
            flash("error")
    else:
        return render_template("updateSched.html",tasks=taskToUpdate, user=current_user)
#----
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})