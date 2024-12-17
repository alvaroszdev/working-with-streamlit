import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

@st.cache_data
def get_df(high_limit, low_limit, x_size, y_size):
    stime = time.time()
    st.session_state["df"] = pd.DataFrame(
        np.random.randint(
            low=-low_limit,
            high=high_limit,
            size=(x_size, y_size),
        ),
        columns=("col %d" % i for i in range(y_size))
    )
    compute_time = time.time() - stime
    return compute_time

@st.dialog("Data generation")
def dialog_compute():
    st.write("Do you want to compute data")

    yes = st.button("Yes")

    if yes:
        st.session_state["compute"] = True
        st.rerun()

st.set_page_config(
    page_title="FRIBELL - Streamlit", 
    page_icon= "🧴",
    layout="wide",
    initial_sidebar_state="expanded", 
    menu_items=None
    )


# Initialization
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

if 'compute' not in st.session_state:
    st.session_state['compute'] = False

s = st.sidebar.chat_input(placeholder="Your message")
if s:
    st.sidebar.success(s)

def page1():
    st.image("https://fribell.com/wp-content/uploads/2022/03/logo-fribell-color.svg", use_container_width=20)
    st.title("streamlit basic")
    st.markdown("a brief project on streamlit widgets :sunglasses:")

def page2():
    empty_widget = st.empty()
    empty_widget2 = st.empty()
    generate_df = st.checkbox("generate df")

    if generate_df:
        with st.expander("Data"):
            col1, col2, col3 = st.columns([3, 6, 2])

            with col1:
                with st.form("compute_form"):
                    low_limit = st.slider(
                        "low_limit",
                        min_value=-100,
                        max_value=1000,
                        value=10,
                        step=1,
                    )

                    high_limit = st.slider(
                        "high_limit",
                        min_value=1000,
                        max_value=1000,
                        value=10,
                        step=1,
                    )

                    x_size = st.number_input(
                        "x_size",
                        min_value=1,
                        max_value=10**9,
                        value=10,
                        step=1,
                    )

                    y_size = st.number_input(
                        "y_size",
                        min_value=1,
                        max_value=10**9,
                        value=10,
                        step=1,
                    )

                    submitted = st.form_submit_button("Submit")
                if submitted:
                    dialog_compute()

            with col2:
                if st.session_state["compute"]:
                    with st.spinner("Generate Dataframe..."):
                        compute_time = get_df(high_limit, low_limit, x_size, y_size)
                        st.dataframe(st.session_state["df"])
                        empty_widget.write("Dataframe dimension %d x %d" % (st.session_state["df"].shape))
                        empty_widget2.write("The computation time is %.3f " % compute_time)

            with col3:
                download_button = st.download_button(
                    label="Download df",
                    data=st.session_state["df"].to_csv(),
                    file_name="my dataframe.csv",
                )

        with st.expander("Metrics"):
            df_max = st.session_state["df"].max().max()
            df_min = st.session_state["df"].min().min()
            df_mean = st.session_state["df"].mean().mean()

            metric_selection = st.multiselect(
                label="select metric to show",
                options=["Max", "Min", "Average"],
                placeholder="Choose an option",
            )

            if "Max" in metric_selection:
                st.metric(
                    "Max value",
                    df_max,
                    delta="Max",
                    delta_color="normal",
                    help="the max value of the DataFrame"
                )

            if "Min" in metric_selection:
                st.metric(
                    "Min value",
                    df_min,
                    delta="min",
                    delta_color="normal",
                    help="the min value of the DataFrame"
                )

            if "Average" in metric_selection:
                st.metric(
                    "Mean value",
                    df_mean,
                    delta=None,
                    delta_color="normal",
                    help="the mean value of the DataFrame"
                )

        with st.expander("Plots"):
            colorscale = st.selectbox(
                "choose color",
                options=[
                    "viridis",
                    "plasma",
                    "cividis",
                    "magma",
                    "Spectral",
                ]
            )

            tab1, tab2, tab3 = st.tabs([
                "Matplotlib", "plotly 2d", "plotly 3d"
            ])

            with tab1:
                fig = plt.figure()
                contour = plt.contour(
                    st.session_state["df"],
                    cmap=colorscale
                )
                plt.colorbar(contour)
                st.pyplot(fig)

            with tab2:
                fig = go.Figure(
                    data=go.Contour(
                        z=st.session_state["df"],
                        colorscale=colorscale
                    )
                )
                st.plotly_chart(fig)

            with tab3:
                fig = go.Figure(
                    data=go.Surface(
                        z=st.session_state["df"],
                        colorscale=colorscale
                    )
                )
                st.plotly_chart(fig)

pg = st.navigation(
    {
        "Home": [st.Page(page1, title="Intro", icon="🔥")],
        "Data": [st.Page(page2, title="Data & Plots", icon="🏋️‍♂️")],
    }
)
pg.run()
