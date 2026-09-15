import os
import msal
import webbrowser
import base64
import mimetypes
import requests
import json

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
MS_GRAPH_AUTHORITY_URL = "https://login.microsoftonline.com/consumers/"

def get_access_token(application_id: str, client_secret: str, scopes: list) -> str:
    client = msal.ConfidentialClientApplication(client_id=application_id, client_credential=client_secret, authority=MS_GRAPH_AUTHORITY_URL)

    # check if there is a refresh token stored

    refresh_token = None

    if os.path.exists("auth/refresh_token.txt"):
        with open("auth/refresh_token.txt", "r") as file:
            refresh_token = file.read().strip()
    
    else:
        if not os.path.exists("auth"):
            os.mkdir("auth")

    # try to acquire a new access token using the refresh token

    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token=refresh_token, scopes=scopes)

    # proceed with the authorization code flow if there is no refresh token

    else:
        auth_request_url = client.get_authorization_request_url(scopes=scopes)
        webbrowser.open(auth_request_url)
        authorization_code = input("[*] Provide the authorization code: ")
        
        if not authorization_code:
            raise ValueError(f"[-] The authorization code is blank. Please check.")
        
        token_response = client.acquire_token_by_authorization_code(code=authorization_code, scopes=scopes)

    # store the refresh token securely

    if "access_token" in token_response:
        with open("auth/refresh_token.txt", "w") as file:
            file.write(token_response.get("refresh_token"))

        return token_response.get("access_token")
    
    else:
        raise Exception(f"[-] The script is unable to acquire the access token either through refresh_token or authorization_code.")

def prepare_request_headers() -> dict:
    if os.getenv("APPLICATION_ID") != None or os.getenv("CLIENT_SECRET") != None:
        APPLICATION_ID = os.environ.get("APPLICATION_ID")
        CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
        SCOPES = ["User.Read", "Mail.ReadWrite", "Mail.Send"]     

    else:
        raise ValueError("The environment variables APPLICATION_ID and CLIENT_SECRET are not defined yet. Please configure.")
    
    access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)

    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

def prepare_attachment(path: str) -> dict:
    with open(path, "rb") as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")

    return {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": os.path.basename(path),
        "contentType": mimetypes.guess_type(path)[0],
        "contentBytes": encoded_content
    }

def send_message(to_recipients: list, subject_text: str, body_text: str, attachments: list = None) -> None:
    URL = f"{MS_GRAPH_BASE_URL}/me/sendMail"

    request_headers = prepare_request_headers()

    message = {
        "message": {
            "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in to_recipients],
            "subject": subject_text,
            "body": {
                "contentType": "HTML",
                "content": body_text
            }
        }
    }

    if attachments != None:
        message["message"]["attachments"] = [prepare_attachment(path) for path in attachments if os.path.exists(path)]

    response = requests.post(URL, headers=request_headers, data=json.dumps(message))

    if response.status_code != 202:
        raise Exception(f"[-] The script is unable to deliver the message to the recipients {tuple(to_recipients)}.")
    
    else:
        print(f"[+] The message has successfully been delivered by the script.")
