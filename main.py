#!/usr/bin/python
'''
version 1.0.0
> quoteの上限に引っかかって現在機能しない

version 2.0.0
> 上記問題を解消。
> ["にじさんじ", "ホロライブ", "VTuber"]のいずれかが含まれているものを対象とし、
> 1回あたり 400 quotes 程度の消費

'''

import json
from datetime import datetime, timedelta
import settings  # ./settings.py

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = settings.DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_today_subscription(channel_list, date):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    videos = {"not_search": []}

    for tag_name in channel_list.get("tags"):
        videos[tag_name] = []

    for channel_info in channel_list.get("items", []):
        if set(channel_info["tags"]).isdisjoint(set(["にじさんじ", "ホロライブ", "VTuber"])):
            videos["not_search"].append(channel_info["title"])
            continue
        videos_info = get_video_by_activity(youtube, channel_info["channelId"], date)
        if not videos_info:
            continue
        for tag_name in channel_info["tags"]:
            videos[tag_name].append(dict(title=channel_info["title"], videos=videos_info))

    return videos


def get_video_by_activity(youtube, channel_id, date):
    activity_response = youtube.activities().list(channelId=channel_id,
                                                  publishedAfter=date,
                                                  part="snippet, contentDetails").execute()

    activity_results = []

    for _activity in activity_response.get("items", []):
        if not _activity["snippet"]["type"] == "upload":
            continue
        video_info = dict(videoTitle=_activity["snippet"]["title"],
                          videoId="https://www.youtube.com/watch?v={}".format(
                              _activity["contentDetails"]["upload"]["videoId"]))
        activity_results.append(video_info)

    return activity_results


if __name__ == "__main__":
    try:
        with open("./resource/subscription.json", mode="r") as f:
            df = json.load(f)
        dt_yesterday = "{}T00:00:00Z".format(
            datetime.strftime(datetime.today() - timedelta(days=1), "%Y-%m-%d"))
        today_videos = get_today_subscription(df, dt_yesterday)
        output_name = "./db/since_{}.json".format(dt_yesterday)
        with open(output_name, mode="w") as wf:
            json.dump(today_videos, wf, ensure_ascii=False)
        print("Success to collect today's Videos!!! -> {}".format(output_name))
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
