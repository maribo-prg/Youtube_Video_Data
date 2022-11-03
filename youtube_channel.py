from googleapiclient.discovery import build
import csv
import api

DEVELOPER_KEY = api.API #APIキー
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

num = 50 #取得する動画の数
Channel_ID="UCL34fAoFim9oHLbVzMKFavQ"#調べたいチャンネルのID

#チャンネルのプレイリストidを返す
def get_playlist_id():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    requests = youtube.channels().list(
        part="contentDetails",#プロパティを入れる
        id=Channel_ID,
    ).execute()
    #print(requests['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
    return requests['items'][0]['contentDetails']['relatedPlaylists']['uploads']

#動画idをリストにして返す
def get_videos_id(P_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    requests = youtube.playlistItems().list(
        part='snippet',
        playlistId=P_id,
        maxResults=num
    ).execute()

    video_list=[]
    for i in range(len(requests['items'])):
        video_list.append(requests['items'][i]['snippet']['resourceId']['videoId'])

    return video_list

#動画のタイトル、日付、閲覧数、高評価数、コメント数、URL、サムネをリスト+辞書型で返す
def get_videos_status(V_lists):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    videos = []
    for i in range(len(V_lists)):
        requests = youtube.videos().list(
            part='statistics,snippet',
            id=V_lists[i]
        ).execute()

        try:
            videos.append({
                'title':requests['items'][0]['snippet']['title'],
                'day':requests['items'][0]['snippet']['publishedAt'],
                'views':requests['items'][0]['statistics']['viewCount'],
                'likes':requests['items'][0]['statistics']['likeCount'],
                'comments':requests['items'][0]['statistics']['commentCount'],
                'url':"https://www.youtube.com/watch?v="+V_lists[i],
                'img':requests['items'][0]['snippet']['thumbnails']['standard']['url']
            })
        except:
            pass
    return videos

#csv化する
def csv_output(videos):

    print([videos[0]['title'],[videos[0]['day']]])
    
    f = open('output.csv', 'w', encoding='utf_8_sig')
    writer = csv.writer(f)
    writer.writerow(['タイトル','日付','視聴回数','高評価数','コメント数','URL','サムネ'])
    for i in range(len(videos)):
        writer.writerow([
            videos[i]['title'],
            videos[i]['day'],
            videos[i]['views'],
            videos[i]['likes'],
            videos[i]['comments'],
            videos[i]['url'],
            videos[i]['img'],
        ])
    f.close()

if __name__ == "__main__":
    try:
        playlistID=get_playlist_id()
        videoId_list=get_videos_id(playlistID)
        video_inf=get_videos_status(videoId_list)
        csv_output(video_inf)
    except:
        pass
