from gpiozero import Button, LED
from signal import pause
import threading
import subprocess
import signal
import os
import time
from google_drive_helper import upload_file, download_file, update_flag_file, get_file_content, get_file_id_by_name, first_delete

# Define GPIO pins using gpiozero
button_record = Button(10)
button_send = Button(5)
button_play = Button(15)

led_record = LED(27)
led_waiting_to_send = LED(7)
led_new_message = LED(13)
led_game_state = LED(21)

# Initial state
recording_process = None
audio_filename = 'bondi2_audio.wav'
received_audio_filename = 'bondi1_audio.wav'
flag_file_id_bondi1 = '1VqR_HutoryHY2SiiP5Gi4qaNomdG0Y4F'  # Replace with your Google Drive flag file ID
flag_file_id_bondi2 = '1Ku6u4mgGht2DExh8I4lQUCQB1Cb80ktu'  # Replace with your Google Drive flag file ID
folder_id = '1eeQAw8t204Kw4yYgLXzVd2ORLdrpM2cH'  # Replace with your Google Drive folder ID
audio_file_id = None

upload_event = threading.Event()

def start_recording():
    global recording_process
    led_game_state.on()
    print("Start recording...")
    led_record.on()
    recording_process = subprocess.Popen(['arecord', '-D', 'plughw:3,0', '-f', 'cd', '-t', 'wav', '-r', '44100', '-c', '1', audio_filename])

def stop_recording():
    global recording_process
    if recording_process:
        recording_process.terminate()
        recording_process = None
    led_record.off()
    led_waiting_to_send.blink(on_time=0.2, off_time=0.2)

def send_audio():
    global audio_file_id
    print("Uploading audio to Google Drive...")
    upload_event.set()
    led_waiting_to_send.off()
    audio_file_id = upload_file(audio_filename, audio_filename, folder_id)
    update_flag_file(flag_file_id_bondi2, 1)
    led_game_state.off()
    upload_event.clear()

def play_audio():
    print("Playing audio...")
    led_new_message.off()
    subprocess.run(['aplay', received_audio_filename])

def check_for_new_audio():
    global audio_file_id
    while True:
        if(upload_event.is_set()):
            time.sleep(10)
            continue
        flag_value = int(get_file_content(flag_file_id_bondi1))
        if flag_value == 1:
            print("New audio file available, downloading...")
            file_id = get_file_id_by_name(received_audio_filename, folder_id)
            download_file(file_id, received_audio_filename)
            update_flag_file(flag_file_id_bondi1, 0)
            led_game_state.on()
            led_new_message.blink(on_time=0.2, off_time=0.2)

        time.sleep(10)

def button_handler():
    button_record.when_pressed = start_recording
    button_record.when_released = stop_recording
    button_send.when_pressed = send_audio
    button_play.when_pressed = play_audio

def cleanup(signal, frame):
    global recording_process
    if recording_process:
        recording_process.terminate()
    led_record.off()
    led_waiting_to_send.off()
    led_new_message.off()
    led_game_state.off()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    first_delete(audio_filename, folder_id)
    # Start the check for new audio loop in a separate thread
    check_audio_thread = threading.Thread(target=check_for_new_audio)
    check_audio_thread.start()

    # Set up button handlers
    button_thread = threading.Thread(target=button_handler)
    button_thread.start()

    button_thread.join()
    check_audio_thread.join()
