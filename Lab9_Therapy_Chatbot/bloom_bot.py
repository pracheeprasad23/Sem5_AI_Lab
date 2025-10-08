import streamlit as st
from google import genai
from google.genai import types

# ✅ Initialize Gemini client with your API key directly
client = genai.Client(api_key="###")  # <-- paste your key here!

MODEL = "gemini-2.5-flash"

def generate_bot_reply(age_group: str, user_message: str, history: list[dict]):
    contents = []
    for turn in history:
        contents.append(types.Content(
            role=turn["role"],
            parts=[types.Part(text=turn["text"])]
        ))
    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=f"(Age group: {age_group}) {user_message}")]
    ))

    response = client.models.generate_content(model=MODEL, contents=contents)
    reply = response.candidates[0].content.parts[0].text
    return reply


def main():
    st.set_page_config(page_title="BloomBot 🌼", layout="centered")
    st.markdown("<h1 style='text-align:center; color:#9370DB;'>🌼 BloomBot 🌼</h1>", unsafe_allow_html=True)
    st.write("Hey there! I’m BloomBot — your kind and gentle chatbot 💜 (Note: I’m just a bot, not a therapist.)")

    # Sidebar age selection
    age = st.sidebar.selectbox("Select your age group 🌈", ["Under 13", "13–18", "19–25", "26+"])

    # Store chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("### 💬 Quick Boosts")
    c1, c2, c3 = st.columns(3)
    if c1.button("Make me laugh 😂"):
        st.write("Why did the math book look sad? Because it had too many problems 😆")
    if c2.button("Say something nice 💖"):
        st.write("You light up the world in your own quiet way ✨")
    if c3.button("Give me motivation ⚡"):
        st.write("It’s okay to go slow. What matters is you’re still moving 🌱")

    # Chat area
    st.markdown("### 💭 Talk to BloomBot")
    user_input = st.text_input("You:", key="input")

    if user_input:
        st.session_state.history.append({"role": "user", "text": user_input})
        reply = generate_bot_reply(age, user_input, st.session_state.history)
        st.session_state.history.append({"role": "assistant", "text": reply})
        st.markdown(f"**BloomBot:** {reply}")

    # Chat history expander
    with st.expander("Show chat history"):
        for turn in st.session_state.history:
            if turn["role"] == "user":
                st.markdown(f"**You:** {turn['text']}")
            else:
                st.markdown(f"**BloomBot:** {turn['text']}")

    st.markdown("---")
    st.caption("BloomBot is a supportive AI bot made with Streamlit + Gemini 💜")


if __name__ == "__main__":
    main()
