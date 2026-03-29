from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# ── SCOPES ──────────────────────────────────────────────────────────────────
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
]

client = OpenAI(api_key=api_key)

# ── GOOGLE AUTH ──────────────────────────────────────────────────────────────
def get_google_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return creds

# ── GMAIL TOOLS ──────────────────────────────────────────────────────────────
def read_emails(max_results=5):
    try:
        creds = get_google_creds()
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
                metadataHeaders=['From','Subject','Date']).execute()
            headers = {h['name']: h['value'] for h in m['payload']['headers']}
            emails.append({
                'id': msg['id'],
                'from': headers.get('From',''),
                'subject': headers.get('Subject',''),
                'date': headers.get('Date',''),
                'snippet': m.get('snippet','')
            })
        return json.dumps(emails, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

def send_email(to: str, subject: str, body: str):
    try:
        creds = get_google_creds()
        service = build('gmail', 'v1', credentials=creds)
        message_text = f"To: {to}\nSubject: {subject}\n\n{body}"
        raw = base64.urlsafe_b64encode(message_text.encode()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return json.dumps({"status": "Email sent successfully", "to": to, "subject": subject})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ── CALENDAR TOOLS ───────────────────────────────────────────────────────────
def get_upcoming_events(max_results=5):
    try:
        creds = get_google_creds()
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        result = []
        for e in events:
            start = e['start'].get('dateTime', e['start'].get('date'))
            result.append({'title': e.get('summary','No title'), 'start': start,
                          'location': e.get('location',''), 'description': e.get('description','')})
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

def create_event(title: str, start_datetime: str, end_datetime: str, description: str = ""):
    try:
        creds = get_google_creds()
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': title,
            'description': description,
            'start': {'dateTime': start_datetime, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_datetime, 'timeZone': 'Asia/Kolkata'},
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return json.dumps({"status": "Event created", "link": event.get('htmlLink')})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ── TOOL DEFINITIONS ─────────────────────────────────────────────────────────
tools = [
    {"type": "function", "function": {
        "name": "read_emails",
        "description": "Read recent emails from Gmail inbox",
        "parameters": {"type": "object", "properties": {
            "max_results": {"type": "integer", "description": "Number of emails to fetch", "default": 5}
        }, "required": []}
    }},
    {"type": "function", "function": {
        "name": "send_email",
        "description": "Send an email via Gmail",
        "parameters": {"type": "object", "properties": {
            "to": {"type": "string", "description": "Recipient email address"},
            "subject": {"type": "string", "description": "Email subject"},
            "body": {"type": "string", "description": "Email body text"}
        }, "required": ["to", "subject", "body"]}
    }},
    {"type": "function", "function": {
        "name": "get_upcoming_events",
        "description": "Get upcoming calendar events",
        "parameters": {"type": "object", "properties": {
            "max_results": {"type": "integer", "description": "Number of events", "default": 5}
        }, "required": []}
    }},
    {"type": "function", "function": {
        "name": "create_event",
        "description": "Create a calendar event",
        "parameters": {"type": "object", "properties": {
            "title": {"type": "string"},
            "start_datetime": {"type": "string", "description": "ISO format: 2026-03-28T10:00:00"},
            "end_datetime": {"type": "string", "description": "ISO format: 2026-03-28T11:00:00"},
            "description": {"type": "string"}
        }, "required": ["title", "start_datetime", "end_datetime"]}
    }},
]

tool_map = {
    "read_emails": read_emails,
    "send_email": send_email,
    "get_upcoming_events": get_upcoming_events,
    "create_event": create_event,
}

# ── AGENT LOOP ───────────────────────────────────────────────────────────────
def run_agent(user_message: str, history: list):
    messages = [
        {"role": "system", "content": (
            "You are a smart personal assistant with access to Gmail and Google Calendar. "
            "Help the user manage their emails and schedule. Today is " + datetime.now().strftime("%A, %d %B %Y") + ". "
            "When asked about emails or events, always use the tools. Be concise and helpful."
        )}
    ] + history + [{"role": "user", "content": user_message}]

    steps = []
    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto"
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content, steps

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            args = json.loads(tc.function.arguments)
            steps.append(f"🔧 Calling **{fn_name}** with `{args}`")
            result = tool_map[fn_name](**args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            steps.append(f"✅ Got result from **{fn_name}**")

# ── STREAMLIT UI ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Agent 1 — Basic Agent", page_icon="🤖", layout="centered")
st.title("🤖 Agent 1 — Basic Agent")
st.caption("Gmail + Google Calendar access via GPT-4o-mini")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask me about your emails or calendar..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent is working..."):
            reply, steps = run_agent(prompt, st.session_state.history)
        if steps:
            with st.expander("🔍 Agent Steps", expanded=False):
                for s in steps:
                    st.markdown(s)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": reply})
