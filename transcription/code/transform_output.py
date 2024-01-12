import json
import argparse, time, os

def transform_json(input_json, speaker_guest):
    # create ouput dir and cd into it
    
    newdir = "out/" + speaker_guest
    os.mkdir (newdir)
    os.chdir (newdir)


    outfilename = "/Users/eriksteinholz/src/lex-in-a-box/transcription/transcriptions/transformed/" + "_".join(speaker_guest.split(" ")) + ".json"
    speaker_host = "Lex Fridman"


    speaker_labels = input_json.get("results", {}).get("speaker_labels", {}).get("segments", [])
    transcripts = input_json.get("results", {}).get("transcripts", [])
    items = input_json.get("results", {}).get("items", [])

    # Create a dictionary to store the aggregated text for each speaker
    speaker_text = ""
    # Iterate through speaker segments
    last_speaker = None
    start_time = 0
    end_time = 0
    
    # outfile = open(outfilename, "w")

    for segment in speaker_labels:
        speaker = segment.get("speaker_label")
        segment_start_time = float(segment.get("start_time", 0))
        segment_end_time = float(segment.get("end_time", 0))

        # Check if the speaker has changed
        if last_speaker is not None and speaker != last_speaker:
            # Process the aggregated text for the previous speaker

            produce_file(speaker_realname, toTime(start_time), toTime(end_time), speaker_text)

            # Reset text and  start_time for the current/new speaker
            speaker_text = ""
            start_time = segment_start_time

        # Initialize text for the speaker
        # speaker_text.setdefault(speaker, "")

        # Find the corresponding transcript for the segment
        transcript = next((t.get("transcript", "") for t in transcripts), "")

        # Iterate through items to aggregate text within the time period
        for item in items:
            item_start_time = float(item.get("start_time", 0))
            item_end_time = float(item.get("end_time", 0))
            item_speaker = item.get("speaker_label", "")
            item_content = item.get("alternatives", [{}])[0].get("content", "")

            # Check if the item is within the time period of the speaker
            try:
                if segment_start_time <= item_start_time <= segment_end_time:
                    speaker_text += item_content + " "
            except:
                print("bug")
        
        if (speaker == "spk_0"):
            speaker_realname = speaker_host
        else:
            speaker_realname = speaker_guest

        last_speaker = speaker
        end_time = segment_end_time


   
    # Process the aggregated text for the last speaker
    if last_speaker is not None:
        produce_file(speaker_realname, toTime(start_time), toTime(end_time), speaker_text)
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
guest_name = " ".join(filename.split("/")[-1].split(".")[0].split("_")[2:]).title()
with open(filename) as f:
    input_json = json.load(f)

# Transform the JSON
transform_json(input_json, guest_name)
