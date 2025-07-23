from agents import function_tool
import os
import requests


#create a function to send a massage to whtsapp
@function_tool
def send_whatsapp_message(number: str, message: str):
    """
    use a ultra messsage api to send a custom messsage to the specific phone number and 
    return success message if the message send sucessefully and give error message if the message not send
    """

    instance_id = os.getenv("INSTANCE_ID")   
    token = os.getenv("Token")
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

    payload ={
       "token": token,
        "to": number,
        "body": message
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return f"Message sent successfully to {number}"
    else:
        return f"Failed to send message to. Error: {response.text}"