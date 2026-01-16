from datetime import datetime
import os
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import pywhatkit
import pyautogui, time


def main():
    load_dotenv()

    PARENT_ID = os.getenv("GDRIVE_PARENT_FOLDER_ID")
    CREDS_PATH = os.getenv("GDRIVE_CREDENTIALS")
    CR_PHONE = os.getenv("CR_PHONE")
    os.environ["CHROME_USER_DATA_DIR"] = os.getenv("CHROME_USER_DATA_DIR")

    creds = Credentials.from_service_account_file(
        CREDS_PATH, scopes=["https://www.googleapis.com/auth/drive"]
    )

    service = build("drive", "v3", credentials=creds)

    def create_folder(name, parent_id):
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        folder = (
            service.files()
            .create(body=file_metadata, fields="id, webViewLink")
            .execute()
        )
        print(f"Folder {name} has been created successfully with ID: {folder['id']}")
        return folder["webViewLink"]

    def send_msg(link):
        time.sleep(10)
        pywhatkit.sendwhatmsg_instantly(
            phone_no=CR_PHONE,
            message=link,
            wait_time=10,
            tab_close=True,
            close_time=3,
        )
        
        time.sleep(2)
        pyautogui.press('enter')

    folder_link = create_folder(datetime.today().strftime("%Y-%m-%d"), PARENT_ID)
    send_msg(folder_link)


if __name__ == "__main__":
    main()
