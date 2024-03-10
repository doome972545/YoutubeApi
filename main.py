import googleapiclient.discovery

# Replace 'YOUR_API_KEY' with the API key you obtained from the Google Cloud Console
API_KEY = 'AIzaSyCmDsfy1HwihKhqF4AR60RTS3dEAM3qV3o'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search_youtube(query):
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=1
    )

    response = request.execute()

    if 'items' in response:
        video_id = response['items'][0]['id']['videoId']
        return get_video_details(video_id)
    else:
        return None

def get_video_details(video_id):
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    )

    response = request.execute()

    if 'items' in response:
        video = response['items'][0]
        snippet = video['snippet']
        details = {
            'title': snippet['title'],
            'description': snippet['description'],
            'views': video['statistics']['viewCount'],
            'likes': video['statistics']['likeCount'],
            # 'dislikes': video['statistics']['dislikeCount'],
            'comments': video['statistics']['commentCount'],
            'thumbnail': snippet['thumbnails']['medium']['url'],
            'video_url': f'https://www.youtube.com/watch?v={video_id}',
            'channel_name': snippet['channelTitle'],
            'channel_thumbnail': snippet['thumbnails']['medium']['url'],  # Channel thumbnail
        }
        return details
    else:
        return None

if __name__ == '__main__':
    search_query = 'ค้นหาวิดีโอ'  # Replace with the search query
    video_details = search_youtube(search_query)

    if video_details:
        print("Video Details:")
        for key, value in video_details.items():
            print(f"{key}: {value}")
    else:
        print("No videos found for the given search query.")
