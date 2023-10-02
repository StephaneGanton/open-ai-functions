import openai
import json
import db_helpers

from secret_key import API_SECRET_KEY
openai.api_key = API_SECRET_KEY

def get_answer(question):

    messages = [{'role': 'user', 'content': question}]
    functions = [
        {
            "name": "get_marks",
            "description": """Get the GPA for a college student or aggregate GPA (such as average, min, max)
                for a given sementer. If function returns -1 then it means we could not find the record in the db""",
            
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "First and last name of the student, e.g John Doe",
                    },
                    "semester": {
                        "type": "integer", 
                        "description": "A number between 1 to 4 indicating the semester of a student",
                        },

                    "operation": {
                        "type": "string",
                        "description": """If student is blank that means aggregate number such as max, min or average is being
                            requested for an entire semester. semester must be passed in this case. If student field is blank and say 
                            they are passing 1 as a value in semester. Then operation parameter will tell if they need a maximum, minimum
                            or an average GPA of all students in semester 1.
                            """,
                        "enum": ["max", "min", "avg"]
                    },
                },
                "required": ["semester"],
            },
        },

        {
            "name": "get_fees",
            "description": """Get the fees for an individual student or total fees for an entire semester.
                If function returns -1 then it means we could not find the record in a db for given input""",

            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "First and last Name of the student. e.g John Smith",
                    },
                    "semester": {
                        "type": "integer",
                        "description": "A number between 1 to 4 indicating the semester of a student",
                    },
                    "fees_type": {
                        "type": "string",
                        "description": "fee type such as 'paid', 'pending' or 'total'",
                        "enum": ["paid", "pending", "total"]
                    },
                },
                "required": ["semester"],
            },
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )

    response_message = response["choices"][0]["message"]


    
    if response_message.get("function_call"):
        
        available_functions = {
            "get_marks": db_helpers.get_marks,
            "get_fees": db_helpers.get_fees,
        }

        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])

        function_response = function_to_call(function_args)

        #return function_response

        messages.append(response_message)
        messages.append({
            "role": "function",
            "name": function_name,
            "content": str(function_response)
        })

        second_call_response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0613",
            messages= messages
        )

        return second_call_response["choices"][0]["message"]["content"]
    else:
        return response_message["content"]
    
    #return response_message

if __name__== '__main__':
    #print(get_answer("how much was peter pandey's due fees in the first semester?"))

    # print(get_answer("What was Peter Pandey's GPA in semester 1?"))
    # print(get_answer("average gpa in third semester?"))
    # print(get_answer("how much is peter pandey's pending fees in the first semester?"))
    #print(get_answer("how much was peter pandey's due fees in the first semester?"))
    print(get_answer("what is the purpose of a balance sheet?"))