import os

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
SECRET_KEY = "769f213c4ea89e980132232fb84a528755cd1029110f2d274dfeabd6b404896a"
DATABASE_URL = os.getenv('DATABASE_URL') if os.getenv(
    'DATABASE_URL') else "postgresql://postgres:niko1122@localhost/BookAPI"
