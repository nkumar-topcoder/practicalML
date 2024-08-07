import boto3
import json
import time
import os
import sys  

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
if not credentials.access_key: 
    print("AWS credentials not found")
    sys.exit(1)

inputcode = """
----sample math program---------------
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SimpleMath.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       77 NUM1 PIC 9(5) VALUE 10.
       77 NUM2 PIC 9(5) VALUE 20.
       77 SUM PIC 9(6).
       77 PRODUCT PIC 9(10).

       PROCEDURE DIVISION.
       MAIN-LOGIC.
           ADD NUM1 TO NUM2 GIVING SUM
           MULTIPLY NUM1 BY NUM2 GIVING PRODUCT
           DISPLAY "The sum of " NUM1 " and " NUM2 " is: " SUM
           DISPLAY "The product of " NUM1 " and " NUM2 " is: " PRODUCT
           STOP RUN.

"""

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

#This function sends a prompt to the Claude API and retrieves the response:
def call_claude_sonet(prompt):
    body = json.dumps({
        "prompt": "\n\nHuman:" + prompt + "\n\nAssistant:",
        "max_tokens_to_sample": 4056,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31",
    })
    response = bedrock_runtime.invoke_model(
        body=body, 
        modelId="anthropic.claude-v2", 
        accept='application/json', 
        contentType='application/json'
    )  
    response_body = json.loads(response.get('body').read())
    return response_body.get('completion')

#This function scans a directory for COBOL files:
def find_cobol_files(directory):
    cobol_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.cbl'):
                cobol_files.append(os.path.join(root, file))
    return cobol_files

#Documenting and Translating Code
#These functions generate documentation and translate COBOL code to a target language:
def code_documentation(inputcode):
    prompt = "You are a Pro*COBOL expert. Convert the following code into documentation and provide context with business logic if required: " + inputcode
    return call_claude_sonet(prompt)

def code_translation(inputcode, target_language):
    prompt = "Convert the given Pro*COBOL code into " + target_language + " and ensure proper formatting for the translated code: " + inputcode
    return call_claude_sonet(prompt)

#Main Execution
#The main block of the script demonstrates both documentation and translation:

if __name__ == "__main__":
    print("\n=========== Documentation Example ======================")
    codedocument = code_documentation(inputcode)
    print(f"Documentation:\n {codedocument}")

    print("\n========== Code Translation Example =====================")
    codetranslate = code_translation(inputcode, "Python")
    print(f"Code Translation:\n {codetranslate}")

#OPTIONAL 

   # ====Documentation & Translation for entire cobol Directory files=========
    # cobol_files = find_cobol_files("c:\\cobol")
    #for file in cobol_files:
    #  print(f"Documentation Started for File : {file}\n")
    #with open(file, 'r') as f:
    #    content = f.read()
    #    # For Documentation
    #    codedocument = code_documentation(content)
            
    #print(f"Code Translation started for file:\n {file}")
         #For Cobol code translation
         #param : Content = cobol code, target_languagetype = "Python" or "Java" or "C++" etc
    #codetranslate = code_translation(content,"Python")
    #print(f"codetranslate:\n {codetranslate}")
