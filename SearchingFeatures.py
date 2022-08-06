from asyncio.windows_events import ERROR_CONNECTION_REFUSED
from cProfile import label
import os.path
from urllib.error import HTTPError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64 
from bs4 import BeautifulSoup
import re
import email
import csv
import pandas as pd

class ConstruccionFeatures():
    def __init__(self,lugar,cant):
        self.tipoDeCasilla=lugar
        self.cantidadResultadosMaximos=cant
        self.VocabularyWords=pd.read_csv("words.csv",encoding='latin1',header=None)
        features=list()
        self.df=pd.DataFrame()
        for word in self.VocabularyWords:
            features.append(str(word))

        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())    
        self.service = build('gmail', 'v1', credentials=self.creds)
    def ExportarData(self):
        self.df.to_csv("finalData.csv", encoding='latin1', index=False)
    def construir(self):
        results = self.service.users().messages().list(userId='me',maxResults=self.cantidadResultadosMaximos,q='in:'+self.tipoDeCasilla).execute()
        messages = results.get('messages')
        vocabulary=dict()
        count=0
        for message in messages:
            #obtener_mensaje(service,"me",message["id"])
            msg_raw=self.service.users().messages().get(userId='me',id=message["id"]).execute()
            try:        
                #body = base64.b64decode(msg['raw'])
                #print(body)
                payload=msg_raw["payload"]
                headers=payload["headers"]
                for heade in headers:
                    if heade["name"]=="Subject":
                        self.subject=heade["value"]
                    if heade["name"]=="From":
                        self.sender=heade["value"].split(" ")[-1][1:-1]
                    if heade["name"]=="Date":
                        date=re.split("\s+",heade["value"])
                        hour=int(date[4].split(":")[0])
                        #print(hour)
                parts=payload.get("parts")[0]
                data=parts["body"]["data"]
                data=data.replace("-","+").replace("_","/")
                decoded_data=base64.b64decode(data)
                
                #Text analysis
                #########################################################################################################################
                soup = BeautifulSoup(decoded_data , "lxml")
                body = str(soup.body())
                
                #FORMATTING
                new_body=re.sub("\s+"," ",body)[4:-5]#replace any whitespace with a space
                new_body=new_body.lower()#a minuscula

                new_body=re.sub("[<].+?[>]","",new_body)#delete all the sentences within <...>

                #Obtener y reemplazar todos los links del texto
                links=re.findall("http[s]?://\S+", new_body)
                new_body=re.sub("http[s]?://\S+","urljans",new_body)        
                
                #Obtener y reemplazar todos los emails del texto
                emails=re.findall("\S+@\S+", new_body)
                new_body=re.sub("\S+@\S+","mailsjans",new_body)

                #Obtener y reemplazar todos los números de teléfono
                telephoneNumbers=re.findall("[0-9]{6,}", new_body)
                new_body=re.sub("[0-9]{6,}","telephonenumber",new_body)

                #Obtener la cantidad de simbolos s/.
                preciossoles=re.findall("s/.", new_body)
                cantidadSimbolosSoles=len(preciossoles)
                preciosdolares=re.findall("[$]",new_body)
                cantidadSimbolosDolares=len(preciosdolares)
                cantidadSimbolosPrecios=cantidadSimbolosDolares+cantidadSimbolosSoles
                new_body=re.sub("s/.","preciosoles",new_body)

                
                #Obtaining words
                new_body=''.join(" " if not (caracter.isalnum()) else caracter for caracter in new_body )
                new_body=re.sub("\s+"," ",new_body)
                print(new_body)
                finalWords=new_body.split(" ")
                
                self.df.loc[count,self.VocabularyWords.iloc[:,0]]=[((word in finalWords)+0) for word in self.VocabularyWords.iloc[:,0]]
                self.df.loc[count,"simboloPrecio"]=(cantidadSimbolosPrecios>0)+0

                self.df.loc[count,"cantidadLinks"]=len(links)
                self.df.drop(["urljans"],axis="columns",inplace=True)
                
                self.df.loc[count,"cantidadEmails"]=len(emails)
                self.df.drop(["mailsjans"],axis="columns",inplace=True)

                self.df.loc[count,"cantidadNumbers"]=len(telephoneNumbers)

                self.df.loc[count,"CorreoInstitucional"]=(self.sender.endswith("edu.pe") or self.sender.endswith("edu.p") or ("pucp" in self.sender))+0
                
                intervals=["madrugada","mañana","tarde","noche"]
                horas=[list(range(0,7)),list(range(7,13)),list(range(13,19)),list(range(19,23))+[23]]
                index_intervalo_hora=[hour in rango for rango in horas].index(True)
                #self.df.loc[count,"HoraDeEnvio"]=intervals[index_intervalo_hora]
                self.df.loc[count,intervals]=[hour in rango for rango in horas]
                self.df.loc[count,"target"]=self.tipoDeCasilla
                    
                ########################################################################################################################
                count+=1
                print(count)
                break
                ########################################################################################################################
            except:
                pass


