import streamlit as st

from main import insert
from main import retrieve

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('Reminiscence to Rescue (R2R)')

with st.sidebar:
    with st.container(border=True):
        selected_dataset = st.radio(
            "Please select from below operations:",
            ("Manage Parameters", "Store Private key", "Retrieve Private Key"),
            captions=["To change parameters like bloom filter size, hash function, etc",
                      "To store private key into bloom filter", "To retrieve private key from bloom filter"]
        )

questions = []
hash_count = 0
size = 0
hash_function = "SHA256"
sq_count = 3

if 'hash_count_ph' not in st.session_state:
    st.session_state.hash_count_ph = 0

if 'size_ph' not in st.session_state:
    st.session_state.size_ph = 0

if 'hash_function_ph' not in st.session_state:
    st.session_state.hash_function_ph = "SHA256"

if 'sq_count_ph' not in st.session_state:
    st.session_state.sq_count_ph = 0

if 'question_ph' not in st.session_state:
    st.session_state.question_ph = []

if 'insertion_time' not in st.session_state:
    st.session_state.insertion_time = 0

if 'retrieval_time' not in st.session_state:
    st.session_state.retrieval_time = 0

if selected_dataset == 'Manage Parameters':
    st.write(
        "Disclaimer: You can choose to update below fields. If no values are updated, default values are "
        "considered.")
    # st.text_input("Number of hash functions", placeholder="0", key="hash_count", value=0)
    # st.text_input("Size of bloom filter in bits", placeholder="0", key="size", value=0)
    st.selectbox(
        'Choose hash function',
        (
            'SHA256', 'SHA512'),
        key="hash_function", placeholder="SHA256")
    st.selectbox(
        'Choose number of security questions (minimum three)',
        (
            '5', '6', '7', '8', '9', '10', '11', '12'),
        key="sq_count")

    # st.session_state.hash_count_ph = int(st.session_state.hash_count)
    # st.session_state.size_ph = int(st.session_state.size)

    st.session_state.hash_count_ph = 0
    st.session_state.size_ph = 0
    st.session_state.hash_function_ph = st.session_state.hash_function
    st.session_state.sq_count_ph = int(st.session_state.sq_count)

if selected_dataset == 'Store Private key':
    answers = []
    hash_count = int(st.session_state.hash_count_ph)
    size = int(st.session_state.size_ph)
    hash_function = st.session_state.hash_function_ph
    sq_count = int(st.session_state.sq_count_ph)

    for i in range(sq_count):
        questions.append(st.selectbox(
            'Choose your security question:',
            (
                'Last ten lines from your favourite song from the Beatles band',
                'The second paragraph on page 34 from your favourite book',
                'First five lines about your favourite place from wikipedia',
                'Your favourite quote from your favourite person',
                'Ten lines from your favourite article in your school magazine',
                'Latitude and longitude of your first travel destination',
                'The name of the first award you received in your childhood',
                'Ten lines of your favourite recipe from your favourite chef',
                'Third last about your favourite sport person from wikipedia',
                'First eight lines from the first movie of your favourite director ',
                'Latitude and longitude of your favourite historical place',
                'Last five lines about your favourite fictional character in their book'
            ),
            key="sq" + str(i + 1)))
        answers.append(st.text_input("Enter your answer", placeholder="", key="sqa" + str(i + 1)))

    private_key = st.text_input("Enter your private key", placeholder="1100111......")

    st.button("Submit", type="primary", on_click=insert,
              args=[private_key, answers, hash_count, size, hash_function])
    st.text_area(label="", height=1000, placeholder="Bloom filter bits will be shown here...", key="bit_array")

    st.session_state.question_ph = questions
    st.write("Time taken to store into bloom filter:" + str(st.session_state.insertion_time) + " milliseconds")

elif selected_dataset == 'Retrieve Private Key':
    answers = []

    for i in range(len(st.session_state.question_ph)):
        st.text("Question " + str(i + 1) + ". " + st.session_state.question_ph[i])
        answers.append(st.text_input("Enter your answer", placeholder="", key="sqa_retrieval" + str(i + 1)))

    st.button("Submit", type="primary", on_click=retrieve, args=[answers])

    st.text_area(label="", height=500, placeholder="Retrieved private key will be shown here... ", key="bit_array")
    st.write("Time taken to retrieve from bloom filter:" + str(st.session_state.retrieval_time) + " milliseconds")
