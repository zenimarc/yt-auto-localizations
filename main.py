from googletrans import Translator
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import re

def translate(title, desc):
    translator = Translator()
    destinations = ['af', 'az', 'id', 'ms', 'bs', 'ca', 'cs', 'da', 'de', 'et', 'en-IN', 'en-GB', 'en', 'es', 'es-419',
                    'es-US', 'eu', 'fil', 'fr', 'fr-CA', 'gl', 'hr', 'zu', 'is', 'it', 'sw', 'lv', 'lt', 'hu', 'nl', 'no',
                    'uz', 'pl', 'pt-PT', 'pt', 'ro', 'sq', 'sk', 'sl', 'sr-Latn', 'fi', 'sv', 'vi', 'tr', 'be', 'bg', 'ky',
                    'kk', 'mk', 'mn', 'ru', 'sr', 'uk', 'el', 'hy', 'iw', 'ur', 'ar', 'fa', 'ne', 'mr', 'hi', 'as', 'bn',
                    'pa', 'gu', 'or', 'ta', 'te', 'kn', 'ml', 'si', 'th', 'lo', 'my', 'ka', 'am', 'km', 'zh-CN', 'zh-TW', 'zh-HK', 'ja', 'ko']

    trans_obj = {}
    for dest in destinations:
        try:
            title_trans = translator.translate(title, dest=dest).text
            desc_trans = translator.translate(desc, dest=dest).text
            print(title_trans, desc_trans)
            trans_obj.update({dest: {'title': title_trans, 'description': desc_trans}})
        except Exception as e:
            print(e)
            continue
    return  trans_obj

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube_run_update(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    #first we get the current video snippet (title, desc, tags...)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    title = (response['items'][0]['snippet']['title'])
    desc = (response['items'][0]['snippet']['description'])
    tags = (response['items'][0]['snippet']['tags'])
    category = (response['items'][0]['snippet']['categoryId'])

    trans_obj = translate(title, desc)


    request = youtube.videos().update(
        part="snippet,localizations",
        body={
            "id": video_id,
            "localizations": trans_obj,
            "snippet": {
                "categoryId": category,
                "defaultLanguage": "en",
                "description": desc,
                "tags": tags,
                "title": title
          }
        }
    )
    response = request.execute()

    print(response)

def youtube_get_snippet(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":

    print("paste here a link of the youtube video you want to translate in different languages")
    link = input()
    pattern = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    video_id = re.search(pattern, link).group(0)

    youtube_run_update(video_id)


