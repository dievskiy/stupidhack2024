function_list = [
    {
        "name": "get_science_question",
        "description": "Get a science question",
        "parameters": {}
   },
    {
        "name": "get_philosophical_question",
        "description": "Get a philosophical question",
        "parameters": {
                "type": "object",
                "properties": {
                    "philosopher_name": {
                        "type": "string",
                        "description": "Name of the philosopher"
                    },
                },
            "required": ["philosopher_name"],
        }

    },
    {
        "name": "get_recipe_question",
        "description": "Get a question on how to make a recipe from some ingredients ",
        "parameters": {}
   },
    {
        "name": "get_coding_question",
        "description": "Get a coding question. ",
        "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Programming language to use for the task"
                    },
                },
            "required": ["language"],
        }
    }
]
