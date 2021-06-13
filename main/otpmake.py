import pyotp     # pyotp 
import datetime  # 시간 라이브러리

# otp에 사용할 키 - base32 방식 A-Z 2-7까지를 이용하고 = 는 채워야하는 공간 패딩 처리용
totp = pyotp.TOTP('GAYDAMBQGAYDAMBQGAYDAMBQGA======', 10)  # 180초 간격, 즉 3분마다 변경됨
otp_value = totp.now()  # 현재 시간을 기준으로 otp 값을 얻는다.

# totp.at을 이용한 TOTP 값 출력, totp.now를 이용한 출력
print("now totp.at: " +  str(totp.at(datetime.datetime.now())) + ", totp.now : " + totp.now())