from flask import Blueprint, request, render_template, redirect, url_for
import time
import os
import shutil
import datetime
import threading

views = Blueprint('views', __name__)

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
website_dir = os.path.join(root_dir, 'website')
files_dir = os.path.join(website_dir, 'files')
text_dir = os.path.join(files_dir, 'text')
images_dir = os.path.join(files_dir, 'images')


@views.route('/', methods=['GET', 'POST'])
def home():
    selected_match = 'trenutni'
    novi_team1 = read_from_file('team1.txt')
    novi_team2 = read_from_file('team2.txt')

    if request.method == 'POST' and 'uredi' in request.form:
        novi_onedigit_score = request.form['onedigit_score']
        novi_twodigit_score = request.form['twodigit_score']
        novi_match = request.form['match']
        novi_team1 = request.form['team-1']
        novi_team2 = request.form['team-2']
        novi_naslov = request.form['naslov']
        novi_podnaslov = request.form['podnaslov']

        if novi_onedigit_score:
            novi_twodigit_score = ''

        if novi_match == 'trenutni':
            novi_match = 'Trenutni'
            selected_match = 'trenutni'
        elif novi_match == 'sljedeci':
            novi_match = 'Sljedeći'
            selected_match = 'sljedeci'

        write_to_file('team1.txt', novi_team1)
        write_to_file('team2.txt', novi_team2)
        
        filename_team1 = f"{novi_team1}_logo.png"
        filename_team2 = f"{novi_team2}_logo.png"
        shutil.copyfile(os.path.join(images_dir, filename_team1), os.path.join(images_dir, 'team1.png'))
        shutil.copyfile(os.path.join(images_dir, filename_team2), os.path.join(images_dir, 'team2.png'))

        write_to_file('onedigit_score.txt', novi_onedigit_score)
        write_to_file('twodigit_score.txt', novi_twodigit_score)
        write_to_file('match.txt', novi_match)
        write_to_file('naslov.txt', novi_naslov)
        write_to_file('podnaslov.txt', novi_podnaslov)
        
    return render_template('home.html', 
                            onedigit_score=read_from_file('onedigit_score.txt'),
                            twodigit_score=read_from_file('twodigit_score.txt'),
                            match=read_from_file('match.txt'),
                            selected_match=selected_match,
                            selected_team1=novi_team1,
                            selected_team2=novi_team2,
                            naslov=read_from_file('naslov.txt'), 
                            podnaslov=read_from_file('podnaslov.txt'))

@views.route('/time')
def start_timer():
    write_to_file('vrijeme_trenutno.txt', 'Vrijeme')
    write_to_file('vrijeme_timer.txt', '')

    global stop_timer
    stop_timer = False
    
    # stop the countdown if it's running
    global stop_countdown
    stop_countdown = True
    
    threading.Thread(target=update_timer).start()

    return """
    <html><head><script>
        setTimeout(() => {
            window.close();
        }, 10);
    </script></head></html>
    """

@views.route('/countdown', methods=['GET', 'POST'])
def start_countdown():
    if request.method == 'POST':
        countdown_value = request.form['vrijeme_countdown']
        write_to_file('vrijeme_timer.txt', 'Vraćamo se za')
        write_to_file('vrijeme_trenutno.txt', '')
        
        # stop the timer if it's running
        global stop_timer
        stop_timer = True
        
        global stop_countdown
        stop_countdown = False
        
        threading.Thread(target=update_countdown, args=(int(countdown_value),)).start()

        return """
        <html><head><script>
            setTimeout(() => {
                window.close();
            }, 10);
        </script></head></html>
        """
    return redirect(url_for('views.home'))

@views.route('/stop')
def stop_timers():
    global stop_timer
    stop_timer = True
    
    global stop_countdown
    stop_countdown = True

    write_to_file('time.txt', '00:00')
    
    return """
    <html><head><script>
        setTimeout(() => {
            window.close();
        }, 10);
    </script></head></html>
    """

def update_timer():
    while not stop_timer:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        with open(os.path.join(text_dir, 'time.txt'), 'w') as file:
            file.write(current_time)
        time.sleep(1)

def update_countdown(countdown_value):
    with open(os.path.join(text_dir, 'time.txt'), 'w') as file:
        for i in range(countdown_value, -1, -1):
            if stop_countdown:
                break
            
            minutes = i // 60
            seconds = i % 60
            file.seek(0)
            file.write(f"{minutes:02d}:{seconds:02d}")
            file.truncate()
            file.flush()
            time.sleep(1)

def write_to_file(filename, text):
    with open(os.path.join(text_dir, filename), 'w', encoding='utf-8') as file:
        file.write(text)

def read_from_file(filename):
    with open(os.path.join(text_dir, filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text
