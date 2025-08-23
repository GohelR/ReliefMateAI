import streamlit as st

st.set_page_config(page_title="ReliefMate AI", page_icon="🆘", layout="wide")

st.title("🆘 ReliefMate AI")
st.subheader("Your Disaster Relief Assistant")

st.markdown("""Welcome to **ReliefMate AI**, a smart assistant designed to provide disaster relief guidance and connect communities with essential resources. 🚑🌍""")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "💬 Chat Assistant", "📍 Resources", "ℹ️ About"])

if page == "🏠 Home":
    st.image("https://source.unsplash.com/1200x400/?disaster,help", use_container_width=True)
    st.write("This platform helps people find support, share updates, and access relief resources during disasters.")

elif page == "💬 Chat Assistant":
    st.header("💬 Ask ReliefMate")
    user_query = st.text_input("Type your question:")
    if user_query:
        st.success(f"🤖 ReliefMate AI says: We are processing your query about '{user_query}' and will guide you soon!")

elif page == "📍 Resources":
    st.header("📍 Relief Resources")
    st.write("✅ Emergency Helplines\n✅ Shelter Locations\n✅ Food & Medical Aid\n✅ Volunteer Info")

elif page == "ℹ️ About":
    st.header("ℹ️ About ReliefMate")
    st.write("ReliefMate AI is built to assist communities during natural disasters with quick information and AI-powered support.")

st.markdown('---')
st.caption("Made with ❤️ by ReliefMate Team")
