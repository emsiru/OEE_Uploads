# station 3
from opcua import Client
import time
import pymysql
import datetime

counter = 0
runtime= 0


url = "opc.tcp://192.168.0.30:4840"
client = Client(url)

while True:

    mydb = pymysql.connect(
            host="192.168.0.206",
            user="Emmanuel_Sim",
            password= "1221",
            database = "14octtraining"
        )
    cursor = mydb.cursor()

    client.connect()

    status = client.get_node('ns=2;s=Application.GVL_FTS.bFTS_Track0_Sending_gb')  
    mstatus = status.get_value()

    drivestate = client.get_node('ns=2;s=Application.GVL_VR2109.uiDrive_State') 
    dstatevalue = drivestate.get_value()

    ftsstate = client.get_node('ns=2;s=Application.GVL_VR2109.uiFTS_Track0_State')
    ftsvalue = ftsstate.get_value()

    actualOutput = "INSERT INTO `actualOutput` (`PID`, `actualOutput`, `time_stamp`) VALUES (%s, %s, %s)"
    runTime = "INSERT INTO `runTime` (`PID`, `runTime`, `time_stamp`) VALUES (%s, %s, %s)"

    if mstatus == True:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        counter += 1
        cursor.execute(actualOutput, ('', counter/2, timestamp))
        print('Output Count:', counter/2)

    if dstatevalue == 2 and ftsvalue == 2:
        runtime += 1
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(runTime, ('', runtime, timestamp))
        print('Run time:', runtime, 's')

    mydb.commit()
    mydb.close()

    client.disconnect()
    time.sleep(1)

    client.session_timeout = 10000
