from flask import Flask, render_template, request, jsonify
import pyautogui as pg
import time
import threading

app = Flask(__name__)

# Define a global variable to keep track of the process status
process_running = False
process_lock = threading.Lock()

@app.route('/', methods=['GET', 'POST'])
def index():
    global process_running
    if request.method == 'POST':
        name = request.form['name']
        a_names = open("./animals.txt", 'r').readlines()
        a = name + " is a "

        # Delay before starting typing
        time.sleep(10)

        with process_lock:
            process_running = True

        for i in a_names:
            with process_lock:
                if not process_running:
                    break

            pg.write(a + i)
            pg.press('enter')
            time.sleep(0.5)
    
    return render_template('index.html')

@app.route('/end_process', methods=['POST'])
def end_process():
    global process_running
    with process_lock:
        process_running = False
    return jsonify({'message': 'Process ended successfully'})

if __name__ == '__main__':
    app.run(debug=True)
