import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from twilio.rest import Client
from datetime import datetime
import gspread

# ----------------WhatsApp API Credentials--------------------------------#

account_sid = '<account_sid>'   # account_sid = 'AC2946b46774e496f09aa1fa70857277fd'
auth_token = '<auth_token>'     # auth_token = '20564e8333662fb30d300852fb348e63'
client = Client(account_sid, auth_token)

# -----------------Google Sheets API Credentials--------------------------#

sheets_acc = gspread.service_account(filename='filename.json')  # filename='client_secret.json'
sheet_id = sheets_acc.open_by_key('1x1sjE6k1bZRS77fQ-8B-LzYdssf_UaGeRyKMrFZYceY')
worksheet = sheet_id.worksheet('Sheet')

# -----------------------Time---------------------------------------------#
t = datetime.now()
st = t.strftime('%H:%M:%S')


def whatsAppMsgAPI(msg):
    message = client.messages.create(
        from_='whatsapp:+1xxxxxxxxxx',   # tiwilio API number
        body=msg,
        to='whatsapp:+91xxxxxxxxxx'     # Your phone number
    )


def file_handling(event):
    lines = 0
    f = open(event.src_path, 'r')
    for i in f:
        lines += 1
    return lines


def on_created(event):
    total_lines = file_handling(event)
    t = datetime.now()            # Time has been once again initiated to get updated time for message and sheets
    ct = t.strftime('%H:%M:%S')
    msg = f"{event.src_path} has been created! at {ct}"
    whatsAppMsgAPI(msg)
    worksheet.append_row([st, event.src_path, total_lines, ct, 'accepted'])


def on_deleted(event):
    t = datetime.now()
    ct = t.strftime('%H:%M:%S')
    msg = f"Someone deleted {event.src_path}! at {ct}"
    whatsAppMsgAPI(msg)


def on_modified(event):
    t = datetime.now()
    ct = t.strftime('%H:%M:%S')
    msg = f"{event.src_path} has been modified at {ct}"
    whatsAppMsgAPI(msg)


def on_moved(event):
    t = datetime.now()
    ct = t.strftime('%H:%M:%S')
    msg = f"someone moved {event.src_path} to {event.dest_path} at {ct}"
    whatsAppMsgAPI(msg)


if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    # Assigning (overriding) the pre-defined dummy method with our method...
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = f"F:\newfolder"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()