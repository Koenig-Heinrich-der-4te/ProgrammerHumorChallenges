import requests
import re 
import json
from urllib.parse import unquote
import os

# actually using regex this time simplified everyting
json_capture = re.compile("ytInitialPlayerResponse = (.+?);</script>") # captures the json containing all required data
playerjs_capture = re.compile('"jsUrl":"(.+?)"') # captures the player.js url used to decipher signatures of some media urls
playerjs_id_capture = re.compile("\/player\/(.+?)\/") # gets the player id used to cache the data

decipher_steps_capture = re.compile('=function\(a\){a=a.split\(""\);(.+?);return a.join\(""\)};')
extract_step = re.compile(".+?\.(.+?)\(a,(\d+)\)") # func name + number

step_reverse_capture = re.compile("([\w\d]+?):function\(a\)")
step_splice_capture = re.compile("([\w\d]+?):function\(a,b\){a")
step_swap_capture = re.compile("([\w\d]+?):function\(a,b\){var")

signature_cipher_extract = re.compile("s=(.+?)&sp=(.+?)&url=(.+)")

mime_type_extract = re.compile("(.+?)\/(.+?); codecs=\"(.+)\"")



def load_json(url):
    content = requests.get(url).text

    res = json_capture.search(content)
    json_content = json.loads(res[1])

    player_url = playerjs_capture.search(content)[1]
    player_url = f"https://www.youtube.com{player_url}"
    return json_content, player_url


def fuck_json(obj, *fuck_path):
    for f in fuck_path:
        obj = obj[f]
    return obj

def extract_details(data):
    details = data["videoDetails"]
    return {
        "title": details["title"],
        "length": int(details["lengthSeconds"]),
        "thumbnail": fuck_json(details, "thumbnail", "thumbnails", -1, "url"),
        "description": details["shortDescription"]
    }

# returns lists of video and audio extracted from the data (uses player_url if signatureCipher instead of url is supplied)
def extract_sources(data, player_url):
    audio = []
    video = []

    adaptive_formats = data["streamingData"]["adaptiveFormats"]
    formats = data["streamingData"]["formats"] + adaptive_formats
    for format in formats:
        media = parse_media(format, player_url)
        if media["format_type"] == "video":
            video.append(media)
        else:
            audio.append(media)
    return video, audio


def parse_media(format, player_url):
    url = format["url"] if "url" in format else decipher_url(format["signatureCipher"], player_url)
    mime_extract = mime_type_extract.match(format["mimeType"])
    media_class, media_type, codecs = mime_extract[1], mime_extract[2], mime_extract[3]
    has_audio = "audioQuality" in format
    if media_class == "video":
        order = format["width"]
        name = f"{format['qualityLabel']} ({format['width']}x{format['height']}), {format['fps']} fps, {media_type} ({codecs})" + ("" if has_audio else " (no audio)")
    else:
        order = format["averageBitrate"]
        name = f"{format['audioSampleRate']} Hz, {format['audioQuality']}/{format['averageBitrate']}, {media_type} ({codecs})"
        
    return {
            "order": order,
            "name": name, # descriptive name containing all relevant information
            "format": media_type,
            "format_type": media_class, # video/audio
            "url": url
        }


def query_cipher_steps(player_url):
    # now I have to load this giant js player file just because youtube wants to prevent me from using the video outside of the official website
    print("downloading player...")
    garbage = requests.get(player_url).text
    steps = decipher_steps_capture.search(garbage)[1]
    steps = steps.split(";")
    step_provider_name = re.search("(.+?)\.", steps[0])[1]
    step_provider = re.search(f"var {step_provider_name}={{(.+?)}};", garbage, re.DOTALL)[1]
    # find the names of the functions used to decipher the signature
    step_types = {
        step_splice_capture.search(step_provider)[1]: "splice", # cut off the first n characters
        step_reverse_capture.search(step_provider)[1]: "reverse", # reverse the string
        step_swap_capture.search(step_provider)[1]: "swap", # swap first and nth character
    }

    # parse the steps needed to decipher the signature
    decipher_steps = []
    for step in steps:
        match = extract_step.match(step)
        step_type = step_types[match[1]]
        num = int(match[2])
        decipher_steps.append([step_type, num])

    return decipher_steps

cipher_cache = {}

def get_cipher_steps(player_url):
    player_id = playerjs_id_capture.search(player_url)[1]
    if player_id in cipher_cache:
        return cipher_cache[player_id]
    print("Url requires deciphering! Fuck youtube")
    if not os.path.exists(f".ytcache/{player_id}.json"): # load and cache steps 
        os.makedirs(".ytcache", exist_ok=True)
        steps = query_cipher_steps(player_url)
        # cache steps so I don't have to download the player.js everytime (speed go brr)
        with open(f".ytcache/{player_id}.json", "w") as file:
            json.dump(steps, file)
    else: # load cached steps
        with open(f".ytcache/{player_id}.json") as file:
            steps = json.load(file)
    cipher_cache[player_id] = steps
    return steps

# Youtube doesn't want us to be able to use certain videos
# but I will do it anyways because I can
# The protection isn't strong so getting around it is possible in acceptable time
def decipher_url(sig_cipher, player_url):
    sig_cipher = unquote(sig_cipher)
    extract = signature_cipher_extract.match(sig_cipher)
    cipher = list(extract[1])
    sp = extract[2]
    base_url = extract[3]

    decipher_steps = get_cipher_steps(player_url)

    for step, num in decipher_steps:
        if step == "swap": # swap first and nth character
            cipher[0], cipher[num % len(cipher)] = cipher[num % len(cipher)], cipher[0]
        elif step == "reverse": # reverse the string
            cipher.reverse()
        elif step == "splice": # cut off the first n characters
            cipher = cipher[num:]
            
    deciphered = "".join(cipher)

    return f"{base_url}&{sp}={deciphered}"

if __name__ == "__main__":
    # for testing or if you just want the urls
    data, jsurl = load_json(input("> "))

    video, audio = extract_sources(data, jsurl)

    with open("test.json", "w") as file:
        json.dump({
            "video": video,
            "audio": audio
        }, file)
