import os
from os.path import join, dirname
import time
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
  xuid_path = "./tmp/xuid_" + xuid + ".txt"
  if os.path.isfile(xuid_path):
    with open(xuid_path) as f:
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
        with open(xuid_path, mode="w") as f:
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

def postOnlineUsers(xuids):
  tags = []
  for xuid in xuids:
    tag = getGamertag(xuid)
    tags.append(tag)
  print(tags)
  res = requests.post(
    DISCORD_WEBHOOK,
    headers={
      "Content-Type": "application/json"
    },
    data=json.dumps({"content": "台東区にいる住民：\n" + "\n".join(tags)})
  )

def postLaunchBot():
  requests.post(
    DISCORD_WEBHOOK,
    headers={
      "Content-Type": "application/json"
    },
    data=json.dumps({"content": "広報たいとうが起動しました"})
  )

def postJoinedXuid(xuid):
  tag = getGamertag(xuid)
  print(tag + ' joined')
  requests.post(
    DISCORD_WEBHOOK,
    headers={
      "Content-Type": "application/json"
    },
    data=json.dumps({"content": tag + "が台東区に帰ってきました"})
  )

def postLeavedXuid(xuid):
  tag = getGamertag(xuid)
  print(tag + ' leaved')
  requests.post(
    DISCORD_WEBHOOK,
    headers={
      "Content-Type": "application/json"
    },
    data=json.dumps({"content": tag + "が台東区から旅立ちました"})
  )

xuids = {}

launched = True

postLaunchBot()
while True:
  print()
  print(xuids)
  try:
    clubXuids = getClubPresences(REALMS_CLUB_ID)
    for presence in clubXuids:
      print(presence)
      state = presence["lastSeenState"]
      xuid = presence["xuid"]
      if launched and state == "InGame":
        postJoinedXuid(xuid)
      if xuid in xuids:
        before_state = xuids[xuid]
        if before_state != state:
          if state == "InGame":
            postJoinedXuid(xuid)
          elif state == "NotInClub":
            postLeavedXuid(xuid)
        xuids[xuid] = state
      else:
        xuids[xuid] = state
  except:
    import traceback
    traceback.print_exc()
  time.sleep(10)
  launched = False
