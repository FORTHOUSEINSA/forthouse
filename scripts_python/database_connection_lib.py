def send_notif(collection, message, date):

    notification = {
        'message' : message, 
        'date' : date
    }
    collection.insert_one(notification)

def send_scheme(collection, scheme, id):

    collection.update_one(
        { "_id": id},
        { "$set": {"schema" : scheme}
        })
    