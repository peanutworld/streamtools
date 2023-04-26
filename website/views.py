from flask import Blueprint, request, render_template, redirect, url_for, Markup, jsonify
import time
import os
import shutil
import datetime
import threading
import json

views = Blueprint('views', __name__)

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
website_dir = os.path.join(root_dir, 'website')
files_dir = os.path.join(website_dir, 'files')
static_dir = os.path.join(website_dir, 'static')
text_dir = os.path.join(files_dir, 'text')
images_dir = os.path.join(static_dir, 'images')


@views.route('/', methods=['GET', 'POST'])
def home():
    selected_match = 'trenutni'
    novi_team1 = read_from_file('team1.txt')
    novi_team2 = read_from_file('team2.txt')

    teams_data = load_json('teams.json')

    if request.method == 'POST' and 'uredi' in request.form:
        novi_score = request.form['score']
        novi_match = request.form['match']
        novi_team1 = request.form['team-1']
        novi_team2 = request.form['team-2']
        novi_naslov = request.form['naslov']
        novi_podnaslov = request.form['podnaslov']

        split_score = novi_score.split(':')

        if len(split_score[0]) == 2 or len(split_score[1]) == 2:
            novi_onedigit_score = ''
            write_to_file('onedigit_score.txt', novi_onedigit_score)
            write_to_file('twodigit_score.txt', novi_score)
        else:
            novi_twodigit_score = ''
            write_to_file('onedigit_score.txt', novi_score)
            write_to_file('twodigit_score.txt', novi_twodigit_score)

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

        write_to_file('match.txt', novi_match)
        write_to_file('naslov.txt', novi_naslov)
        write_to_file('podnaslov.txt', novi_podnaslov)
        

    score = read_from_file('onedigit_score.txt')
    if score == '':
        score = read_from_file('twodigit_score.txt')

    team1_options = ''
    team2_options = ''
    for team in teams_data:
        team1_options += '<option value="{}" {}>{}</option>'.format(team["value"], 'selected' if novi_team1 == team["value"] else '', team["name"])
        team2_options += '<option value="{}" {}>{}</option>'.format(team["value"], 'selected' if novi_team2 == team["value"] else '', team["name"])

        
    return render_template('home.html', 
                            score=score,
                            match=read_from_file('match.txt'),
                            selected_match=selected_match,
                            team1_options=Markup(team1_options),
                            team2_options=Markup(team2_options),
                            teams_data=teams_data,
                            images_dir=images_dir,
                            naslov=read_from_file('naslov.txt'), 
                            podnaslov=read_from_file('podnaslov.txt'))

@views.route('/teams')
def teams():
    data = load_json('teams.json')
    return render_template('teams.html', teams=data)

@views.route('/add_team', methods=['POST'])
def add_team():
    name = request.form['name']
    logo = request.files['logo']
    value = request.form['value']
    data = load_json('teams.json')
    data.append({'name': name, 'value': value})
    save_json('teams.json', data)
    logo.save(f'{images_dir}/{value}_logo.png')

    return redirect('/teams')

@views.route('/remove_team', methods=['POST'])
def remove_team():
    value = str(request.data.decode('utf-8'))
    teams = load_json('teams.json')
    teams = [team for team in teams if str(team['value']) != value]
    save_json('teams.json', teams)
    return jsonify({'success': True})

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

def load_json(filename):
    with open(os.path.join(text_dir, filename), 'r') as f:
        data = json.load(f)
    return data

def save_json(filename, data):
    with open(os.path.join(text_dir, filename), 'w') as f:
        json.dump(data, f, indent=4)

def write_to_file(filename, text):
    with open(os.path.join(text_dir, filename), 'w', encoding='utf-8') as file:
        file.write(text)

def read_from_file(filename):
    with open(os.path.join(text_dir, filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text
