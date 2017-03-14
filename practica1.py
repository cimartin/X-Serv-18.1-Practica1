#!/usr/bin/python3

import webapp
import csv
import os

class acortar_Url(webapp.webApp):
    diccUrl = {}
    diccUrlacort = {}
    contador = -1
    

    def Url(self, longitudUrl, Urlacortad):
        with open ("urls.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([int(Urlacortad)] + [longitudUrl])
        return None
        

    def leerDiccionario(self,file):
        with open("urls.csv", "r") as csvfile:
            if os.stat("urls.csv").st_size == 0:
                print("fichero vacio")
            else:
                reader = csv.reader(csvfile)
                for row in reader:  
                    self.diccUrlacort[row[1]] = int(row[0])
                    self.diccUrl[int(row[0])] = row[1]
                    self.contador = self.contador + 1
                return None

    def parse(self, request):
        try:
            metodo = request.split(' ', 2)[0]
            recurso = request.split(' ', 2)[1]
            try:
                body = request.split('\r\n\r\n')[1][6:]
            except IndexError:
                body = "" #Cuerpo vacio
        except IndexError:
            return None
        return (metodo, recurso, body)


    def process(self, parseRequest):
    
        (metodo,recurso, body) = parseRequest

        if len(self.diccUrlacort) == 0:
            self.leerDiccionario("urls.csv")
        if metodo == "GET":
            if recurso == "/":
                return ("200 OK", "<html><head></head><body>" + "<form action = '' method = 'POST'>" + "Url: <input type ='text' name = 'valor'>"  + "</form>" + "<p>" + str(self.diccUrlacort) + "</p></body></html>")     
            else:
                try:
                    recurso = int(recurso[1:])
                    if recurso in self.diccUrl:
                        return("300 Redirect", "<html><head></head><body><meta http-equiv = 'refresh'"+ " content = '1 url=" + self.diccUrl[recurso] + ">" "</body></html>")            
                    else:
                        return("404 Not Found", "<html><head></head><body>" + "recurso no encontrado" + "</body></head>")
                except ValueError:
                    return("404 Not Found", "<html><head></head><body>" + "recurso no encontrado" + "</body></html>")                           
        elif metodo == "POST":
            if body == "":
                return("404 Not Found", "<html><head></head><body>" + " no me has dado ninguna url a acortar" + "</body></html>")
            elif body.find("http") == -1:
                body = "http://" + body
                while body.find("%2F") != -1:
                    body = body.replace("%2F", "/")
                    
            
            else:
                while body.find("%2F") != -1:
                    body = body.replace("%2F", "/")
                    if body in self.diccUrlacort:
                        contador = self.diccUrlacort[body]
                        
                    else:
                        body = "http://" + body[9:]
                        self.contador = self.contador + 1
                        contador = self.contador
                        self.diccUrlacort[body] = contador
                        self.diccUrl[contador] = body
                        self.Url(body, contador)
                        return("200 OK", "<html><head></head><body>" + "<a href=" + body + ">" + body + "</href>" + "<p><a href= " + str(contador) + ">" + str(contador) + "</p></href></body></html>") 
            

        else:
            return("404 Not Found", "<html><head></head><body> metodo no encontrado </body></html>")

if __name__ == "__main__":
        testWebApp = acortar_Url("localhost", 1234)
  




