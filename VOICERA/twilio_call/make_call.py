from twilio.rest import Client


account_sid = "AC5fed3########################"
auth_token = "68c374cad615c6###################"

client = Client(account_sid, auth_token)
call = client.calls.create(
    url= "https://51454ccf829a.ngrok-free.app/voice", 
    to="+91977########",                   
    from_="+13412374779",
    method="POST"                   
)

print(f"Call initiated: {call.sid}")
