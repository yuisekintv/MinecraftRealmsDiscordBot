import os
from os.path import join, dirname
import json
import requests
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

OPENXBL_TOKEN = os.environ.get("OPENXBL_TOKEN")
REALMS_CLUB_ID = os.environ.get("REALMS_CLUB_ID")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

headers = {
  "X-Authorization": OPENXBL_TOKEN,
  "Accept": "application/json;charset=UTF-8",
}

def getClubPresences(clubid):
  club_res = requests.get(
    "https://xbl.io/api/v2/clubs/" + clubid,
    headers=headers
  )
  club_json = club_res.json()
  realms_name = club_json["clubs"][0]["profile"]["name"]["value"]
  presences = club_json["clubs"][0]["clubPresence"]
  return presences

def getGamertag(xuid):
  path = "./tmp/xuid_" + xuid + ".txt"
  if os.path.isfile(path):
    with open(path) as f:
      s = f.read()
      return s
  else:
    person_res = requests.get(
      "https://xbl.io/api/v2/account/" + xuid,
      headers=headers
    )
    person_json = person_res.json()
    for setting in person_json["profileUsers"][0]["settings"]:
      if setting["id"] == "Gamertag":
        tag = setting["value"]
        with open(path, mode='w') as f:
          s = f.write(tag)
        return setting["value"]

def postNobody():
  res = requests.post(
    DISCORD_WEBHOOK,
    headers={
      "Content-Type": "application/json"
    },
    data=json.dumps({"content": "台東区にはだれもいません"})
  )

def postPresences(presences):
  tags = []
  for presence in presences:
    tag = getGamertag(presence)
    tags.append(tag)
  print(tags)
  res = requests.post(
    DISCORD_WEBHOOK,
    headers={
      "Content-Type": "application/json"
    },
    data=json.dumps({"content": "台東区にいる住民：\n" + "\n".join(tags)})
  )



presences = getClubPresences(REALMS_CLUB_ID)

onlinePresences = []
for presence in presences:
  if presence["lastSeenState"] == "InGame":
    onlinePresences.append(presence["xuid"])

print(onlinePresences)

if len(onlinePresences) == 0:
  postNobody()
else:
  postPresences(onlinePresences)