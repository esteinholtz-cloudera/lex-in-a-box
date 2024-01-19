import json
import argparse, time, os
import settings

def transform_json(input_json, speaker_guest):
    # create ouput dir and cd into it
    
    newdir = settings.TRANSFORMED_TRANSCRIPTS + "/" + "_".join(speaker_guest.split(" "))
    os.mkdir (newdir)
    os.chdir (newdir)

    outfilename = "/Users/eriksteinholz/src/lex-in-a-box/transcription/transcriptions/transformed/" + "_".join(speaker_guest.split(" ")) + ".json"
    speaker_host = settings.SPEAKER_HOST

    speaker_labels = input_json.get("results", {}).get("speaker_labels", {}).get("segments", [])
    transcripts = input_json.get("results", {}).get("transcripts", [])
    items = input_json.get("results", {}).get("items", [])

    # Create a dictionary to store the aggregated text for each speaker
    speaker_text = ""
    # Iterate through speaker segments
    start_time = 0
    end_time = 0
    
    # outfile = open(outfilename, "w")

    # segment iterator
    segment_iter = iter(speaker_labels)

    segment = next(segment_iter)
    last_speaker = speaker = segment.get("speaker_label")
    segment_start_time = float(segment.get("start_time", 0))
    segment_end_time = float(segment.get("end_time", 0))

    # Initialize text for the speaker
    # speaker_text.setdefault(speaker, "")
    speaker_text = ""
    speaker_start_time = 0

    # Iterate through items to aggregate text within the time period
    i=0
    for item in items:
        i=i+1
        #speaker = item.get("speaker")
        

        # if the speaker has changed, produce the output
        if speaker != last_speaker:
            # Process the aggregated text for the previous speaker
            if (last_speaker == "spk_0"):
                last_speaker_realname = speaker_host
            else:
                last_speaker_realname = speaker_guest
            produce_file(last_speaker_realname, toTime(speaker_start_time), toTime(speaker_end_time), speaker_text)

            # Reset text and  start_time for the current/new speaker
            speaker_text = ""
            speaker_start_time = segment_start_time
            last_speaker = speaker
            

        item_start_time = float(item.get("start_time", segment_start_time)) # the default is for punctuations, which dont have times
        item_content = item.get("alternatives", [{}])[0].get("content", "")
        speaker_end_time_ = item.get("end_time", "")
        if speaker_end_time_ != "":
            speaker_end_time = float(speaker_end_time_)

        # Check if the item is within the time period of the speaker
        try:
            if item_start_time <= segment_end_time:
                if (item_start_time != segment_start_time) and (item_start_time != 0): #it is not a punctuation
                     speaker_text += " "
                speaker_text += item_content
            else:
                # next segment
                segment = next(segment_iter)
                segment_end_time = float(segment['end_time'])
                speaker = segment['speaker_label']
        except:
            print("bug")

   
    # Process the aggregated text for the last speaker
    if last_speaker is not None:
        if (last_speaker == "spk_0"):
            last_speaker_realname = speaker_host
        else:
            last_speaker_realname = speaker_guest
        produce_file(last_speaker_realname, toTime(speaker_start_time), toTime(speaker_end_time), speaker_text)
    # outfile.close()
    os.chdir ("../..")    
    return

def produce_file(speaker_realname, start_time, end_time, speaker_text):
            transcript = speaker_text.strip()
            output_dict = {
                "Speaker": speaker_realname,
                "Start": start_time,
                "End": end_time,
                "Text": transcript
            }
            # Print or process the output as needed
            filename = str(start_time)+"-"+str(end_time) + ".txt"
            with open(filename, "w") as outfile:
                outfile.write(json.dumps(output_dict, indent=2))


def toTime(intime):
    return time.strftime('%H:%M:%S',time.gmtime(intime))
    # convert to timestamp within the day
    intime=float(intime)
    s = int(intime % 60)
    mtot = (intime - s) // 60
    m = int(mtot % 60)
    h = int((mtot - m) // 60)
    return str(h)+":"+str(m)+":"+str(s)

# Example input JSON

# Instantiate the parser
parser = argparse.ArgumentParser(description='input JSON to be transformed')
parser.add_argument('pos_arg', type=str,
                    help='A required integer positional argument')
# parse args
args = parser.parse_args()
print(args)
filename = args.pos_arg

#hardcoded for test
#filename = "/Users/eriksteinholz/src/lex-in-a-box/transcription/transcriptions/mit_ai_ian_goodfellow.json"

# get the guest name from the file name
guest_name_pre = filename.split("/")[-1].split(".")[0].split("_")[2:]
if guest_name_pre[-1] in "ABCDE": # it is a multipart transcription - remove
     guest_name_pre.pop(-1)
if guest_name_pre[-1] in "123456789": # it is a repeat guest - remove
    guest_name_pre.pop(-1)


guest_name = " ".join(guest_name_pre).title()
with open(filename) as f:
    input_json = json.load(f)

# Transform the JSON
transform_json(input_json, guest_name)
