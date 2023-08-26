from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Order, Track
from . import db
import json
from datetime import datetime
from sqlalchemy import update

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home() :
    if request.method == 'POST' :
        note = request.form.get('note')

        if len(note) < 1 :
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/orders', methods=['GET'])
@login_required
def orders() :
    return render_template("orders.html", user=current_user)


@views.route('/order/<id>', methods=['GET'])
@login_required
def orderById(id) :

    order_id = id
    # Find the order associated with ID in path
    order = Order.query.get(order_id)

    #print("Order: ", order)

    # Find the track associated with order, the ID of which is in path
    track = Track.query.filter_by(order_id=order.id).first()
    #print("Track: ", track)

    return render_template("order.html", user=current_user, order=order, track=track)


@views.route('/order', methods=['GET', 'POST'])
@login_required
def order() :

    if request.method == 'POST' :
        so_num = request.form.get('so_num')
        if len(so_num) != 5 :
            flash('SO number is invalid!', category='error')
        po_num = request.form.get('po_num')
        if len(po_num) != 5 :
            flash('PO number is invalid!', category='error')
        else :
            new_order = Order(
                user_id=current_user.id,
                so_num=so_num,
                po_num=po_num
            )

            db.session.add(new_order)
            db.session.commit()
            db.session.refresh(new_order)

            print("CREATED NEW ORDER!", new_order)
            flash('Order created!', category='success')

            new_track = Track(
                user_id=new_order.user_id,
                order_id = new_order.id,
                received = False,
                tested = False,
                shipped = False,
                location = "receiving"
            )
            db.session.add(new_track)
            db.session.commit()
            db.session.refresh(new_track)
            print("CREATED NEW ORDER TRACK!", new_track)
            flash('New track created!', category='success')

    return render_template("order_form.html", user=current_user)


@views.route('/delete-order', methods=['POST'])
def delete_order():
    order = json.loads(request.data)
    orderId = order['orderId']
    order = Order.query.get(orderId)
    if order:
        if order.user_id == current_user.id:
            db.session.delete(order)
            db.session.commit()

    trackId = orderId
    track = Track.query.get(trackId)
    if track:
        if track.user_id == current_user.id:
            db.session.delete(track)
            db.session.commit()
            
    return jsonify({})


@views.route('/tracks', methods=['GET'])
@login_required
def tracks() :
    return render_template("tracks.html", user=current_user)


@views.route('/track', methods=['GET', 'POST'])
@login_required
def track() :

    if request.method == 'POST' :
        new_track = Track(
            user_id=new_order.user_id,
            order_id = new_order.id,
            received = bool(False),
            tested = bool(False),
            shipped = bool(False),
            location = "receiving"
        )
        db.session.add(new_track)
        db.session.commit()
        db.session.refresh(new_track)
        print("CREATED NEW TRACK!", new_track)
        flash('New track created!', category='success')

    return render_template("track_form.html", user=current_user)


@views.route('/track/<id>', methods=['GET', 'POST'])
@login_required
def TrackById(id) :

    track_id = id
    track = Track.query.get(track_id)
    order = Order.query.get(track.order_id)

    track.received = bool(track.received)
    track.tested = bool(track.tested)
    track.shipped = bool(track.shipped)
    
    if request.method == 'POST' :

        track = Track.query.get(track_id)
        print("existing track", track)

        #print("track.received: ", track.received)
        #print("track.tested: ", track.tested)
        ##print("track.shipped: ", track.shipped)
        #print("track.location: ", track.location)

        #print("update track received: ", bool(request.form.get('received')))
        #print("update track tested: ", bool(request.form.get('tested')))
        #print("update track shipped: ", bool(request.form.get('shipped')))
        #print("update track location: ", str(request.form.get('location')))

        track.received = bool(request.form.get('received'))
        track.tested = bool(request.form.get('tested'))
        track.shipped = bool(request.form.get('shipped'))
        track.location = request.form.get('location')
        track.last_update = datetime.now()

        db.session.commit()
        db.session.refresh(track)

        print("UPDATED EXISTING TRACK RECORD!", track)
        flash('Updated track success!', category='success')

    return render_template("track.html", user=current_user, order=order, track=track)


@views.route('/delete-track', methods=['POST'])
def delete_track():
    track = json.loads(request.data)
    trackId = track['trackId']
    track = Track.query.get(trackId)
    if track:
        if track.user_id == current_user.id:
            db.session.delete(track)
            db.session.commit()

    return jsonify({})

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
