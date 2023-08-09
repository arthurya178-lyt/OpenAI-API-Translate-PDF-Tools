
from PyPDF2 import PdfReader
import os
import json
from nltk.tokenize import sent_tokenize
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
FileName = os.getenv("FILE_NAME")
page_start_at = int(os.getenv("PDF_START_PAGE"))
page_end_at = int(os.getenv("PDF_END_PAGE"))
language = os.getenv("LANGUAGE")



reader = PdfReader(f'./SourceFile/{FileName}')
Token_used = 0
Token_send = 0
Token_receive = 0

def send_to_chatGPT3_5(text):
    ask_question = text
    target_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Translate to {language} {ask_question}\n"}],
        "temperature": 0.5,
    }
    new_session = requests.session()
    response = new_session.post(target_url, data=json.dumps(request_data), headers=headers)
    parse_result = response.json()
    # parse_result = {"choices": [{"message": {"content": "123123"}}]}
    serial_num = 0
    while True:
        if os.path.isfile(f'./logger/Log {datetime.now().strftime("%Y-%m-%d %H%M%S")} {serial_num}.txt'):
            serial_num += 1
        else:
            break
    f = open(f'./logger/Log {datetime.now().strftime("%Y-%m-%d %H%M%S")} {serial_num}.txt' ,'w',encoding="UTF-8")
    if type(parse_result) == type({}):
        f.write(json.dumps(parse_result, indent=2))
    f.writelines("\n")
    f.write(str(parse_result))
    f.close()

    chunks = []
    for choice in parse_result['choices']:
        print("原文: ")
        print(text)
        print()
        print("譯文: ")
        print(choice['message']['content'])
        print()
        chunks.append(choice['message']['content'])
    global Token_used, Token_receive, Token_send
    Token_used += int(parse_result['usage']['total_tokens'])
    Token_receive += int(parse_result['usage']['completion_tokens'])
    Token_send += int(parse_result['usage']['prompt_tokens'])
    return chunks


if page_end_at is None or page_end_at == 0:
    page_amount = len(reader.pages)
else:
    page_amount = page_end_at
chunks = []
for pages in range(page_start_at, page_amount):
    page = reader.pages[pages]
    sentences = sent_tokenize(page.extract_text())
    #print(sentences)
    sentence = ""
    for text in range(len(sentences)):
    #for text in range(1):
        sentence += sentences[text]
        if len(sentence) > 1000:
            chunks.append(sentence)
            sentence = ""
    if len(sentence) != 0:
        chunks.append(sentence)
        sentence = ""
#print(chunks)


print(f"===== Start Translate PDF =====")
write_result_file_name = f'./result/{datetime.now().strftime("%Y-%m-%d %H%M%S")}.txt'
for index in range(len(chunks)):
    f = open(write_result_file_name, 'a', encoding="UTF-8")
    for gpt_chunk in send_to_chatGPT3_5(chunks[index]):
        f.writelines(gpt_chunk)
    f.close()
    print(f"Translate Progress  {index+1}/{len(chunks)}")

f = open(write_result_file_name, 'a', encoding="UTF-8")
f.writelines("\n\n")
f.writelines("======== This translation Used Token and valuation ==========\n")
f.writelines(f'Current used token: Send:{Token_send} Receive:{Token_receive} Total:{Token_used}\n')
f.writelines(f'Price: Send_price:{Token_send/1000*0.0015} Receive_price:{Token_receive/1000*0.002} Total:{(Token_send/1000*0.0015)+(Token_receive/1000*0.002)}\n')
f.close()


print("======== This translation Used Token and valuation ==========")
print(f'Current used token: Send:{Token_send} Receive:{Token_receive} Total:{Token_used}')
print(f'Price: Send_price:{Token_send/1000*0.0015} Receive_price:{Token_receive/1000*0.002} Total:{(Token_send/1000*0.0015)+(Token_receive/1000*0.002)}')

print("\n\n")
print("~~~~~ Translate Complete ~~~~")
