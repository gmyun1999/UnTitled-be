# firebase_config.py
import os

import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    # Path to your service account key file
    key_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "letter-79136-firebase-adminsdk-zoh6n-d3f60bc7f4.json",
    )

    # Initialize credentials
    cred = credentials.Certificate(key_path)
    # Initialize the Firebase Admin SDK
    firebase_admin.initialize_app(cred)

    print("Firebase Admin SDK has been initialized.")
    print()
