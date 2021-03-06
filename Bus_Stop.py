import xml.etree.ElementTree as ET
import requests
import smtplib
from email.mime.text import MIMEText
import pw
 
def callAPI(bstopid):
    url = 'http://apis.data.go.kr/6260000/BusanBIMS/stopArrByBstopid'
    params ={'serviceKey' : 'JcfoCADRdvuoKVQ+BWTGO6Ztqm5WugNb03CCD4dzS6fm1mxpCe5lM3JLPdnONqoWeMp7W9+UbHRxf+/QuMycWQ==', \
    'bstopid' : bstopid }

    response = requests.get(url, params=params)
    content = response.text

    root = ET.fromstring(content)
    return root

def fromFile():
    root = ET.parse('bus.xml').getroot()
    return root

def searchBusInfo(root):
    busInfo = []
    for child in root.iter('item'):
        busNo = child.find('lineno').text
        bstopid = child.find('bstopid').text
        if (bstopid == '175830201' and busNo == '51') or (bstopid == '175830301' and (busNo == '77' or busNo == '100-1')) :
            busInfo.append(child.find('lineno').text)
            busInfo.append(child.find('min1').text)
            busInfo.append(child.find('min2').text)
    return busInfo

def sendEmail(busInfo):
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()      # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(pw.id, pw.password)
    
    msgBody = str()
    for i in busInfo:
        locPointer = 3
        currentLoc = 1
        for j in i:
            if (currentLoc%locPointer == 1):
                msgBody = msgBody + j + "번 버스 도착까지 "
            elif (currentLoc%locPointer == 2):
                msgBody = msgBody + j + "분 남았습니다. 다음 버스는 "
            else:
                msgBody = msgBody + j + "분 후에 도착합니다.\n\r"
            currentLoc = currentLoc + 1
    msg = MIMEText(msgBody)
    msg['Subject'] = '버스 도착 시간 안내'
    msg['From'] = pw.email
    msg['To'] = pw.email
    smtp.sendmail(pw.email, pw.email, msg.as_string())
    smtp.quit()

def main():
    #root = fromFile()
    bstopid = ['175830201','175830301']
    busInfo = []
    for i in bstopid:
        root = callAPI(i)
        busInfo.append(searchBusInfo(root))
    sendEmail(busInfo)
    
main()