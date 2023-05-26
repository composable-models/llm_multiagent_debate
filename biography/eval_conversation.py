import json
import openai
import numpy as np
import time

def parse_bullets(sentence):
    bullets_preprocess = sentence.split("\n")
    bullets = []

    for bullet in bullets_preprocess:
        try:
            idx = bullet.find(next(filter(str.isalpha, bullet)))
        except:
            continue

        bullet = bullet[idx:]

        if len(bullet) != 0:
            bullets.append(bullet)

    return bullets


def parse_yes_no(string):
    """
    Parses a string containing "yes" or "no" and returns a boolean value.

    Args:
        string (str): The string to parse.

    Returns:
        bool: True if the string contains "yes", False if the string contains "no".

    Raises:
        ValueError: If the input string does not contain "yes" or "no".
    """

    if "uncertain" in string.lower():
        return None
    elif "yes" in string.lower():
        return True
    elif "no" in string.lower():
        return False
    else:
        return None

def filter_people(person):
    people = person.split("(")[0]
    return people

if __name__ == "__main__":
    response = json.load(open("biography_1_2.json", "r"))

    with open("article.json", "r") as f:
        gt_data = json.load(f)

    gt_data_filter = {}

    for k, v in gt_data.items():
        k = filter_people(k)
        gt_data_filter[k] = v

    gt_data = gt_data_filter

    people = list(response.keys())

    accuracies = []

    for person in people:

        if person not in gt_data:
            continue

        gt_description = gt_data[person]
        gt_bullets = parse_bullets(gt_description)
        bio_descriptions = response[person]# [2][-1]['content']

        for description in bio_descriptions:

            bio_description = description[-1]['content']

            bio_bullets = parse_bullets(bio_description)
            if len(bio_bullets) == 1:
                if len(bio_bullets[0]) < 400:
                    continue

            bio_bullets = " ".join(bio_bullets)
            # continue

            for bullet in gt_bullets:
                message = [{"role": "user", "content": "Consider the following biography of {}: \n {} \n\n Is the above biography above consistent with the fact below? \n\n {} \n Give a single word answer, yes, no, or uncertain. Carefully check the precise dates and locations between the fact and the above biography.".format(person, bio_bullets, bullet)}]

                try:
                    completion = openai.ChatCompletion.create(
                              model="gpt-3.5-turbo-0301",
                              messages=message,
                              n=1)
                except Exception as e:
                    print("sleeping")
                    time.sleep(20)
                    continue

                print(message)

                content = completion["choices"][0]["message"]["content"]
                print(content)
                accurate = parse_yes_no(content)

                if accurate is not None:
                    accuracies.append(float(accurate))

            print("accuracies:", np.mean(accuracies), np.std(accuracies) / (len(accuracies) ** 0.5))

