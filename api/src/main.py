import re
import requests
from pytube import YouTube
from xml.etree import cElementTree as ET
from html import unescape


def captions_transform_xml_to_str(captions_xml):
    xml_root = ET.fromstring(captions_xml)
    captions_str = ""
    for child in xml_root.findall('text'):
        captions_str = captions_str + " " + child.text
    return captions_str


def captions_clean_text(captions_str):
    # transform any HTML characters into text
    captions_str = unescape(captions_str)
    # remove caption metadata between square brackets
    # matches anything btw square brackets, f.e. "[text]"
    re_matching_group = "[\\[].*?[\\]]"
    # replacing matching group with empty string
    captions_str = re.sub(re_matching_group, "", captions_str)
    # remove leading whitespace
    captions_str = captions_str.lstrip()
    return captions_str


def validate_youtube_url(youtube_url):
    if not isinstance(youtube_url, str):
        return False
    re_mg = re.compile("(?:https?://)?(?:www[.])?(?:youtube[.]com|youtu[.]be)")
    return re_mg.match(youtube_url)


def handler(event, context):
    youtube_url = event.get("queryStringParameters").get("youtube_url")
    is_valid = validate_youtube_url(youtube_url)
    if (not is_valid):
        raise Exception(f'the youtube_url provided ({youtube_url}) is invalid')

    yt_link = "https://www.youtube.com/watch?v=T-cbdnP0Hyc"

    print(f"creating Youtube object for link: {yt_link}")
    yt_object = YouTube(yt_link)

    captions_xml = yt_object.caption_tracks[0].xml_captions
    captions_str = captions_transform_xml_to_str(captions_xml)
    captions_str = captions_clean_text(captions_str)

    # Try to add some punctuation to captions_str
    res = requests.post("http://bark.phon.ioc.ee/punctuator",
                        {"text": captions_str})
    captions_with_punctuation = res.text

    return {
        'statusCode': 200,
        'body': captions_with_punctuation
    }
