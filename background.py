from threading import Thread

from flask import Flask

app = Flask('')
 
@app.route('/')
def home():
  return "Я работаю"
 
def run():
  app.run(host='0.0.0.0', port=80)
 
def keep_alive():
  t = Thread(target=run)
  t.start()
