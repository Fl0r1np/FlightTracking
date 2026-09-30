import os
from dotenv import load_dotenv

if __name__ == '__main__':

    # Load the environments
    load_dotenv()

    # Load OpenSky API Credentials
    opensky_username = os.getenv("OPENSKY_USERNAME")
    opensky_password = os.getenv("OPENSKY_PASSWORD")

    print(f"OpenSky Credentials: {opensky_username}:{opensky_password}")