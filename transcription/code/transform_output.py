import json
import argparse

def transform_json(input_json, speaker_guest):
    outfilename = "/Users/eriksteinholz/src/lex-in-a-box/transcription/transcriptions/transformed/" + "_".join(speaker_guest.split(" ")) + ".json"
    speaker_host = "Lex Fridman"


    speaker_labels = input_json.get("results", {}).get("speaker_labels", {}).get("segments", [])
    transcripts = input_json.get("results", {}).get("transcripts", [])
    items = input_json.get("results", {}).get("items", [])

    # Create a dictionary to store the aggregated text for each speaker
    speaker_text = {}
    # Iterate through speaker segments
    last_speaker = None
    start_time = 0
    end_time = 0
    
    outfile = open(outfilename, "w")

    for segment in speaker_labels:
        speaker = segment.get("speaker_label")
        segment_start_time = float(segment.get("start_time", 0))
        segment_end_time = float(segment.get("end_time", 0))

        if (speaker == "spk_0"):
            speaker_realname = speaker_host
        else:
            speaker_realname = speaker_guest


        # Check if the speaker has changed
        if last_speaker is not None and speaker != last_speaker:
            # Process the aggregated text for the previous speaker
            transcript = speaker_text[last_speaker].strip()
            output_dict = {
                "Speaker": speaker_realname,
                "Start": toTime(start_time),
                "End": toTime(end_time),
                "Text": transcript
            }
            # Print or process the output as needed
            outfile.write(json.dumps(output_dict, indent=2))

            # Reset text and update start_time for the current speaker
            speaker_text[speaker] = ""
            start_time = segment_start_time

        # Initialize text for the speaker
        speaker_text.setdefault(speaker, "")

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
                    speaker_text[item_speaker] += item_content + " "
            except:
                print("bug")

        last_speaker = speaker
        end_time = segment_end_time

   
    # Process the aggregated text for the last speaker
    if last_speaker is not None:
        transcript = speaker_text[last_speaker].strip()
        output_dict = {
            "Speaker": speaker_realname,
            "Start": toTime(start_time),
            "End": toTime(end_time),
            "Text": transcript
        }
        # Print or process the output as needed
        outfile.write(json.dumps(output_dict, indent=2))  

    outfile.close()
    return

def toTime(intime):
    # convert to timestamp within the day
    intime=float(intime)
    s = int(intime % 60)
    mtot = (intime - s) // 60
    m = int(mtot % 60)
    h = int((mtot - m) // 60)
    return str(h)+":"+str(m)+":"+str(s)

# Example input JSON

# Ask for additional command line arguments if needed (for VSCode)
parser = argparse.ArgumentParser()
parser.add_argument('--interactive', action='store_true', default=False)
(args, rest) = parser.parse_known_args()
if args.interactive:
  try: readline.read_history_file()
  except: pass
  rest += input("Arguments: ").split(" ")  # Get input args
  try: readline.write_history_file()
  except: pass

  # Your other script arguments go here
  parser.add_argument("-output-dir", default="/out")
  # ...
  # Instantiate the parser
  parser = argparse.ArgumentParser(description='input JSON to be transformed')
  parser.add_argument('pos_arg', type=str,
                    help='A required integer positional argument')
# parse args
  args = parser.parse_args(rest)
  print(args)



#filename = args.pos_arg
filename = "/Users/eriksteinholz/src/lex-in-a-box/transcription/transcriptions/mit_ai_christof_koch.json"
guest_name = " ".join(filename.split("/")[-1].split(".")[0].split("_")[2:]).title()
with open(filename) as f:
    input_json = json.load(f)

# Transform the JSON
transform_json(input_json, guest_name)
