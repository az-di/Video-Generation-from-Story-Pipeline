from meta_prompt import meta_prompt
import json
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from collections import defaultdict
from generate_subtitle import chapter

load_dotenv()



my_endpoint = os.getenv("OPENAI_ENDPOINT")

def get_GPT4O_client(endpoint):

    subscription_key = os.getenv("OPENAI_KEY")
    api_version = os.getenv("API_VERSION")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )
    
    return client


subtitle_input_file = "subtitle_" + chapter + ".json"
subtitle_output_file = "subtitle_ch_" + chapter + ".json" # temp file created in create_timestamp_json()
output_file = "scenes_ch_" + chapter + ".json" # output file for generated scenes



def create_timestamp_json(): # simplifies the subtitle JSON to only include time and text
    with open(subtitle_input_file, "r") as f:
        data = json.load(f)
    output = []
    for item in data:
        duration = round(item["end"] - item["start"], 2)  # round to 2 decimal places
        output.append({
            "time": str(duration),
            "text": item["text"]
        })
    with open(subtitle_output_file, "w") as f:
        json.dump(output, f, indent=2)




def generate_image_prompts():

    with open(subtitle_output_file, "r", encoding="utf-8") as f:
        subtitle_lines = json.load(f)

    bible_text_for_prompt = json.dumps(subtitle_lines, ensure_ascii=False, indent=2)
    prompt_filled = meta_prompt.replace("{{ $json.attributes.fullText }}", bible_text_for_prompt)
    prompt_filled = prompt_filled.replace("{{ $('Manual Trigger').item.json.scenecount }}", "30") 

    client = get_GPT4O_client(my_endpoint)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot assistant that converts biblical chapters into image prompts."},
            {"role": "user", "content": prompt_filled}
        ]
    )
    
    return response.choices[0].message.content



if __name__ == "__main__":
    
    create_timestamp_json()
    
    generated_prompts_json = generate_image_prompts()
    
    scenes = json.loads(generated_prompts_json)

    # Load timestamp data to get actual durations per line
    with open(subtitle_output_file, "r") as f:
        timestamp_data = json.load(f)
    
    line_to_duration = {item["text"]: float(item["time"]) for item in timestamp_data}

    grouped_scenes = defaultdict(list)
    for scene in scenes:
        grouped_scenes[scene["bible_lines"]].append(scene)

    # Adjust scene lengths proportionally
    for line_text, group in grouped_scenes.items():

        original_total = sum(float(scene["scene_length"]) for scene in group)

        actual_duration = line_to_duration.get(line_text)
        if actual_duration is None:
            print(f"Warning: No duration found for line: {line_text}")
            continue

        proportional_lengths = []
        for scene in group:
            prop = float(scene["scene_length"]) / original_total
            proportional_lengths.append(round(prop * actual_duration, 2))

        drift = round(actual_duration - sum(proportional_lengths), 2)
        if drift != 0 and proportional_lengths:
            proportional_lengths[-1] = round(proportional_lengths[-1] + drift, 2)

        for scene, new_length in zip(group, proportional_lengths):
            scene["scene_length"] = new_length


    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scenes, f, indent=2, ensure_ascii=False)
        print("saved to ", output_file)


    
    
    

    
    
