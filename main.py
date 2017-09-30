import os
import sys
from oauth2client import client
from oauth2client.tools import argparser

from auth import get_authenticated_service


OAUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
VIDEO = 'youtube#video'


class TrackInfo(object):
    def __init__(self, name, extra_shit=None):
        self.name = name
        self.extra_shit = extra_shit


def construct_playlist_url(playlist_id, video_id):
    # please don't punk me- video id must be in the playlist, ofc.
    youtube_url = 'https://www.youtube.com/watch'
    return '{}?v={}&list={}'.format(youtube_url, video_id, playlist_id)


def get_packname(full_path):
    # this is shitty
    path_elements = full_path.split('/')
    packname = path_elements[-1] if path_elements[-1] else path_elements[-2]
    return packname
    

def create_description(full_path, track_info_list):
    # return a string that's like, long and has the proper info for all the tracks,
    packname = get_packname(full_path)
    track_data_fmted = [
            '{} - {}'.format(t.extra_shit[1], t.extra_shit[0])
            for t in track_info_list
            ]
    desc = '\n'.join([
        "Auto-gen'd playlist for ITG pack: {}".format(packname),
        "if there are mistakes, this has the proper track listing at least.",
        ] + track_data_fmted)
    return desc


def create_playlist(service, name, desc=""):
    # This code creates a new playlist in the user's channel.
    # #thanksgoogle
    playlists_insert_response = service.playlists().insert(
      part="snippet,status",
      body=dict(
        snippet=dict(
          title=name,
          description=desc
        ),
        status=dict(
          privacyStatus="public"
        )
      )
    ).execute()
    return playlists_insert_response


def add_item_to_playlist(service, playlistId, videoId):
    request_data = {
            'snippet': {
                'playlistId': playlistId,
                'resourceId': {
                    'kind': VIDEO,
                    'videoId': videoId,
                    },
                }
            }
    response = service.playlistItems().insert(
            body=request_data,
            part='snippet',
            ).execute()
    return response


def search_keywords(service, track):
    q = ' '.join(track.extra_shit)
    results = service.search().list(
            q=q, maxResults=1, part="id,snippet",
            ).execute()
    results = results.get('items', [])
    
    vid_results = [x for x in results if x['id']['kind'] == VIDEO]
    if vid_results:
        return vid_results[0]
        print('{} ~~~ {} ~~ {}'.format(
            x['snippet']['title'],
            x['snippet']['channelTitle'],
            track.extra_shit,
            # x['snippet']['thumbnails']['url'],
            ))
    return None


def get_val(sm_config_line):
    # a config line looks like '#NAME: value'
    value = sm_config_line.split(':')[-1].strip()
    # well, assuming that it doesn't contain any semi colons
    value = value.split(';')[0]
    return value


def parse_title_artist(sm_path):
    artist = ''
    title = ''
    with open(sm_path, 'r') as s:
        # honestly if it's not in th;e first 20 lines what are they doing
        for line in s:
            if artist != '' and title != '':
                break
            if '#ARTIST:' in line:
                artist = get_val(line)
            elif '#TITLE:' in line:
                title = get_val(line)
    return title, artist


def get_track_titles(path):
    pack_contents = os.listdir(path)
    shit = []
    for p in pack_contents:
        if not os.path.isdir(path + '/' + p):
            continue

        sm = list(filter(lambda s: s.endswith('.sm'), os.listdir(path + '/' + p)))
        if not sm:
            print('No sm found for track: {}'.format(p), file=sys.stderr)
        else:
            # babe, what if there's mroe than one sm??? huh???
            # babe, what if it's an ssc and not an sm?? huh???
            sm = sm[0]
            # Parse sm here and get info
            title, artist = parse_title_artist('/'.join([path, p, sm]))
            shit.append(TrackInfo(p, extra_shit=(title, artist)))
    return shit


def main():
    argparser.add_argument('path', help='path to sm pack')
    argparser.add_argument('--playlist_id', help='existing playlist id to add to')
    args = argparser.parse_args()

    # Note: we have args.path here (to extract keywords with)
    track_info = get_track_titles(args.path)
    name = get_packname(args.path)
    playlist_desc = create_description(args.path, track_info)

    svc = get_authenticated_service(args)
    vid_results = [search_keywords(svc, track) for track in track_info]

    playlist_response = create_playlist(svc, name, desc=playlist_desc)
    playlist_id = args.playlist_id if args.playlist_id else playlist_response['id']

    for vid in vid_results:
        resp = add_item_to_playlist(svc, playlist_id, vid['id']['videoId'])

    first_vid_id = vid_results[0]['id']['videoId']
    print(construct_playlist_url(playlist_id, first_vid_id))


if __name__ == '__main__':
    main()
