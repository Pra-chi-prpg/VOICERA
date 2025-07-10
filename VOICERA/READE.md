This project lets you create an **AI-powered outbound voice call** using:
- **Twilio** for calling
- **Groq's LLaMA 3** for conversational AI
- **FastAPI** as the backend server
- **gTTS** for converting text to speech
- **Ngrok** to expose localhost for Twilio

## feature
- Initiates an outbound call using Twilio
- Captures user speech and converts it to text(viaTwilio)
- Sends the text to Groq's LLaMA 3 model via API
- Converts the AI response to speech using gTTS
- Responds on the call dynamically

voiceAI/
├── app.py # FastAPI server
├── make_call.py # Triggers outbound call
├── groq_utils.py # Groq + gTTS utility functions
├── hdfc_credit_card.pdf
├── static/ # Stores generated MP3 files
│ └── response.mp3
├── templates/
│ └── twiml.xml # Twilio XML response template
├── requirements.txt
└── README.md
