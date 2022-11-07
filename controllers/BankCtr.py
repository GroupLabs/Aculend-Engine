import requests
import json
from models.BankModel import Bank
import os

def get_users(db):

    res = []

    for bank in db["banks"].find():

        # request data from inverite
        req_id = bank['request_guid']
        sta = requests.get(
            f'https://sandbox.inverite.com/api/v2/fetch/{req_id}',
            headers={
            "content-type": "application/json",
            'Auth': f"{os.getenv('INVERITE_AUTH')}",
            }
        )

        # switch to json
        sta = sta.json()

        # catch failed connection
        try:
            sta['status']
        except KeyError:
            print(sta['error'])
            raise ConnectionRefusedError("Failed to connect with Inverite")

        # if verified
        if(sta['status'] == "Verified"):

            # get risk score from Inverite
            risk_score = requests.post(
                'https://sandbox.inverite.com/api/v2/risk',
                data={"request" : sta["request"]},
                headers={
                    "content-type": "application/json",
                    'Auth': f"{os.getenv('INVERITE_AUTH')}"
                }
            )

            # switch to json
            risk_score = risk_score.json()

            # catch failed connection
            try:
                risk_score['bin_score']
            except KeyError:
                
                # assign score in case it doesn't exist
                risk_score['bin_score'] = 0

        # build item
        item = {
            "name" : sta["name"],
            "status" : "true",
            "email" : sta["contacts"][0]['contact'],
            "phone" : sta["contacts"][1]['contact'],
            "bankname" : bank["bankname"],
            "score" : risk_score['bin_score']
        }

        # append to response
        res.append(item)

    print(res)

    return json.dumps(res)

def get_banklist(db):
    banklist = requests.get(
        'https://sandbox.inverite.com/api/v2/bank/list_available',
        headers={
            "Accept": "application/json",
            "Content-type": "application/json",
            "Auth": f"{os.getenv('INVERITE_AUTH')}"
        }
    )

    # switch to json
    banklist = banklist.json()

    return json.dumps(banklist["banks"])

def create(data, db):
    body = {
        "ip": data['ip'],
        "email": data['email'],
        "firstname": data['firstName'],
        "lastname": data['lastName'],
        "username": f"{data['firstName']} {data['lastName']}",
        "referenceid": data['refID'],        
        "bankID": data['bank'],
        "phone": data['phonenumber'],
        "siteID": "317",
    }

    resItem = requests.post(
        'https://sandbox.inverite.com/api/v2/create',
        json=body,
        headers={
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Auth" : f"{os.getenv('INVERITE_AUTH')}"
        }
    )

    # switch to json
    resItem = resItem.json()

    # assimilate to Bank class
    bank = Bank(
        firstname=data["firstName"],
        lastname=data["lastName"],
        password=resItem["password"],
        birthday=data["birthday"],
        gender=data["gender"],
        marrial=data["marrial"],
        ip=data["ip"],
        phone=data["phonenumber"],
        email=data["email"],
        bank=data["bank"],
        bankname=data["bankname"],
        site=data["site"],
        year_lived=data["yearslived"],
        month_lived=data["monthlived"],
        income=data["income"],
        otherincome=data["otherincome"],
        refID=data["refID"],
        request_guid=resItem["request_guid"],
        iframeurl=resItem["iframeurl"],
        reused=resItem['reused']
    )

    # upload to banks collection
    db["banks"].insert_one(bank.get_dict())
