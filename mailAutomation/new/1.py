from RPA.Browser.Selenium import Selenium

from RPA.FileSystem import FileSystem

from RPA.Excel.Files import Files

import subprocess

import re

import os

import time

import win32com.client

import zipfile

# from connect_db import connect_to_db

import pandas as pd

import glob

from datetime import datetime

import shutil

import sys

# from notifier import send_email

import traceback

# from sqlalchemy import text

 

## defining subject and path for downloading the files

 

# destination = ---- your destsination

# Table_Name  = 'Suit_Approvals'

 

# base_directory = -- your directory

 

## function to open outlook

 

# def open_outlook():

#     outlook_path = your outllok.exe file path
#     subprocess.Popen(outlook_path)
#     print(f"Launching Outlook ......Waiting for COM interface to Launch Outlook successfully")

    

#     time.sleep(20)
    
import subprocess
import time
import os

def open_outlook():
    outlook_path = r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"  # Update this path if needed

    if not os.path.exists(outlook_path):
        print("Outlook executable not found.")
        return

    subprocess.Popen(outlook_path)
    print("Launching Outlook... Waiting for COM interface to initialize.")
    time.sleep(20)  # Wait for Outlook to launch


# def open_outlook():

#     max_attempts = 10

#     sleep_seconds = 3

 

#     try:

#         # Try to get existing Outlook instance

#         outlook = win32com.client.GetActiveObject("Outlook.Application")

#         print("✅ Attached to existing Outlook instance.")

#         return outlook

#     except Exception:

#         print("📨 No running Outlook instance found. Launching new one...")

 

#     # Start Outlook via subprocess (non-blocking)

#     subprocess.Popen([r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"])

   

#     # Try connecting repeatedly

#     for attempt in range(1, max_attempts + 1):

#         try:

#             outlook = win32com.client.GetActiveObject("Outlook.Application")

#             print("✅ Outlook launched and connected.")

#             return outlook

#         except Exception:

#             print(f"⏳ Outlook not ready (attempt {attempt}/{max_attempts}). Retrying...")

#             time.sleep(sleep_seconds)

   

#     # If still not connected, raise error

#     raise RuntimeError("❌ Outlook failed to initialize after multiple attempts.")

   

 

## function to fetch the mails containg link

 

def fetch_emails():
    

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    inbox = outlook.GetDefaultFolder(6)

    messages = inbox.Items

   

   ## filter only unread emails:

    unread_emails = messages.Restrict("[Unread] = true")

   

    ## sort emails:

    unread_emails.Sort("[ReceivedTime]", True)

   

   

   

    approval_pattern = re.compile(r"\bapproval(s|ed)?\b", re.IGNORECASE)

 

    for message in unread_emails:

        try:

            body = message.Body

            subject = message.Subject

            received = message.ReceivedTime

 

            # URL pattern matching

            matches = re.findall(r"https?://[\w./-]*hawkeyestate\.files\.com[\w./-]*", body)

 

            # Updated subject line check using regex

            if matches and approval_pattern.search(subject):

                message.Unread = False

                message.Save()

                print(f"Subject : {subject}")

                print(f"Received time : {received}")

                print(f"Link found : {matches}")

                return matches

 

        except Exception as e:

            print(f"Error processing emails: {e}")

     

       

           

    print(f"No Unread Email found with hawkeyestate Link")

    return None



open_outlook()

