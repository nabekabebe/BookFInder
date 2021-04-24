import os

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
SECRET_KEY = "769f213c4ea89e980132232fb84a528755cd1029110f2d274dfeabd6b404896a"
DATABASE_URL = os.getenv('DATABASE_URL') if os.getenv(
    'DATABASE_URL') else "postgresql://jjjwivytsimjwi:e2bdcc0bd14397dcb667d49cebf96b9fb480f48ee8b4c16f051a52182c16effa@ec2-18-233-83-165.compute-1.amazonaws.com:5432/dc02n7i8oqjtit"
