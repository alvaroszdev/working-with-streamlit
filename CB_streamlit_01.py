import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def get_df(high_limit,low_limit,x_size,y_size):

    df = pd.DataFrame(
        np.random.randint(
            low = -low_limit,
            high = high_limit,
            size = (x_size,y_size),
        ),
        columns= ("col %d" % i for i in range (y_size))
    )

    return df

s = st.sidebar.chat_input(placeholder="Your message",)
if s:
    st.sidebar.success(s)
st.image("https://fribell.com/wp-content/uploads/2022/03/logo-fribell-color.svg",use_container_width=20)
st.title ("streamlit basic") 
st.markdown("a brief project on streamlit widgets :sunglasses:")

empty_widget= st.empty()

generate_df=st.checkbox("generate df")
with st.expander("Data"):

    col1,col2,col3 = st.columns([3,6,2,])

    with col1:

        low_limit= st.slider(
            "low_limit",
            min_value=-100, 
            max_value=1000, 
            value=10, 
            step=1,
        )

        high_limit= st.slider(
            "high_limit",
            min_value=1000, 
            max_value=1000, 
            value=10, 
            step=1,
        )


        x_size= st.number_input(
            "x_size",
            min_value=1, 
            max_value=10**9, 
            value=10, 
            step=1,
        )

        y_size= st.number_input(
            "y_size",
            min_value=1, 
            max_value=10**9, 
            value=10, 
            step=1,
        )


    with col2:
        with st.spinner("Generate Dataframe..."):
            if generate_df:
       
                df = get_df(high_limit,low_limit, x_size,y_size)
                st.dataframe(df)
                empty_widget.write("Dataframe dimension %d x %d" % (df.shape))

    with col3:
        download_button = st.download_button(
        label="Download df", 
        data=df.to_csv(), 
        file_name="my dataframe.csv", 
        )

with st.expander("Metrics"):
    df_max = df.max().max()
    df_min = df.min().min()
    df_mean = df.mean().mean()

    metric_selection= st.multiselect(
        label="select metrict to sow", 
        options=["Max","Min","Average"],
        placeholder="Choose an option", 
    )

    if "Max" in metric_selection:
        st.metric(
            "Max value",
            df_max,
            delta = "Max",
            delta_color = "normal",
            help = "that max value of the DataFrame"
        )


    if "Min" in metric_selection:
        st.metric(
        "Min value",
        df_min,
        delta = "min",
        delta_color = "normal",
        help = "that min value of the DataFrame"
        )


    if "Average" in metric_selection:
        st.metric(
            "Mean value",
            df_mean,
            delta = None,
            delta_color = "normal",
            help = "that mean value of the DataFrame"
        )
with st.expander("Plots"):

    colorscale=st.selectbox(
        "choose color",
        options=[
    "viridis",    # Perceptualmente uniforme y ampliamente usado
        "plasma",     # Sequential, brillante
        "cividis",    # Sequential, accesible para personas con daltonismo
        "magma",      # Sequential, oscuro   # Diverging, transición de azul a rojo
        "Spectral",   # Diverging, brillante y diverso
        ]
    )
    options=["Matplotlib","plotly 2d","plotly 3d"],
    

    tab1,tab2,tab3=st.tabs(
        ["Matplotlib","plotly 2d","plotly 3d"]
    )


    with tab1:

        fig=plt.figure()
        contour = plt.contour(
            df,
            cmap=colorscale

        )
        plt.colorbar(contour)
        st.pyplot(fig)

    with tab2:

        fig= go.Figure(
            data = 
            go.Contour(
                z=df,
                colorscale=colorscale
            )
        )
        st.plotly_chart(fig)

    with tab3:

        fig= go.Figure(
            data = 
            go.Surface(
                z=df,
                colorscale=colorscale
            )
        )
        st.plotly_chart(fig)