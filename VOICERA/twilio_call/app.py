
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langdetect import detect
from groq_utils import get_answer_from_pdf, translate_to_hindi, convert_to_speech
prompt ="Convince the caller to sign up for a credit card(HDFC).Tell this in frendly way and provide all the details of credit card."

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.api_route("/voice", methods=["GET", "POST"])
async def voice(request: Request):
    try:
        if request.method == "GET":
            ai_text = "Welcome to HDFC Credit Card Assistant."
            voice = "en-IN-NeerjaNeural"
        else:
            form = await request.form()
            user_input = form.get("SpeechResult", "").strip()
            print(f"\n [User Question] {user_input}")

            
            is_hindi = False
            try:
                is_hindi = detect(user_input) == "hi"
            except Exception as e:
                print(f"[LangDetect Error] {e}")


            ai_text = await get_answer_from_pdf(user_input)

            
            voice = "en-IN-NeerjaNeural"
            if is_hindi:
                ai_text = await translate_to_hindi(ai_text)
                voice = "hi-IN-SwaraNeural"

            print(f" [AI Answer] {ai_text}")

        mp3_url = await convert_to_speech(ai_text, voice=voice)

        return templates.TemplateResponse(
            "twiml.xml",
            {"request": request, "mp3_url": mp3_url},
            media_type="application/xml"
        )

    except Exception as e:
        print(f"[ ERROR in /voice] {e}")
        return Response(
            content="<Response><Say>Something went wrong. Please try again.</Say></Response>",
            media_type="application/xml"
        )
