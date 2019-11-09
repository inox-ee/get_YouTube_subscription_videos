#!/usr/bin/python
'''
quoteの上限に引っかかって現在機能しない
'''

import json
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCApR917DsH6BZLmQDX4idkt_L0AOP0Gvs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_today_subscription(channel_list):
    videos = {}

    for tag_name in channel_list.get("tags"):
        videos[tag_name] = []

    for channel_info in channel_list.get("items", []):
        videos_info = video_search(channel_info["channelId"])
        if not videos_info:
            continue
        for tag_name in channel_info["tags"]:
            videos[tag_name].append(dict(channelId=channel_info["title"], videos=videos_info))

    return videos


def video_search(channel_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    dt_yesterday = "{}T00:00:00Z".format(
        datetime.strftime(datetime.today() - timedelta(days=1), "%Y-%m-%d"))

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(channelId=channel_id,
                                            publishedAfter=dt_yesterday,
                                            part="snippet",
                                            maxResults=5).execute()

    print(search_response)

    search_result = []

    for searched_video in search_response.get("items", []):
        if not searched_video:
            continue
        video_info = dict(videoTitle=searched_video["snippet"]["title"],
                          videoId="https://www.youtube.com/watch?v={}".format(
                              searched_video["id"]["videoId"]))
        search_result.append(video_info)
    return search_result


if __name__ == "__main__":
    try:
        # video_search("UC_a1ZYZ8ZTXpjg9xUY9sj8w")
        with open("./test.json", mode="r") as f:
            df = json.load(f)
            today_videos = get_today_subscription(df)
            with open("./result_today.json", mode="w") as wf:
                json.dump(today_videos, wf, ensure_ascii=False)
        print("Success to collect today's Videos!!!")
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
