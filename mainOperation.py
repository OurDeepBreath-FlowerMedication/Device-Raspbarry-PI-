# -*- coding: utf-8 -*-

import schedule
import time
import json
import API.callServer as cs
from datetime import datetime, timedelta

import assistant.callGemini as cg
import assistant.textToSpeech as tts

import device_control.takeMedication as tm
import device_control.flowerLED as fl
import device_control.flowerMoter as fm

flowerLED = fl.FlowerLED() # LED 제어를 위한 인스턴스 생성
flowerMoter = fm.FlowerMoter()
routines = [] # 하루 일정 저장(from Server)
moter_move = [False, False, False] # 모터 움직임 여부 확인

medi_take = { # 약 모터 제어 객체 저장
    '0' : tm.TakeMedication(0, moter_move[0], flowerLED, flowerMoter), 
    '1' : tm.TakeMedication(1, moter_move[1], flowerLED, flowerMoter),
    '2' : tm.TakeMedication(2, moter_move[2], flowerLED, flowerMoter)
    } 

daily_schedule = None # 일정 시간 계산 스케줄 객체 삭제
fin_time = "23:50:00" #"00:00:00" # 삭제 시간(상수)

# 매 10분마다 체크 후 알림
def routineTimeCheck() :
    global flowerLED
    global flowerMoter
    global routines
    global moter_move
    global medi_take
    global daily_schedule
    global fin_time

    now = datetime.now().strftime("%H:%M")

    # 종료 시점
    if fin_time <= now :
        flowerLED.turnOff()
        flowerMoter.close_flower() # 꽃 초기화
        
        for moter_num in range(3) :
            # 안움직인 모터 움직이기(약 버려짐)
            if(not moter_move[moter_num]) :
                tm.stepper_step(moter_num)
            
            # 버튼 비활성화(이벤트 리스너 삭제)
            if(medi_take[str(moter_num)].is_activate) :
                medi_take[str(moter_num)].deactivate_button()

        moter_move = [False, False, False]
        schedule.cancel_job(daily_schedule)
        return
    for routine in routines :
        # 약 일정 + 설정한 시간 지남.
        if routine['is_medication']!=-1 and routine['end_at'] < now :
            if(medi_take[str(routine['is_medication'])].is_activate) :
                medi_take[str(routine['is_medication'])].deactivate_button()

        if routine['start_at'] <= now <= routine['end_at']:
            if(routine['is_medication']==-1) :
                if(cg.doTheTask(routine['schedule_name'])) :
                    flowerLED.doneRoutine()
                    flowerMoter.blomming_flower()
                    if(routine['routin_id'] != 3) : # 식사 일정 여부 확인
                        # 식사 일정과 동일한 약 일정 찾기
                        medication = next((rou for rou in routines if rou.get('routin_id') == routine['routin_id'] and rou.get('is_medication') != -1), None)
                        if(medication) : 
                            # 식사 이전에 섭취해야 하는 약이라면 취소
                            if(medication['is_medication'] == 0) :
                                if(medi_take[str(routine['routin_id'])].is_activate) :
                                    medi_take[str(routine['routin_id'])].deactivate_button()
                                else :
                                    routines.remove(medication)

                            # 식사 도중에 섭취하는 약이라면 최대 30분 까지
                            elif(medication['is_medication'] == 1) :
                                medication['end_at'] = (datetime.now() + timedelta(minutes=30)).strftime("%H:%M")

                            # 식후 30분 후에 섭취하는 약이라면 최대 1시간 까지
                            else :
                                medication['start_at'] = (datetime.now() + timedelta(minutes=30)).strftime("%H:%M")
                                medication['end_at'] = (datetime.now() + timedelta(hours=1)).strftime("%H:%M")
                    cs.updateDone(routine['id'])
                    routines.remove(routine)
            else :
                if(routine['is_medication']==0) :
                     tts.tts("식전 약 드세요") 
                if(routine['is_medication']==1) : 
                     tts.tts("식사와 함께 약 드세요")
                if(routine['is_medication']==2) :  
                    meal = next((rou for rou in routines if rou.get('routin_id') == routine['routin_id'] and rou.get('is_medication') == -1), None)
                    if(meal) : continue
                    tts.tts("식후 약 드세요") 

                # 모터 제어 설정(버튼 이벤트 클릭 리스너 설정)
                not_take = 3
                for meal_time in range(3) :
                    if (medi_take[str(meal_time)].is_activate) : 
                        not_take = meal_time
                    if(routine['routin_id']==meal_time) :
                        # 그럴리는 없지만, 약 섭취 시간이 곂친다면, 뒤의 약(식사 기준) 섭취를 우선으로 함.
                        # 버튼이 하나만 있기에, 버튼에 대한 약 공급이 하나만 일어나도록 한 조치
                        if(not_take<meal_time) :
                            medi_take[str(not_take)].deactivate_button()

                        if(not medi_take[str(meal_time)].is_activate) : 
                            medi_take[str(meal_time)].activate_button(routines, routine)
        
            time.sleep(10)
                
 
# 특정 시간에 실행할 작업 정의
def getRoutines():
    global routines
    global moter_move
    global daily_schedule

    # 인터넷에서 일정 획득
    cs.getTodayRoutine()
    with open('/home/Dahee_youn/iot_project/data/todayRoutine.txt', 'r') as file :
        routines = json.loads(file.read())
    
    flowerLED.startDay(len(routines))
    flowerMoter.startDay(len(routines))
    
    # 매 10분 마다 루틴 알림
    daily_schedule = schedule.every(10).seconds.do(routineTimeCheck)
    #daily_schedule = schedule.every(10).minutes.do(routineTimeCheck)
    
# 처음 부팅시의 실행을 위해
getRoutines()

# 매일 오전 6시 10분에 작업 수행"06:10"
schedule.every().day.at("06:10").do(getRoutines)

# 매 해당 시간에 작업이 수행되도록 하기 위한 반복문
while True:
    schedule.run_pending()
    time.sleep(1)
