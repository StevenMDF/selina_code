"""find a singer's first album"""
import sys
from json.decoder import JSONDecodeError

import requests
from requests.exceptions import HTTPError

ITUNES_API_ENDPOINT = 'https://itunes.apple.com/search'


def command_first_album():
    """enter search keywords and then print the results"""
    if not len(sys.argv) == 2:
        print(f'usage: python {sys.argv[0]} {{SEARCH_TERM}}')
        sys.exit(1)

    term = sys.argv[1]
    resp = requests.get(
        ITUNES_API_ENDPOINT,
        {
            'term': term,
            'media': 'music',
            'entity': 'album',
            'attribute': 'artistTerm',
            'limit': 200,
        },
    )
    try:
        resp.raise_for_status()
    except HTTPError as e:
        print(f'Error: failed to call iTunes API, {e}')
        sys.exit(2)
    try:
        albums = resp.json()['results']
    except JSONDecodeError:
        print(f'Error: response is not valid JSON format')
        sys.exit(2)
    if not albums:
        print(f'Error: no albums found for artist "{term}"')
        sys.exit(1)

    sorted_albums = sorted(albums, key=lambda item: item['releaseDate'])
    first_album = sorted_albums[0]
    # only keep date (such as 17th Feb 2023 11:23, we only keep '17th Feb 2023')
    release_date = first_album['releaseDate'].split('T')[0]

    # print result
    print(f"{term}'s first album: ")
    print(f"  * Name: {first_album['collectionName']}")
    print(f"  * Genre: {first_album['primaryGenreName']}")
    print(f"  * Released at: {release_date}")


if __name__ == '__main__':
  # you don't need to add or change code here
    command_first_album()
