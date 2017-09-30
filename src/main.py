#!python3

import json
from oauth2client import client
from auth import get_authenticated_service
from oauth2client.tools import argparser


OAUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

def list_channels(service):
  results = service.channels().list(
    **kwargs
  ).execute()

  print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
       (results['items'][0]['id'],
        results['items'][0]['snippet']['title'],
        results['items'][0]['statistics']['viewCount']))


def create_playlist(service, name):
    # This code creates a new, private playlist in the authorized user's channel.
    playlists_insert_response = youtube.playlists().insert(
      part="snippet,status",
      body=dict(
        snippet=dict(
          title=name,
          description="",
        ),
        status=dict(
          privacyStatus="public"
        )
      )
    ).execute()


def search_keywords(service, list_of_words):
    q = ' '.join(list_of_words)
    results = service.search().list(
            q=q, maxResults=5, part="id,snippet",
            ).execute()
    print('Top 5 results?')
    for x in results.get('items', []):
        print('{} ~~~ {}'.format(
            x['snippet']['title'],
            x['snippet']['channelTitle'],
            ))


def main(args):
    # Note: we have args.path here (to extract keywords with)
    svc = get_authenticated_service(args)
    search_keywords(svc, ['atropos', 'dnb'])


if __name__ == '__main__':
    argparser.add_argument('path', help='path to sm pack')
    args = argparser.parse_args()
    main(args)
