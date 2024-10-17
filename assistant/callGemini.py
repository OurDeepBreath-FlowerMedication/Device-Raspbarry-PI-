import google.generativeai as genai
import os
import assistant.speechToText as stt
import assistant.textToSpeech as tts

genai.configure(api_key=os.environ["API_KEY"])

def doTheTask(task) :
    systemInstruction = '''
    1. '질문'에 대한 '응답'이 일정을 수행했음이 추측 가능하거나 긍정표현(예) 응, 어, 당근 등) 1을,
    2. 일정을 수행한 것이 아닌게 확실하면 0을,
    3. 응답이 질문과 관련 없는 내용이거나, 질문에 대한 직접적인 답변이 아닐 경우 -1을 반환한다.
    '''
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=systemInstruction)
    chat = model.start_chat(history=[])

    cnt = 0
    result = -1

    while(1) :
        message = stt.getResponse(task)
        if message :
            print(message)
            response = model.generate_content("질문 : " + task + "을/를 하셨나요? \n응답 : " + message)
            result = int(response.text)
        if result == 1 :
            tts.tts("수고하셨습니다.")
            return True
        elif result == 0 :
            tts.tts("일과를 완료하지 못하셨군요.")
            return False
        else :
            cnt += 1
            if(cnt < 3) :
                tts.tts("응답을 이해하지 못했습니다. 다시 말씀해 주세요.") 
            else : 
                tts.tts("응답을 이해하지 못했습니다.")
                return False

