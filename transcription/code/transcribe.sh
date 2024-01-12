jobname=$1
echo starting $jobname
aws start-transcription-job
--transcription-job-name $jobname
--language-code en-US
--media 

--output-bucket-name <value>
--no-identify-language

[--cli-input-json <value>]
