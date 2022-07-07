import xml.etree.ElementTree as ET
import requests
import smtplib
from email.mime.text import MIMEText
import pw
 
def callAPI():
    url = 'http://apis.data.go.kr/6260000/BusanBIMS/stopArrByBstopid'
    params ={'serviceKey' : 'JcfoCADRdvuoKVQ+BWTGO6Ztqm5WugNb03CCD4dzS6fm1mxpCe5lM3JLPdnONqoWeMp7W9+UbHRxf+/QuMycWQ==', \
    'bstopid' : '175830201' }

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
        if busNo == '51' or busNo == '77' or busNo == '100-1' :
            busInfo.append(child.find('lineno').text)
            busInfo.append(child.find('min1').text)
            busInfo.append(child.find('min2').text)
    return busInfo

def sendEmail(busInfo):
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()      # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(pw.id, pw.password)
    
    for i in busInfo:
        msgBody = msgBody + busInfo[0] + "번 버스 도착까지 " + busInfo[1] + "분 남았습니다. 다음 버스는 " + busInfo[2] + "분 후에 도착합니다."
    msg = MIMEText(msgBody)
    msg['Subject'] = '51번 버스 도착 시간 안내'
    msg['From'] = pw.email
    msg['To'] = pw.email
    smtp.sendmail(pw.email, pw.email, msg.as_string())
    smtp.quit()

def main():
    #root = fromFile()
    root = callAPI()
    busInfo = searchBusInfo(root)
    sendEmail(busInfo)
    
main()