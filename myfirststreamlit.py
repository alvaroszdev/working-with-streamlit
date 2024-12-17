import streamlit as st 
import pandas as pd

st.write("hello world")

x = st.slider("x")
st.write(x,"squared is ", x*x)

mytext = st.text_input("your name",key ="name")
st.write(mytext)

df = pd.DataFrame(
    {
        "first colum":[1,2,3,4],
        "second colum":[10,20,30,40,],
    }
)

st.write(df)
