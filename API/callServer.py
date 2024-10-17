import requests
import json
import API.linkData as ld

# 서버에서 데이터를 가져와 메모장에 기록
def getTodayRoutine() :
    params = {'deviceID': ld.deviceID}
    response = requests.get(f"{ld.ServerIP}/done/getrsp", params=params)

    try :
        with open('/home/Dahee_youn/iot_project/data/todayRoutine.txt', 'w') as file:
            json.dump(response.json(), file)  
    except ValueError:
        print(ValueError)

# 수행 완료한 작업 done으로 업데이트
def updateDone(doneID) :
    params = {'deviceID': ld.deviceID, 'doneID' : doneID}
    requests.get(f"{ld.ServerIP}/done/update", params=params)

