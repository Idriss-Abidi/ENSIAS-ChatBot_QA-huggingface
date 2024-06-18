import streamlit as st

try:
    from transformers import pipeline
except ImportError:
    st.error("Error: Unable to import transformers package. Please make sure it is installed.")
    st.stop()

def main():
    st.image("C:\\Users\\ADMIN\\Desktop\\PFA\\PFA2\\logo.jpg", width=200) 
    st.title("Ask Ensias Chatbot")

    # Initialize the QA pipeline
    qa_model = pipeline("question-answering", model='deepset/roberta-base-squad2')

    #The context
    context = """ENSIAS, the National School of Computer Science and Systems Analysis, is a premier engineering institution located in Rabat, Morocco. 
    Founded in 1992, ENSIAS offers a diverse range of undergraduate and graduate programs covering computer science, information technology, and systems analysis. 
    With nine distinct study fields available to engineering students, ENSIAS provides a tailored educational experience catering to various interests and career paths. 
    These study fields include GL, IDSIT, IDF, BI&A, GD, 2IA, SSI, 2SCL, and SSE. 
    These study fields are Business Intelligence & Analytics (BI&A), Data Engineering (GD), Software Engineering (GL), Engineering in Data Science and IoT (IDSIT), Digital Engineering for Finance (IDF), Artificial Intelligence Engineering (2IA), Information Systems Security (SSI), Smart Supply Chain & Logistics (2SCL), and Smart System Engineering (SSE). 
    Admission to ENSIAS is highly competitive and is determined by performance in the national entrance exam for engineering schools in Morocco. 
    Under the leadership of Ms. Ilham Berrada, who assumed the role of director in 2020, the school remains dedicated to fostering innovation, diversity, and excellence in education and research."""


    # Initialize chat 
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # user input
    if prompt := st.chat_input("Ask your question about ENSIAS:"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response from the pipeline
        result = qa_model(question=prompt, context=context)
        response = result['answer']
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear button
    if st.button("Clear"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
