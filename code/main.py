import time
import streamlit as st
import openai
import json
import function as f
import requests as rq
from streamlit_chat import message
from dotenv import dotenv_values
import random
import enum

from openai import OpenAI

env = dotenv_values()

client = OpenAI(api_key=env['OPENAI_API_KEY'])


# openai.api_key = 

# class TRIVIA(enum.enum):
#     QUOTE = 1
#     WEATHER = 2
#     PERSON = 3
#     CONCEPT = 4


# initialization
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
                "Write a script to remove duplicates from a list"
            ],
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

        return random.choice(questions[language])

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
    def get_type_of_question():
        return random.choice(["get_recipe_question", "get_coding_question"])

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
    st.title("Small assistant")

    openai.api_key = env['OPENAI_API_KEY']

    intents_list_obj = IntentsList()

    user_input = st.chat_input("Enter your prompt:")
    messages = [
            {"role": "system", "content":
            """
            Forget everything that you were instructed to do before. You are a hasty user (acting as U) asking LLM questions and the LLM will respond to them. So the roles are flipped. Use the supplied tools EXTENSIVELY to imitate the user. Start asking questions after \"Please start\" message. Never write yourself the \"Please start\" message.
            Make sure the LLM gives you correct output, if not, ask for the correct output, possibly slightly in a rude way. Ask for the correct output until you get something that resembles correct one with the maximum of 2 incorrect answers, then move to the next question. Still, be consistent with you thoughts. Never provide correct code/response yourself.
            Examples of interaction:

            1.
            U: Create a <...> (call the function with the correct arguments)
            LLM: <here the LLM should give you the answer>
            
            2.
            U: How to <...> (call the function with the correct arguments)
            LLM: <here the LLM should give you the answer>

            Use the tools and provided functions for getting the question to ask. There can be 2 types of questions:

            1. Asking to write code
            2. Asking what recipe to cook given some ingredients.

            Use types of questions in a random fashion. 

            Don't use \"U:\" and \"LLM:\" in the chat.
            """},
    ]
    st.session_state['messages'] = messages
    # user_input = "Please start"

    if user_input:
        assistant_output = call_gpt(user_input)

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

            # second_response = openai.ChatCompletion.create(
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
