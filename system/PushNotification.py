
import firebase_admin
from firebase_admin import credentials, messaging
import base64


from datetime import datetime
from pytz import timezone



mst = timezone('MST')
now = datetime.now(mst)

current_time = now.strftime("%B %d, %Y : %H:%M:%S")

from firebase import firebase

firebase = firebase.FirebaseApplication("https://alertaapp-1616127995731-default-rtdb.firebaseio.com/",None)
leer = firebase.get('/token', "")
tokens = []
for x in leer.values():
    (tokens.append(x))

#tokens = ["cTryYm9aRQmygpteEZ7Hra:APA91bH8QHKvE4Nqhzzv4l4rGFVc9-5bWkdIpOMW1f7OIYq201rfSdFNjF_E22DQSsmu1Uh4MxLmwj8GFUqWYR3c1OUUeay6JJXAXQLD-H1VwABTgVetBzG-NJbOjr3MpA5PGoKDLY7G"]
print(tokens)
cred = credentials.Certificate("quickstart.json")

#cred = credentials.Certificate("/home/samuel/Descargas/nuevo/ReconocimientoFacial/system/quickstart.json")


with open("notification/image.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

n = 0

result = firebase.put('/detecciones/'+str(n), "image", str(encoded_string))




firebase_admin.initialize_app(cred)

def sendPush(title, msg, registration_token, dataObject=None):
    #See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data={"id" : str(n), "fecha" : current_time, "info" : "ALERTA, se ha detectado un intruso"},
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.

    for x in response.responses:

        print((x.message_id))
        print((x.success))

#tokens = ["eLiqu0oBQca7s9Xd2KViq8:APA91bFCj7caOEhSiim5wO3DBoGMKlPDIZlgnOjKfpZiU3thsXUOqwGUSuhY_ihP8u9_uJAFiv6xfVuf4dHgNnzWyfB7a1IXoHH12ji1-n5tQskf5XNLc590b0sGP5zPZt6RNC5H0tvq"]

sendPush("Alerta de intruso", "Se ha detectado un desconocido", tokens)
n += 1

if n == 11:
    n=0