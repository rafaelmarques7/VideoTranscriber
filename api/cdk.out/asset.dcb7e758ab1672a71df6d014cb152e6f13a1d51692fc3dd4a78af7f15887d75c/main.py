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
    re_matching_group = "[\[].*?[\]]" # matches all btw square brackets, f.e. "[text]"
    captions_str = re.sub(re_matching_group, "", captions_str)
    # remove leading whitespace
    captions_str = captions_str.lstrip()
    return captions_str

def handler(event, context):
    yt_link = "https://www.youtube.com/watch?v=T-cbdnP0Hyc"

    yt_object = YouTube(yt_link)
    captions_xml = yt_object.caption_tracks[0].xml_captions
    captions_str = captions_transform_xml_to_str(captions_xml)
    captions_str = captions_clean_text(captions_str)

    # Try to add some punctuation to captions_str
    res = requests.post("http://bark.phon.ioc.ee/punctuator", {"text": captions_str})
    captions_with_punctuation = res.text

    return {
        'statusCode': 200,
        'body': captions_with_punctuation
    }
