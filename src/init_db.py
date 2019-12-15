import random, re, csv, os
from json.decoder import JSONDecodeError
from typing import Optional

import requests

from app.database import Base, engine, Session
from app.crud.shop import create as create_shop
from app.crud.hospital import create as create_hospital
from app.crud.user import create as create_user, read_by_email
from app.crud.drug import create as create_drug, read_by_name
from app.schemas.hospital import HospitalCreate
from app.schemas.shop import ShopCreate
from app.schemas.user import UserCreate
from app.schemas.drug import DrugCreate
from app.models.user import User
from app.models.hospital import Hospital
from app.models.shop import Shop
from app.models.drug import Drug
from app.models.prescription import PrescribedDrug, Prescription
from app.models.reservation import HospReservation, ShopReservation


def request_url(url: str, serviceKey: str, page: int) -> Optional[dict]:
    queryParams = {
        "ServiceKey": serviceKey,
        "pageNo": page,
        "numOfRows": 100,
        "_type": "json",
    }
    r = requests.get(url, params=queryParams)
    json: dict = {}
    try:
        json = r.json()
    except JSONDecodeError:
        print("Error: response content is not JSON")
        print(r.text)
    finally:
        return json


def add_hospital(item: dict):
    # 좌표정보가 없을 시 DB에 추가하지 않고 넘어감
    if not ("wgs84Lon" in item) or not ("wgs84Lat" in item):
        print("Warning: current data has no longitude/latitude")
        return

    # 전화번호 양식이 잘못되었을 경우 추가하지 않고 넘어감
    tel = (
        str(item["dutyTel1"]).replace("(", "").replace(")", "").replace("-", "").strip()
    )
    if re.fullmatch("^(0\d{1,2})?-?\d{3,4}-?\d{4}$", tel) is None:
        print(
            "Warning: current data has incorrect form of tel: " + str(item["dutyTel1"])
        )
        return

    hospital = HospitalCreate(
        name=item["dutyName"],
        addr=item["dutyAddr"],
        tel=tel,
        lon=float(item["wgs84Lon"]),
        lat=float(item["wgs84Lat"]),
        strCnd=random.randint(1, 10),
        course_bitmask=random.randint(1, 2 ** 29 - 1),
    )

    if "dutyTime1s" in item:
        timestr = str(item["dutyTime1s"])
        hospital.dutyTime1s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime1c" in item:
        timestr = str(item["dutyTime1c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime1c = "23:59"
        else:
            hospital.dutyTime1c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime2s" in item:
        timestr = str(item["dutyTime2s"])
        hospital.dutyTime2s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime2c" in item:
        timestr = str(item["dutyTime2c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime2c = "23:59"
        else:
            hospital.dutyTime2c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime3s" in item:
        timestr = str(item["dutyTime3s"])
        hospital.dutyTime3s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime3c" in item:
        timestr = str(item["dutyTime3c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime3c = "23:59"
        else:
            hospital.dutyTime3c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime4s" in item:
        timestr = str(item["dutyTime4s"])
        hospital.dutyTime4s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime4c" in item:
        timestr = str(item["dutyTime4c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime4c = "23:59"
        else:
            hospital.dutyTime4c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime5s" in item:
        timestr = str(item["dutyTime5s"])
        hospital.dutyTime5s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime5c" in item:
        timestr = str(item["dutyTime5c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime5c = "23:59"
        else:
            hospital.dutyTime5c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime6s" in item:
        timestr = str(item["dutyTime6s"])
        hospital.dutyTime6s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime6c" in item:
        timestr = str(item["dutyTime6c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime6c = "23:59"
        else:
            hospital.dutyTime6c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime7s" in item:
        timestr = str(item["dutyTime7s"])
        hospital.dutyTime7s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime7c" in item:
        timestr = str(item["dutyTime7c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime7c = "23:59"
        else:
            hospital.dutyTime7c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime8s" in item:
        timestr = str(item["dutyTime8s"])
        hospital.dutyTime8s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime8c" in item:
        timestr = str(item["dutyTime8c"])
        if int(timestr[0:2]) >= 24:
            hospital.dutyTime8c = "23:59"
        else:
            hospital.dutyTime8c = timestr[0:2] + ":" + timestr[2:4]

    db = Session()
    try:
        create_hospital(db=db, hospital_in=hospital)
    except:
        db.rollback()
        raise
    finally:
        db.close()


def add_shop(item: dict):
    # 좌표정보가 없을 시 DB에 추가하지 않고 넘어감
    if not ("wgs84Lon" in item) or not ("wgs84Lat" in item):
        print("Warning: current data has no longitude/latitude")
        return

    # 전화번호 양식이 잘못되었을 경우 추가하지 않고 넘어감
    tel = (
        str(item["dutyTel1"]).replace("(", "").replace(")", "").replace("-", "").strip()
    )
    if re.fullmatch("^(0\d{1,2})?-?\d{3,4}-?\d{4}$", tel) is None:
        print(
            "Warning: current data has incorrect form of tel: " + str(item["dutyTel1"])
        )
        return

    shop = ShopCreate(
        name=item["dutyName"],
        addr=item["dutyAddr"],
        tel=tel,
        lon=float(item["wgs84Lon"]),
        lat=float(item["wgs84Lat"]),
    )

    if "dutyTime1s" in item:
        timestr = str(item["dutyTime1s"])
        shop.dutyTime1s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime1c" in item:
        timestr = str(item["dutyTime1c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime1c = "23:59"
        else:
            shop.dutyTime1c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime2s" in item:
        timestr = str(item["dutyTime2s"])
        shop.dutyTime2s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime2c" in item:
        timestr = str(item["dutyTime2c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime2c = "23:59"
        else:
            shop.dutyTime2c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime3s" in item:
        timestr = str(item["dutyTime3s"])
        shop.dutyTime3s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime3c" in item:
        timestr = str(item["dutyTime3c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime3c = "23:59"
        else:
            shop.dutyTime3c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime4s" in item:
        timestr = str(item["dutyTime4s"])
        shop.dutyTime4s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime4c" in item:
        timestr = str(item["dutyTime4c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime4c = "23:59"
        else:
            shop.dutyTime4c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime5s" in item:
        timestr = str(item["dutyTime5s"])
        shop.dutyTime5s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime5c" in item:
        timestr = str(item["dutyTime5c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime5c = "23:59"
        else:
            shop.dutyTime5c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime6s" in item:
        timestr = str(item["dutyTime6s"])
        shop.dutyTime6s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime6c" in item:
        timestr = str(item["dutyTime6c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime6c = "23:59"
        else:
            shop.dutyTime6c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime7s" in item:
        timestr = str(item["dutyTime7s"])
        shop.dutyTime7s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime7c" in item:
        timestr = str(item["dutyTime7c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime7c = "23:59"
        else:
            shop.dutyTime7c = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime8s" in item:
        timestr = str(item["dutyTime8s"])
        shop.dutyTime8s = timestr[0:2] + ":" + timestr[2:4]
    if "dutyTime8c" in item:
        timestr = str(item["dutyTime8c"])
        if int(timestr[0:2]) >= 24:
            shop.dutyTime8c = "23:59"
        else:
            shop.dutyTime8c = timestr[0:2] + ":" + timestr[2:4]

    db = Session()
    try:
        create_shop(db=db, shop_in=shop)
    except:
        db.rollback()
        raise
    finally:
        db.close()


def add_user(item: dict):
    user = UserCreate(
        name=item["name"],
        tel=item["phone"],
        email=item["local"] + "@" + item["domain"],
        password=item["passwd"],
        lon=item["lng"],
        lat=item["lat"],
    )
    db = Session()
    try:
        if read_by_email(db, email=user.email) is not None:
            print(
                f"Warning: the email of this user is already registered: {user.email}"
            )
            return
        create_user(db, user=user)
    except:
        db.rollback()
        raise
    finally:
        db.close()


def add_drug(item: dict):
    drug = DrugCreate(name=item["name"], unit=item["unit"])
    db = Session()
    try:
        if read_by_name(db, name=drug.name) is not None:
            print(f"Warning: the name of this drug is already registered: {drug.name}")
            return
        create_drug(db, drug=drug)
    except:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    serviceKey: str = os.environ["SERVICE_KEY"]
    Base.metadata.create_all(bind=engine)

    # Adding hospitals from API
    print("============================")
    print("Adding initial hospital data")
    print("============================")
    url = (
        "http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncFullDown"
    )
    totPage = 700
    curPage = 1
    while curPage <= totPage:
        js = request_url(url, serviceKey, curPage)
        if js is not {}:
            if curPage is 1:
                totPage = int(js["response"]["body"]["totalCount"] / 100)
                print(
                    "Total hospitals in API: ",
                    int(js["response"]["body"]["totalCount"]),
                )
            for item in js["response"]["body"]["items"]["item"]:
                add_hospital(item)
        if curPage % 20 is 0:
            print(f"{curPage} pages processed ({curPage} / {totPage})")
        curPage += 1
    print("Hospitals added")
    print("")

    # Adding stores from API
    print("============================")
    print("Adding initial shop data")
    print("============================")
    url = (
        " http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown"
    )
    totPage = 200
    curPage = 1
    while curPage <= totPage:
        js = request_url(url, serviceKey, curPage)
        if js is not {}:
            if curPage is 1:
                totPage = int(js["response"]["body"]["totalCount"] / 100)
                print(
                    "Total shops in API: ", int(js["response"]["body"]["totalCount"]),
                )
            for item in js["response"]["body"]["items"]["item"]:
                add_shop(item)
            totPage = int(js["response"]["body"]["totalCount"] / 100)
        if curPage % 20 is 0:
            print(f"{curPage} pages processed ({curPage} / {totPage})")
        curPage += 1
        curPage += 1
    print("Shops added")
    print("")

    # Adding users from customers.csv
    print("============================")
    print("Adding initial user data")
    print("============================")
    with open("customers.csv", mode="r", newline="", encoding="UTF-8") as r:
        reader = csv.DictReader(r)
        idx: int = 1
        for item in reader:
            add_user(item)
            if idx % 500 is 0:
                print(f"{idx} lines processed")
            idx += 1
    print("Users added")
    print("")

    # Adding drugs from drugs.csv
    print("============================")
    print("Adding initial drug data")
    print("============================")
    with open("drugs.csv", mode="r", newline="", encoding="UTF-8") as r:
        reader = csv.DictReader(r)
        idx: int = 1
        for item in reader:
            add_drug(item)
            if idx % 500 is 0:
                print(f"{idx} lines processed")
            idx += 1
    print("Drugs added")
    print("")


if __name__ == "__main__":
    print("Initialize DB")
    Base.metadata.create_all(bind=engine)
    init_db()
    print("Initializing finished")
