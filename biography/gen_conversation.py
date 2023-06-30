import json
import openai
import random
from tqdm import tqdm

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


def filter_people(person):
    people = person.split("(")[0]
    return people


def construct_message(agents, idx, person, final=False):
    prefix_string = "Here are some bullet point biographies of {} given by other agents: ".format(person)

    if len(agents) == 0:
        return {"role": "user", "content": "Closely examine your biography and provide an updated bullet point biography."}


    for i, agent in enumerate(agents):
        agent_response = agent[idx]["content"]
        response = "\n\n Agent response: ```{}```".format(agent_response)

        prefix_string = prefix_string + response

    if final:
        prefix_string = prefix_string + "\n\n Closely examine your biography and the biography of other agents and provide an updated bullet point biography.".format(person, person)
    else:
        prefix_string = prefix_string + "\n\n Using these other biographies of {} as additional advice, what is your updated bullet point biography of the computer scientist {}?".format(person, person)

    return {"role": "user", "content": prefix_string}


def construct_assistant_message(completion):
    content = completion["choices"][0]["message"]["content"]
    return {"role": "assistant", "content": content}


if __name__ == "__main__":
    with open("article.json", "r") as f:
        data = json.load(f)

    people = sorted(data.keys())
    people = [filter_people(person) for person in people]
    random.seed(1)
    random.shuffle(people)

    agents = 3
    rounds = 2

    generated_description = {}


    for person in tqdm(people[:40]):
        agent_contexts = [[{"role": "user", "content": "Give a bullet point biography of {} highlighting their contributions and achievements as a computer scientist, with each fact separated with a new line character. ".format(person)}] for agent in range(agents)]

        for round in range(rounds):
            for i, agent_context in enumerate(agent_contexts):

                if round != 0:
                    agent_contexts_other = agent_contexts[:i] + agent_contexts[i+1:]

                    if round == (rounds - 1):
                        message = construct_message(agent_contexts_other, 2*round - 1, person=person, final=True)
                    else:
                        message = construct_message(agent_contexts_other, 2*round - 1, person=person, final=False)
                    agent_context.append(message)

                try:
                    completion = openai.ChatCompletion.create(
                              model="gpt-3.5-turbo-0301",
                              messages=agent_context,
                              n=1)
                except:
                    completion = openai.ChatCompletion.create(
                              model="gpt-3.5-turbo-0301",
                              messages=agent_context,
                              n=1)

                print(completion)
                assistant_message = construct_assistant_message(completion)
                agent_context.append(assistant_message)

            bullets = parse_bullets(completion["choices"][0]['message']['content'])

            # The LM just doesn't know this person so no need to create debates
            if len(bullets) == 1:
                break

        generated_description[person] = agent_contexts

    json.dump(generated_description, open("biography_{}_{}.json".format(agents, rounds), "w"))

