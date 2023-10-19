import datetime
import json
import os
import uuid

import requests
from authlib.jose import jwt

BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth"

exp = int((datetime.datetime.now() + datetime.timedelta(minutes=4)).timestamp())

# https://fhir.epic.com/Documentation?docId=oauth2&section=Creating-JWTs
jwt_header = {"alg": "RS384", "typ": "JWT"}
payload = {
    "iss": "7d3d5e8a-6dd5-45a3-8ad6-74fb876a52cd", # non-production ID, see screnshort below
    "sub": "7d3d5e8a-6dd5-45a3-8ad6-74fb876a52cd", # non-production ID, see screnshort below
    "aud": f"{BASE_URL}/oauth2/token",
    "jti": str(uuid.uuid4()), # should be uniq for every token request within the exp 
    "exp": exp,
}

with open("privatekey.pem") as f: # path to generated private .pem file
    private_key = f.read()

encoded_token = jwt.encode(jwt_header, payload, private_key)
# https://fhir.epic.com/Documentation?docId=oauth2&section=Backend-Oauth2_Access-Token-Request
data = {
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": encoded_token
}
headers = requests.structures.CaseInsensitiveDict(
    [("Content-Type", "application/x-www-form-urlencoded")]
)
response = requests.post(
    f"{BASE_URL}/oauth2/token",
    headers=headers,
    data=data,
)
print(response.json())