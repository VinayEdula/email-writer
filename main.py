from langchain import PromptTemplate
import streamlit as st
from langchain.llms import OpenAI

query_template = """
    Below is an email that may be unstructured and poorly worded.
    Your goal is to:
    - Format the email properly
    - Convert the input email into the tone specified in curly braces. 
    - Convert the input email into the dialect specified in curly braces.

    Take these examples of different tones as reference:
    - Formal: We went to Hyderabad for the weekend. We have a lot of things to tell you.
    - Informal: Went to Hyderabad for the weekend. Lots to tell you.  

    Below are some examples of words in different dialects:
    - American: Garbage, cookie, green thumb, parking lot, pants, windshield, French Fries, cotton candy, apartment
    - British: Green fingers, car park, trousers, windscreen, chips, candyfloss, flag, rubbish, biscuit

    Example Sentences from each dialect:
    - American: As they strolled through the colorful neighborhood, Sarah asked her friend if he wanted to grab a coffee at the nearby café. The fall foliage was breathtaking, and they enjoyed the pleasant weather, chatting about their weekend plans.
    - British: As they wandered through the picturesque neighbourhood, Sarah asked her friend if he fancied getting a coffee at the nearby café. The autumn leaves were stunning, and they savoured the pleasant weather, chatting about their weekend plans.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""


prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=query_template,
)


def loadLanguageModel(api_key_openai):
    llm = OpenAI(temperature=.7, openai_api_key=api_key_openai)
    return llm


st.set_page_config(page_title="Professional Email Writer", page_icon=":robot:")
st.header("Professional Email Writer")

column1, column2 = st.columns(2)


st.markdown("## Enter Your Sample Email Text To Convert")


def fetchAPIKey():
    input_text = st.text_input(
        label="OpenAI API Key ",  placeholder="Ex: vk-Cb8un42twmA8tf...", key="openai_api_key_input")
    return input_text


openai_api_key = fetchAPIKey()

column1, column2 = st.columns(2)
with column1:
    tone_drop_down = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))

with column2:
    dialect_drop_down = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))


def getEmail():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed',
                              placeholder="Your Email...", key="input_text")
    return input_text


input_text = getEmail()

if len(input_text.split(" ")) > 700:
    st.write("Maximum limit is 700 words. Please enter a shorter email")
    st.stop()


def textBoxUpdateWithExample():
    print("in updated")
    st.session_state.input_text = "Vinay I am starts work at yours office from monday"


st.button("*Show an Example*", type='secondary',
          help="Click to see an example of the email you will be converting.", on_click=textBoxUpdateWithExample)
st.markdown("### Your Email:")

if input_text:
    if not openai_api_key:
        st.warning(
            'Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()
    llm = loadLanguageModel(api_key_openai=openai_api_key)
    prompt_with_email = prompt.format(
        tone=tone_drop_down, dialect=dialect_drop_down, email=input_text)
    formatted_email = llm(prompt_with_email)
    st.write(formatted_email)
