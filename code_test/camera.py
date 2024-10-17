import cv2
from picamera2 import Picamera2

# Picamera2 객체 생성 및 카메라 시작
picam2 = Picamera2()
#picam2.set_controls({'Resolution': (640, 480)})
config = picam2.create_still_configuration(main={"size": (640, 480)})
picam2.start()


while True:
    # 카메라에서 이미지 캡처py
    im = picam2.capture_array()

    # BGR에서 RGB로 변환
    im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # 이미지를 창에 표시
    cv2.imshow("Camera", im_rgb)

    # 'q' 키가 눌리면 루프를 종료하고 카메라 피드를 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 창을 닫고 Picamera2를 정리
cv2.destroyAllWindows()
picam2.stop()