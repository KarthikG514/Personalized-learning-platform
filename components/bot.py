from flask import Flask, jsonify, request, Blueprint
import google.generativeai as genai

bot_routes = Blueprint('bot', __name__)  # ✅ Fix: Corrected __name__

# ✅ Configure API with the correct model
genai.configure(api_key="AIzaSyCtiWcnSlUXhReWGZl0kepja4-OX7k_r5w")
model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Use the correct model
chat = model.start_chat(history=[])

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=False)  # 🔧 Disable streaming
        return response.text.strip()
    except Exception as e:
        print(f"Error in Gemini API: {e}")
        return None

@bot_routes.route('/ask-chat', methods=['POST'])
def ollama_chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Invalid request data"}), 400
        
        user_input = data.get('prompt')

        if user_input.lower() == 'quit':
            return jsonify({"response": "Exiting the chatbot. Goodbye!"})

        response_text = get_gemini_response(user_input)

        if not response_text:
            return jsonify({"error": "No response from AI"}), 500

        return jsonify({"response": response_text})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
