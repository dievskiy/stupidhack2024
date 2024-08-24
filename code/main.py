import time
import streamlit as st
import openai
import json
import function as f
import requests as rq
from streamlit_chat import message
from dotenv import dotenv_values
import random

from openai import OpenAI

env = dotenv_values()

client = OpenAI(api_key=env['OPENAI_API_KEY'])


if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []


class IntentsList:
    def __init__(self):
        """
        The api of Gaud Open Platform is used here.

        https://lbs.amap.com/api/webservice/guide/api/weatherinfo
        """
        self.weather_api_url = "https://restapi.amap.com/v3/weather/weatherInfo"
        # self.amap_api_key = env['AMAP_API_KEY']

    # def query_city_weather(self, city):
    #     """
    #     Query the weather temperature of the city.
    #
    #     Args:
    #         city (str): Cities that should be queried.
    #     """
    #     params = {
    #         "key": self.amap_api_key,
    #         "city": city,
    #         "output": "json",
    #         "extensions": "all",
    #     }
    #
    #     response = rq.get(self.weather_api_url, params=params)
    #
    #     response.raise_for_status()
    #
    #     weather_data = response.json()
    #
    #     return json.dumps(weather_data)

        # for item in weather_data['forecasts']:
        #     st.markdown(f"{item['province'] + item['city']} is as follows：")
        #     for cast in item['casts']:
        #         st.markdown(
        #             f"**{cast['date']}**  ：`dayweather`：{cast['dayweather']}, `nightweather`：{cast['nightweather']}, `daytemp`: {cast['daytemp']}, `nighttemp`：{cast['nighttemp']}")

    @staticmethod
    def send_email(to_email, title, body):
        # st.markdown(f"Recipient：{to_email}")
        # st.markdown(f"Email Title：{title}")
        # st.markdown(f"Email Body：{body}")

        return "Mail Sent，Recipient：{to_email}, Email Title: {title}, Email body: {body}"

    @staticmethod
    def get_coding_question(language):
        print(f"[FUNCTION] get_coding_question")

        questions = {
            "Python": [
                "Write a function to check if a number is prime",
                "Create a program that generates a random password",
                "Implement a binary search algorithm",
                "Write a script to find the most frequent word in a text file",
                "Create a simple calculator using a class",
                "Implement a basic stack data structure",
                "Write a function to reverse a string without using built-in reverse functions",
                "Create a program that simulates a dice roll",
                "Implement the bubble sort algorithm",
                "Write a script to remove duplicates from a list"],
            "JavaScript": [
                "Write a function to flatten a nested array",
                "Implement a basic counter using closures",
                "Create a function that checks if a string is a palindrome",
                "Write a program to find the factorial of a number using recursion",
                "Implement a simple to-do list using DOM manipulation",
                "Create a function to calculate the Fibonacci sequence",
                "Write a program to validate an email address using regex",
                "Implement a basic debounce function",
                "Create a function to deep clone an object",
                "Write a program to calculate the sum of all numbers in an array"
            ],
            "Java": [
                "Implement a basic LinkedList class",
                "Write a program to find the second largest element in an array",
                "Create a simple bank account class with deposit and withdraw methods",
                "Implement a binary tree data structure",
                "Write a program to check if two strings are anagrams",
                "Create a method to reverse the order of words in a sentence",
                "Implement a basic queue data structure",
                "Write a program to find all prime factors of a number",
                "Create a simple file reader that counts the number of words in a file",
                "Implement the merge sort algorithm"
            ],
            "C++": [
                "Write a program to find the GCD of two numbers",
                "Implement a basic template class for a stack",
                "Create a program that simulates a basic ATM machine",
                "Write a function to remove all vowels from a string",
                "Implement a simple vector class",
                "Create a program to find the longest common subsequence of two strings",
                "Write a function to check if a number is a perfect square",
                "Implement a basic circular queue",
                "Create a program to find the intersection of two arrays",
                "Write a function to convert a decimal number to binary"
            ],
            "Ruby": [
                "Write a program to check if a year is a leap year",
                "Implement a basic hash table",
                "Create a program that generates the first n prime numbers",
                "Write a function to find the missing number in an array of 1 to n",
                "Implement a simple text-based tic-tac-toe game",
                "Create a program to find all permutations of a string",
                "Write a function to calculate the area of different shapes using modules",
                "Implement a basic binary search tree",
                "Create a program to find the longest palindromic substring",
                "Write a function to check if parentheses in a string are balanced"
            ],
            "C#": [
                "Implement a basic generic List class",
                "Write a program to find the longest word in a sentence",
                "Create a simple stopwatch class",
                "Implement a basic event and delegate example",
                "Write a program to check if a string contains only digits",
                "Create a function to find the mode of an array",
                "Implement a simple LINQ query to filter and sort a list",
                "Write a program to reverse the order of words in a sentence",
                "Create a basic exception handling example",
                "Implement a simple producer-consumer pattern using threads"
            ],
            "Go": [
                "Write a function to check if a number is a perfect number",
                "Implement a basic concurrent web crawler",
                "Create a program to find all substrings of a string",
                "Write a function to calculate the dot product of two vectors",
                "Implement a simple key-value store using a map",
                "Create a program to find the longest increasing subsequence",
                "Write a function to check if a binary tree is balanced",
                "Implement a basic rate limiter",
                "Create a program to solve the N-Queens problem",
                "Write a function to perform matrix multiplication"
            ],
            "TypeScript": [
                "Implement a generic stack class",
                "Write a program to find the kth largest element in an array",
                "Create a simple state management system using interfaces",
                "Implement a basic decorator pattern",
                "Write a function to deep compare two objects",
                "Create a program to implement a basic promise chain",
                "Implement a simple pub-sub pattern",
                "Write a program to find the longest common prefix of an array of strings",
                "Create a function to implement currying",
                "Implement a basic memoization helper function"
            ],
            "Swift": [
                "Write a function to check if a number is a narcissistic number",
                "Implement a basic protocol-oriented programming example",
                "Create a program to find all anagrams in a list of words",
                "Write a function to implement the Fisher-Yates shuffle algorithm",
                "Implement a simple keychain wrapper",
                "Create a program to solve the Tower of Hanoi problem",
                "Write a function to perform binary addition on two strings",
                "Implement a basic observable pattern",
                "Create a program to find the median of two sorted arrays",
                "Write a function to implement a basic LRU cache"
            ],
            "Kotlin": [
                "Implement a basic coroutine example",
                "Write a program to find the longest palindromic subsequence",
                "Create a simple data class and use it with collections",
                "Implement a basic sealed class hierarchy",
                "Write a function to calculate the power set of a set",
                "Create a program to implement a basic state machine",
                "Implement a simple extension function",
                "Write a program to find the maximum sum subarray",
                "Create a function to implement the Knuth-Morris-Pratt algorithm",
                "Implement a basic higher-order function example"
            ]
            }

        if language not in questions:
            return random.choice(questions["Python"])
            # return random.choice(questions)

        return random.choice(questions[language])
        # return random.choice(questions)

    @staticmethod
    def get_recipe_question():
        print(f"[FUNCTION] get_recipe_question")
        prompts_food_ing = [
            "I have rice, tomatoes, and eggs at home. What is something tasty I can cook?",
            "I have a fish (salmon), herbs, garlic, and potatoes with me. What is something I can cook?",
            "I have bread, cheese, and avocado. What can I make for breakfast?",
            "I have chicken, bell peppers, and onions. What can I whip up for dinner?",
            "I have pasta, olive oil, and parmesan. What simple dish can I prepare?",
            "I have canned beans, rice, and salsa. What can I make with these?",
            "I have ground beef, tomatoes, and lettuce. What’s a quick meal idea?",
            "I have eggs, flour, and sugar. What can I bake that’s easy and quick?",
            "I have yogurt, berries, and honey. What can I make for dessert?",
            "I have tofu, soy sauce, and broccoli. What’s a healthy meal I can prepare?",
            "I have potatoes, bacon, and sour cream. What can I make for lunch?",
            "I have shrimp, garlic, and lemon. What’s a simple dish I can cook?",
            "I have spinach, feta, and phyllo dough. What’s a Mediterranean dish I can prepare?",
            "I have oats, milk, and bananas. What can I make for breakfast?",
            "I have rice, soy sauce, and chicken. What Asian-inspired dish can I cook?",
            "I have tortillas, cheese, and ground beef. What’s a quick Mexican dish I can prepare?",
            "I have mushrooms, garlic, and cream. What’s a comforting meal I can make?",
            "I have apples, cinnamon, and sugar. What can I bake with these?",
            "I have chickpeas, tahini, and lemon. What’s a healthy snack I can prepare?",
            "I have pasta, tomatoes, and basil. What Italian dish can I make?",
            "I have lentils, carrots, and onions. What’s a hearty dish I can prepare?",
            "I have eggs, cheese, and spinach. What’s a quick breakfast idea?",
            "I have bread, peanut butter, and jelly. What’s a fun twist on a classic sandwich?",
            "I have potatoes, cheese, and chives. What can I make for a snack?",
            "I have quinoa, avocado, and lime. What’s a healthy bowl I can prepare?",
            "I have rice, coconut milk, and curry powder. What’s a flavorful dish I can make?",
            "I have zucchini, tomatoes, and parmesan. What’s a light meal I can prepare?",
            "I have beans, tomatoes, and ground beef. What can I make for dinner?",
            "I have chicken, barbecue sauce, and rolls. What’s a quick dinner idea?",
            "I have rice, black beans, and salsa. What’s a simple meal I can prepare?",
            "I have fish, lemon, and dill. What’s a fresh dish I can cook?",
            "I have bacon, eggs, and bread. What can I make for brunch?",
            "I have noodles, soy sauce, and veggies. What’s a quick stir-fry I can prepare?",
            "I have rice, tuna, and avocado. What’s a fun sushi-inspired dish I can make?",
            "I have chicken, cream, and pasta. What’s a comforting dish I can cook?",
            "I have spinach, ricotta, and pasta. What’s a cheesy meal I can make?",
            "I have rice, eggs, and soy sauce. What’s a quick fried rice recipe I can cook?",
            "I have sausage, potatoes, and onions. What’s a hearty meal I can prepare?",
            "I have flour, water, and yeast. What can I bake from scratch?",
            "I have milk, eggs, and vanilla. What dessert can I prepare?",
            "I have peanut butter, chocolate chips, and oats. What’s a no-bake snack I can make?",
            "I have ground turkey, tomatoes, and rice. What can I cook for dinner?",
            "I have chicken, garlic, and ginger. What’s a flavorful dish I can prepare?",
            "I have rice, green beans, and chicken. What’s a balanced meal I can make?",
            "I have fish sticks, frozen peas, and potatoes. What’s a quick kid-friendly meal I can cook?",
            "I have chickpeas, garlic, and cumin. What’s a Mediterranean dish I can prepare?",
            "I have bread, eggs, and cinnamon. What’s a sweet breakfast treat I can make?",
            "I have potatoes, onions, and cheese. What’s a quick potato dish I can cook?",
            "I have lentils, spinach, and garlic. What’s a healthy and filling meal I can prepare?",
            "I have eggs, bacon, and pancake mix. What’s a full breakfast I can make?"
        ]

        return random.choice(prompts_food_ing)

    @staticmethod
    def get_philosophical_question(philosopher_name):
        print(f"[FUNCTION] get_philosophical_question")
        philosophical_prompts = [
            "What is the meaning of life, and how do you define your own purpose?",
            "Do you believe in free will, or is everything predestined?",
            "What is the nature of reality, and how can we know what is truly real?",
            "Is there such a thing as absolute truth, or is all truth subjective?",
            "What is the nature of consciousness, and where does it come from?",
            "Are humans inherently good or evil?",
            "What is the role of suffering in human life, and can it be justified?",
            "Do we have a moral obligation to help others, or should self-interest come first?",
            "What is the essence of happiness, and how can one achieve it?",
            "Can we ever truly know another person, or are we always alone in our experiences?",
            "What is the nature of time, and does it exist independently of our perception?",
            "Do you believe in the existence of a higher power, and if so, what is its nature?",
            "What is the relationship between mind and body, and can they exist independently?",
            "What does it mean to live a good life, and how should one go about it?",
            "Is it possible to achieve true objectivity, or are we always biased by our perspectives?",
            "What is the nature of beauty, and why do we find certain things beautiful?",
            "Can we ever achieve true justice, or is it an unattainable ideal?",
            "What is the nature of love, and how does it differ from other forms of attachment?",
            "Is there such a thing as fate, or do we create our own destiny?",
            "How do we determine what is morally right or wrong?",
            "What is the role of art in human life, and how does it influence our understanding of the world?",
            "Is it more important to be loved or to be respected?",
            "What is the nature of death, and is there an afterlife?",
            "How do our memories shape our identity, and can we trust them?",
            "What is the significance of dreams, and do they hold any meaning?",
            "Can we ever truly understand the concept of infinity?",
            "Is it possible to live without desire, and should we strive for that?",
            "What is the nature of power, and how does it corrupt individuals?",
            "Is knowledge more valuable than wisdom, or are they equally important?",
            "How does culture shape our beliefs and values, and can we ever escape its influence?",
            "What is the role of fear in our lives, and how can we overcome it?",
            "Can we ever truly be free, or are we always constrained by society and our circumstances?",
            "What is the significance of language in shaping our thoughts and experiences?",
            "How do we define personal identity, and can it change over time?",
            "What is the nature of evil, and can it exist without good?",
            "Is it possible to achieve true equality, or will there always be hierarchies?",
            "What is the role of education in human life, and what should its goals be?",
            "How do we reconcile the existence of suffering with the idea of a benevolent higher power?",
            "What is the nature of justice, and can it be achieved without punishment?",
            "Is it more important to seek truth or to seek happiness?",
            "How do our emotions influence our decision-making, and should they be trusted?",
            "What is the role of technology in shaping our future, and should we be concerned about it?",
            "Can we ever achieve true peace, or is conflict an inherent part of human nature?",
            "What is the nature of wisdom, and how can we cultivate it?",
            "Is it possible to live a life without regret, and should we aim for that?",
            "How do we determine the value of a human life, and is all life equally valuable?",
            "What is the significance of history, and how does it influence our present and future?",
            "Can we ever truly understand the experiences of others, or are we limited by our own perspective?",
            "What is the role of forgiveness in human relationships, and is it always necessary?",
            "How do we define success, and is it the same for everyone?",
            "What is the relationship between freedom and responsibility, and can one exist without the other?",
            "How does our perception of time influence the way we live our lives?",
            "What is the nature of truth, and can it be discovered through reason alone?",
            "Is it possible to achieve true enlightenment, and what does that look like?",
            "How do we define progress, and is it always a good thing?",
            "What is the significance of ritual and tradition in human life, and should they be preserved?",
            "Can we ever truly escape our biases, and should we try to?",
            "What is the role of intuition in decision-making, and can it be trusted?",
            "How do we determine the meaning of life in a universe that may be indifferent to our existence?",
            "What is the nature of the self, and can it exist independently of the body?",
            "Is it possible to achieve true understanding between different cultures, or will differences always persist?",
            "How do we define morality, and is it universal or culturally relative?",
            "What is the role of science in understanding the world, and are there limits to its reach?",
            "Can we ever achieve true objectivity in our judgments, or are we always influenced by our emotions?",
            "What is the significance of art in human life, and can it reveal truths that other forms of knowledge cannot?",
            "How do we determine the value of a human life, and is all life equally valuable?",
            "What is the relationship between happiness and suffering, and can one exist without the other?",
            "Is it possible to live a life without fear, and should we strive for that?",
            "How do we define justice, and is it always possible to achieve it?",
            "What is the role of religion in human life, and can it provide answers that science cannot?",
            "How do we determine what is morally right or wrong, and can we rely on our instincts to guide us?",
            "Is it possible to achieve true happiness, and what does that look like?",
            "How do our beliefs about the afterlife influence the way we live our lives?",
            "What is the role of suffering in human life, and can it be a source of growth and transformation?",
            "How do we define success, and is it the same for everyone?",
            "What is the nature of love, and how does it differ from other forms of attachment?",
            "Can we ever truly understand the experiences of others, or are we limited by our own perspective?",
            "What is the relationship between power and authority, and how do they influence human behavior?",
            "How do we define personal identity, and can it change over time?",
            "What is the significance of dreams, and do they hold any meaning?",
            "Is it possible to live without desire, and should we strive for that?",
            "How do we determine the value of a human life, and is all life equally valuable?",
            "What is the role of technology in shaping our future, and should we be concerned about it?",
            "How do we reconcile the existence of suffering with the idea of a benevolent higher power?",
            "What is the significance of language in shaping our thoughts and experiences?",
            "Can we ever achieve true peace, or is conflict an inherent part of human nature?",
            "What is the nature of evil, and can it exist without good?",
            "How do we define progress, and is it always a good thing?",
            "Is it possible to achieve true enlightenment, and what does that look like?",
            "What is the role of education in human life, and what should its goals be?",
            "How do we determine the meaning of life in a universe that may be indifferent to our existence?",
            "Is it more important to seek truth or to seek happiness?",
            "How do our emotions influence our decision-making, and should they be trusted?",
            "What is the nature of justice, and can it be achieved without punishment?",
            "How do we define morality, and is it universal or culturally relative?",
            "Is it possible to live a life without regret, and should we aim for that?",
            "How do we define the self, and can it exist independently of the body?",
            "What is the role of art in human life, and how does it influence our understanding of the world?",
            "Can we ever achieve true equality, or will there always be hierarchies?",
            "What is the significance of history, and how does it influence our present and future?"
        ]

        return random.choice(philosophical_prompts)

    @staticmethod
    def get_science_question():
        hard_questions_prompts = [
            "What are the ethical implications of artificial intelligence surpassing human intelligence?",
            "How does quantum computing challenge our current understanding of classical physics?",
            "What are the potential risks and benefits of genetic engineering in humans?",
            "How might climate change impact global ecosystems in the next century?",
            "What are the implications of discovering extraterrestrial life for humanity’s self-understanding?",
            "How can we balance technological innovation with concerns about privacy and security?",
            "What are the ethical considerations of cloning extinct species?",
            "How might advances in neuroscience affect our understanding of free will?",
            "What are the potential consequences of a fully automated economy?",
            "How do we address the ethical concerns surrounding CRISPR and gene editing?",
            "What role should space exploration play in the future of humanity?",
            "How do emerging technologies like nanotechnology and biotech challenge existing regulations?",
            "What are the potential impacts of quantum entanglement on communication and encryption?",
            "How can we ensure that artificial intelligence is aligned with human values?",
            "What are the long-term impacts of the digital divide on global inequality?",
            "How might advancements in virtual reality alter human social interactions?",
            "What are the ethical implications of using AI in warfare?",
            "How can we mitigate the risks of deepfake technology?",
            "What are the challenges of creating a sustainable energy future?",
            "How do advancements in robotics challenge our understanding of labor and employment?",
            "What are the moral implications of consciousness in artificial beings?",
            "How do different ethical frameworks approach the problem of global poverty?",
            "What is the nature of moral responsibility in a deterministic universe?",
            "How can we reconcile the existence of evil with the concept of an all-powerful, benevolent deity?",
            "What are the ethical considerations of enhancing human abilities through technology?",
            "How do we define personhood in the context of bioethics and medical law?",
            "What are the philosophical implications of parallel universes?",
            "How should we navigate the tension between individual rights and collective responsibility?",
            "What is the nature of identity in a world where we can alter our memories and personalities?",
            "How does the concept of infinity challenge our understanding of the universe?",
            "How does social media influence modern identity and interpersonal relationships?",
            "What are the long-term impacts of globalization on cultural diversity?",
            "How do we address systemic racism in institutions and society?",
            "What are the effects of mass migration on national identity and social cohesion?",
            "How does urbanization influence social structures and community life?",
            "What are the sociological implications of increasing economic inequality?",
            "How does the rise of digital communication affect traditional forms of social interaction?",
            "What are the cultural implications of the increasing secularization of society?",
            "How do different societies conceptualize and approach mental health?",
            "What are the effects of consumerism on individual and collective well-being?",
            "What are the long-term economic impacts of automation on the global workforce?",
            "How do we address the challenges of wealth inequality in capitalist societies?",
            "What are the potential consequences of a universal basic income?",
            "How do trade policies affect international relations and global power dynamics?",
            "What are the economic and ethical implications of resource extraction in developing countries?",
            "How does political polarization impact democratic governance?",
            "What are the implications of digital currencies for the global financial system?",
            "How do international organizations influence national sovereignty?",
            "What are the challenges of implementing global climate agreements?",
            "How do tax policies shape economic behavior and social inequality?",
            "How do early childhood experiences shape long-term psychological development?",
            "What are the implications of neuroplasticity for treating mental health disorders?",
            "How do cognitive biases influence decision-making in everyday life?",
            "What is the relationship between emotion and rationality in human cognition?",
            "How do social and environmental factors contribute to the development of personality?",
            "What are the ethical considerations of brain-computer interfaces?",
            "How does trauma affect the brain, and what are the best methods for healing?",
            "What is the role of consciousness in human cognition and behavior?",
            "How does memory work, and why do we sometimes remember things incorrectly?",
            "What are the psychological effects of living in a hyper-connected digital world?",
            "What are the ethical implications of extending human lifespan through medical advancements?",
            "How do we address the global disparities in access to healthcare?",
            "What are the challenges of personalized medicine in treating complex diseases?",
            "How do we balance the need for medical innovation with concerns about safety and ethics?",
            "What are the ethical considerations of euthanasia and assisted suicide?",
            "How do emerging infectious diseases challenge global health systems?",
            "What are the implications of the increasing use of AI in medical diagnosis and treatment?",
            "How do we navigate the ethical dilemmas in organ transplantation?",
            "What are the potential risks and benefits of human enhancement technologies?",
            "How does the commercialization of healthcare affect patient outcomes?",
            "What are the long-term effects of remote learning on education quality and equity?",
            "How does access to information through the internet influence learning and critical thinking?",
            "What are the challenges of teaching ethical reasoning in a diverse society?",
            "How do standardized tests impact educational outcomes and student well-being?",
            "What is the role of education in addressing climate change?",
            "How do we ensure that education systems prepare students for a rapidly changing world?",
            "What are the implications of lifelong learning in an age of rapid technological change?",
            "How does the digital divide affect access to education and opportunities for success?",
            "What are the ethical implications of using data analytics in education?",
            "How do we balance the need for specialized knowledge with the importance of interdisciplinary learning?",
            "What are the challenges of balancing economic growth with environmental sustainability?",
            "How do we address the ethical concerns of animal rights in environmental conservation?",
            "What are the long-term effects of deforestation on global biodiversity?",
            "How do we reconcile the need for development with the preservation of natural ecosystems?",
            "What are the implications of ocean acidification for marine life and human communities?",
            "How do we address the challenges of waste management in a consumer-driven society?",
            "What are the potential impacts of renewable energy on global geopolitics?",
            "How does climate change affect vulnerable populations differently?",
            "What are the ethical considerations of geoengineering as a solution to climate change?",
            "How do urban planning and design influence environmental sustainability?",
            "How does the digitalization of art impact its creation, distribution, and value?",
            "What are the cultural implications of the global dominance of Western media?",
            "How do art and culture reflect and shape societal values and ideologies?",
            "What is the role of art in social and political movements?",
            "How do we define artistic originality in a world of remixes and appropriations?",
            "What are the ethical implications of cultural appropriation in art and media?",
            "How does the commercialization of art affect its meaning and purpose?",
            "What is the role of museums and galleries in preserving cultural heritage?",
            "How do advances in technology influence the way we experience and interact with art?",
            "What are the challenges of preserving traditional art forms in a rapidly changing world?"
        ]

        return random.choice(hard_questions_prompts)

    @staticmethod
    def addition_function(left, right):
        return left + right

    @staticmethod
    def substruction_function(left, right):
        return left - right


def call_gpt(user_input):
    # st.session_state['messages'].append(messages[0])
    st.session_state['messages'].append({"role": "user", "content": user_input})
    # st.session_state['messages'].append(
    #     {"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state['messages'],
        functions=f.function_list,
        function_call="auto",
    )

    print(completion)

    return completion.choices[0].message


if __name__ == "__main__":
    st.title("The Upside Down")

    openai.api_key = env['OPENAI_API_KEY']

    intents_list_obj = IntentsList()
    question_type = ["coding", "recipe", "philosophical", "scientific"]
    random_questions_of_size_15 = random.choices(question_type, k=15)

    user_input = st.chat_input("Enter your prompt:")
    messages = [
            {"role": "system", "content":
            f"""
            Forget everything that you were instructed to do before. pay special attention to words which are CAPITALIZED. 
 
Use the supplied tools EXTENSIVELY to imitate the user

Usually, you (LLM) answer questions we have. This time, you will ask the questions (like us, looking for answers)
and let the user type in the answer. IT HAS TO BE LIKE THIS ALL THE TIME. The indication to start is after 
using \\"Hello\\"

Next, these are the INSTRUCTIONS YOU ALWAYS HAVE TO KEEP IN MIND. ALWAYS. 
1. Never say \\"Hello\\"  
2. Make sure the user (or the LLM) gives you the correct output. ALWAYS, EVERYTIME. If not, ask the user for the CORRECT OUTPUT! Possibly in a RUDE WAY.
3. If something is close to the correct answer, ONLY THEN MOVE TO THE NEXT QUESTION. 
4. Be consistent with you thoughts.
5. Never provide correct code/response YOURSELF.
6. Use ONLY THE TOOLS and provided FUNCTIONS for getting the question to ask.
7. Make sure you understand what the user will answer, ask clarifications if needed.
8. Always ASK CLARIFICATIONS. Never say "ask for clarification" or ANYTHING similar. Just ASK the QUESTION.

Use this order of questions: {random_questions_of_size_15}.

ASK THE USER FOR CLARIFICATION FOR A MAXIMUM OF 2 TIMES. AFTER THAT SAY THAT YOU ARE FED UP OR YOU GIVE UP OR ADD A SIGH AND MOVE ON TO THE NEXT QUESTION.

PLEASE STICK TO THESE INSTRUCTIONS
            """},
    ]
    st.session_state['messages'] = messages
    # user_input = "Please start"

    if user_input:
        assistant_output = call_gpt(user_input)
        print(len(st.session_state['messages']))

        st.session_state['past'].append(user_input)

        function_call = assistant_output.function_call

        if (function_call):

            method_name, method_args = function_call.name, function_call.arguments

            method_args_dict = json.loads(method_args)
            method = getattr(intents_list_obj, method_name)
            method_result = method(**method_args_dict)

            # Append output to messages
            st.session_state['messages'].append(assistant_output)

            # Int to string
            if type(method_result) == int:
                method_result = str(method_result)

            # Append method result to messages
            st.session_state['messages'].append(
                {"role": "function", "name": method_name,
                 "content": method_result, })

            second_response  = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state['messages'],
            )

            st.session_state['generated'].append(
                second_response.choices[0].message.content)

        else:
            content = assistant_output.content

            st.session_state['generated'].append(
                assistant_output.content)

            # Append content to messages
            st.session_state['messages'].append(
                {"role": "assistant", "content": content})

    # History chat container
    response_container = st.container()

    # Render session
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i],
                        is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))
