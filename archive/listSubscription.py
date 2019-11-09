#!/usr/bin/python

# This code sample shows how to add a channel subscription.
# The default channel-id is for the GoogleDevelopers YouTube channel.
# Sample usage:
# python add_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import argparse
import os
import re

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
DEVELOPER_KEY = 'AIzaSyCApR917DsH6BZLmQDX4idkt_L0AOP0Gvs'
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials, developerKey=DEVELOPER_KEY)


# This method calls the API's youtube.subscriptions.insert method to add a
# subscription to the specified channel.
def get_subscription_list(youtube, results, channel_id, **kwargs):
    if not kwargs:
        list_subscription_response = youtube.subscriptions().list(
            part="snippet",
            channelId=channel_id,
            maxResults=25,
        ).execute()
    else:
        list_subscription_response = youtube.subscriptions().list(
            part="snippet",
            channelId=channel_id,
            maxResults=25,
            pageToken=kwargs["pageToken"],
        ).execute()

    for item in list_subscription_response.get("items", []):
        results.append("({}) {}".format(item["snippet"]["resourceId"]["channelId"],
                                        item["snippet"]["title"]))

    nextPageToken = list_subscription_response.get("nextPageToken")
    if nextPageToken is not None:
        get_subscription_list(youtube, results, channel_id, pageToken=nextPageToken)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--channel-id',
                        help='ID of the channel to subscribe to.',
                        default='UCA6e3ASawwX8sXUV7FCAZhQ')
    args = parser.parse_args()

    youtube = get_authenticated_service()
    try:
        list_subscription = []
        get_subscription_list(youtube, list_subscription, args.channel_id)
        print("Channels:\n", "\n".join(list_subscription), "\n")

    except HttpError as e:
        print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
