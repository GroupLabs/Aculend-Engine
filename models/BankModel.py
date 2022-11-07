import datetime
import json

class Bank:
    def __init__(self, firstname, lastname, password, birthday, 
    gender, marrial, ip, phone, email, bank, bankname, site,
    year_lived, month_lived, income, otherincome, refID, request_guid,
    iframeurl, reused, date=datetime.datetime.utcnow(), status=False):
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.birthday = birthday
        self.gender = gender
        self.marrial = marrial
        self.ip = ip
        self.phone = phone
        self.email = email
        self.bank = bank
        self.bankname = bankname
        self.site = site
        self.year_lived = year_lived
        self.month_lived = month_lived
        self.income = income
        self.otherincome = otherincome
        self.refID = refID
        self.request_guid = request_guid
        self.iframeurl = iframeurl
        self.reused = reused
        self.status = status
        self.date = date
    
    def get_dict(self):
        if self.status:
          status_ = "true"
        else:
          status_ = "false"

        bank_dict = {
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "password" : self.password,
            "birthday": self.birthday,
            "gender": self.gender,
            "marrial": self.marrial,
            "ip": self.ip,
            "phone": self.phone,
            "email": self.email,
            "bank": self.bank,
            "bankname": self.bankname,
            "site": self.site,
            "year_lived": self.year_lived,
            "month_lived": self.month_lived,
            "income": self.income,
            "otherincome": self.otherincome,
            "refID": self.refID,
            "request_guid": self.request_guid,
            "iframeurl": self.iframeurl,
            "reused": self.reused,
            "status": status_,
            "date" : self.date
        }

        return bank_dict
    
    def get_json(self):
        return json.dump(self.get_dict(), indent=4)