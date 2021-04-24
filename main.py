from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

credentials = None

if os.path.exists("token.pickle"):
    print("Getting Credentials")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("refesh")
        credentials.refresh(Request())
    else:
        print("fetch")
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=["https://www.googleapis.com/auth/youtube"])
        flow.run_local_server(port=8080, prompt="consent")
        credentials = flow.credentials
        with open("token.pickle", "wb") as f:
            print("saving")
            pickle.dump(credentials, f)

def main():
    youtube = build('youtube', 'v3', credentials=credentials)
    request = youtube.subscriptions().list(part='subscriberSnippet', mySubscribers=True)
    response = request.execute()
    username = (response['items'][0]['subscriberSnippet']['title'])
    print(username)
    #print(username)
    request = youtube.videos().update(part="snippet",        body={
          "id": "NgvskquGfro",
          "snippet": {
            "title": f"This video will update to my last sub: {username}",
            "categoryId": "22",
            "description": f"{username} was my last sub"

          }
        }).execute()


main()


