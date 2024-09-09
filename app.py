import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.card import card
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
st.set_page_config(layout="wide",page_title='RGNC Kartika')
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Kartika Damodara Month 2023")
    font_css = """
    <style>
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size: 24px;
    
    }
    button[data-baseweb="tab"] {
        margin-right: 30%; /* Adjust the value to control the space between tabs */
    }
    </style>
    """

    st.write(font_css, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Dashboard", "Excel"])
    vv_url = "https://docs.google.com/spreadsheets/d/1DEeRHNvakG8ZxjIfBdIvJOEUkJgryrqkOxeFBTLPnEM/edit#gid=0"
    kv_url = "https://docs.google.com/spreadsheets/d/1DEeRHNvakG8ZxjIfBdIvJOEUkJgryrqkOxeFBTLPnEM/edit#gid=1318636251"
    vg_url = "https://docs.google.com/spreadsheets/d/1DEeRHNvakG8ZxjIfBdIvJOEUkJgryrqkOxeFBTLPnEM/edit#gid=1647846290"
    rgnc_url = "https://docs.google.com/spreadsheets/d/1DEeRHNvakG8ZxjIfBdIvJOEUkJgryrqkOxeFBTLPnEM/edit#gid=272388271"
    conn = st.connection("gsheets", type=GSheetsConnection)
    #--------------- 1 Loading VV
    # vv = conn.read(worksheet="Vamsivat",usecols=list(range(13)))
    vv = conn.read(spreadsheet=vv_url,usecols=list(range(13)))
    new_cols=['Date','Sevaks','Lamps','Place','HousePrograms', 'Contacts', 'Books', 'Temples', 'Schools', 'Offices', 'Shops', 'Hospitals', 'Others']
    vv=vv.rename(columns=dict(zip(vv.columns,new_cols)))
    vv=vv.drop(0)
    vv=vv.fillna(0)
    vv.drop(vv[vv['Date'] == 0].index, inplace=True)
    #--------------- 2 Loading KV
    # kv = conn.read(worksheet="Kalpavriksha",usecols=list(range(14)))
    kv = conn.read(spreadsheet=kv_url,usecols=list(range(14)))
    new_cols=['Date','Sevaks','Lamps','Place','HousePrograms', 'Contacts', 'Books', 'Temples', 'Schools', 'Offices', 'Shops', 'Hospitals', 'Others','Apartments']
    kv=kv.rename(columns=dict(zip(kv.columns,new_cols)))
    kv=kv.drop(0)
    kv=kv.fillna(0)
    kv.drop(kv[kv['Date'] == 0].index, inplace=True)
    #--------------- 3 Loading VG
    # vg = conn.read(worksheet="Vrajagopis",usecols=list(range(13)))
    vg = conn.read(spreadsheet=vg_url,usecols=list(range(13)))
    new_cols=['Date','Sevaks','Lamps','Place','HousePrograms', 'Contacts', 'Books', 'Temples', 'Schools', 'Offices', 'Shops', 'Hospitals', 'Others']
    vg=vg.rename(columns=dict(zip(vg.columns,new_cols)))
    vg=vg.drop(0)
    vg=vg.fillna(0)
    vg.drop(vg[vg['Date'] == 0].index, inplace=True)
    #--------------- 4 Loading RGNC
    # rgnc = conn.read(worksheet="RGNC",usecols=list(range(14)))
    rgnc = conn.read(spreadsheet=rgnc_url,usecols=list(range(14)))
    rgnc=rgnc.fillna(0)
    rgnc=rgnc.drop(rgnc.columns[:3],axis=1)
    new_cols = ['Sector','Lamps','HousePrograms','Contacts','Books','Temples',"Schools",'Offices','Shops','Hospitals','Others']
    rgnc = rgnc.drop(0)
    rgnc=rgnc.rename(columns=dict(zip(rgnc.columns,new_cols)))
    rgnc = rgnc.drop([4,5,6])
    with tab2:
    #-------------- 5 Dropdown to display excel data from sidebar 
        selected_sheet = st.selectbox(
        "Click to view Excel Sheets",
        ("RGNC", "Vamsivat", "Kalpavriksha",'Vrajagopis'),
        index=None,
        placeholder="Select Sheet...",
        )
        if selected_sheet=='Vamsivat':
            st.header("Vamsivat")
            st.dataframe(vv)
        elif selected_sheet=='Kalpavriksha':
            st.header("Kalpavriksha")
            st.dataframe(kv)
        elif selected_sheet=='Vrajagopis':
            st.header("Vrajagopis")
            st.dataframe(vg)
        elif selected_sheet=='RGNC':
            st.header("RGNC")
            st.dataframe(rgnc)

    #----------------- 6 Overall Charts
    with tab1:
        rgnc['Lamps'] = rgnc.Lamps.astype('int')
        #progress bar and pie
        current_completion = rgnc.Lamps.sum()
        total_target = 25000
        completion_percentage = (current_completion / total_target) * 100
        col1, col2, col3 = st.columns(3)
        houses_covered=rgnc.HousePrograms.sum()
        unq_places = pd.concat([vv.Place,kv.Place,vg.Place])
        with col1:
            c1=card(
                title=f"{current_completion}",
                text="Unique Souls Offered",
                image="https://i.pinimg.com/originals/5e/c1/2e/5ec12ebb5ab4b57812cfdf2cb31fd9e7.jpg",
                on_click=lambda: print("Clicked!")
            )
        with col2:
            c2=card(
                title=f"{int(houses_covered)}",
                text="Unique Houses Covered  ",
                image="https://i.pinimg.com/originals/5e/c1/2e/5ec12ebb5ab4b57812cfdf2cb31fd9e7.jpg",
                on_click=lambda: print("Clicked!")
            )
        with col3:
            c3=card(
                title=f"{len(unq_places)}",
                text="Unique Locations Covered",
                image="https://i.pinimg.com/originals/5e/c1/2e/5ec12ebb5ab4b57812cfdf2cb31fd9e7.jpg",
                on_click=lambda: print("Clicked!")
            )
        st.divider()

        col1, col2 = st.columns(2)
        progress_value = min(completion_percentage / 100, 1.0)
        st.progress(progress_value)
        st.header(f"Completion: {completion_percentage:.2f}%")
        with col1:
            st.header("Locations Covered")
            total_homes = pd.concat([vv.iloc[:, 4:], kv.iloc[:, 4:], vg.iloc[:, 4:]])
            temp = total_homes.sum().apply(pd.to_numeric, errors='coerce')
            temp = temp.dropna()
            top = temp.nlargest(5)
            fig = px.pie(
                values=top.values, 
                names=top.index,
                hole=0.6,
                title='Locations Visited',
                color_discrete_sequence=['skyBlue', 'mediumPurple', 'cornflowerblue', 'cyan', 'dodgerblue'] 
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)

        with col2:
            st.header("How much have we completed?")
            fig = px.pie(
                values=[current_completion, total_target - current_completion], 
                names=['Completed', 'Remaining'],
                hole=0.6,
                title='Completion Progress'
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)


        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            # timeline date vs lamps
            vv_date_lamps = vv[['Date', 'Lamps']].copy()
            vv_date_lamps.loc[:, 'Date'] = pd.to_datetime(vv_date_lamps['Date'], format='%d-%m-%y')
        
            kv_date_lamps = kv[['Date', 'Lamps']].copy()
            kv_date_lamps.loc[:, 'Date'] = pd.to_datetime(kv_date_lamps['Date'], format='%d-%m-%y')
        
            vg_date_lamps = vg[['Date', 'Lamps']].copy()
            vg_date_lamps.loc[:, 'Date'] = pd.to_datetime(vg_date_lamps['Date'], format='%d-%m-%y')
        
            # Combine dataframes
            combined_dates_lamps = pd.concat([vv_date_lamps, kv_date_lamps, vg_date_lamps], ignore_index=True)
        
            # Convert 'Date' column back to string format for consistency
            combined_dates_lamps.loc[:, 'Date'] = combined_dates_lamps['Date'].dt.strftime('%d-%m-%y')
            combined_dates_lamps.loc[:, 'Lamps'] = combined_dates_lamps['Lamps'].astype('int')
        
            # Group by 'Date' and sum the 'Lamps'
            overall_date_lamps = combined_dates_lamps.groupby('Date').sum().reset_index()
        
            # Convert 'Date' back to datetime for sorting
            overall_date_lamps.loc[:, 'Date'] = pd.to_datetime(overall_date_lamps['Date'], format='%d-%m-%y')
            overall_date_lamps = overall_date_lamps.sort_values(by='Date', ascending=True)
        
            # Prepare x values for plotting
            xval = overall_date_lamps['Date'].dt.strftime('%d-%m-%Y')
        
            # Plot the timeline of lamps offered
            fig = px.line(overall_date_lamps, x=xval, y='Lamps', labels={'Lamps': 'Number of Lamps'}, title='Timeline of Lamps Offered')
            fig.update_traces(mode='markers+lines', marker=dict(size=10))  # Add markers (bubbles) on top
            fig.update_xaxes(type='category', tickformat='%d-%m-%Y', tickangle=45, title_text='Date')
            fig.update_yaxes(tickfont=dict(size=16))
            fig.update_layout(
                title=dict(text='Timeline of Lamps Offered', font=dict(size=24)),  # Increase title font size to 24
                xaxis=dict(title=dict(font=dict(size=18))), 
                yaxis=dict(title=dict(font=dict(size=18)))  # Adjust label font size
            )
            st.plotly_chart(fig)

            # vv_date_lamps = vv[['Date', 'Lamps']] ; vv_date_lamps['Date'] = pd.to_datetime(vv_date_lamps['Date'])
            # kv_date_lamps = kv[['Date', 'Lamps']] ; kv_date_lamps['Date'] = pd.to_datetime(kv_date_lamps['Date'])
            # vg_date_lamps = vg[['Date', 'Lamps']] ; vg_date_lamps['Date'] = pd.to_datetime(vg_date_lamps['Date'])

            # vv_date_lamps.Lamps = vv_date_lamps.Lamps.astype('int')
            # kv_date_lamps.Lamps = kv_date_lamps.Lamps.astype('int')
            # vg_date_lamps.Lamps = vg_date_lamps.Lamps.astype('int')

            # combined_dates_lamps = pd.concat([vv_date_lamps, kv_date_lamps, vg_date_lamps], ignore_index=True)
            # overall_date_lamps = combined_dates_lamps.groupby('Date').sum().reset_index()
            # overall_date_lamps['Date'] = pd.to_datetime(overall_date_lamps['Date'])
            # overall_date_lamps = overall_date_lamps.sort_values(by='Date', ascending=True)
            # # print(overall_date_lamps.Date)
            
            # xval = overall_date_lamps['Date'].dt.strftime('%d-%m-%Y')
            # xval = pd.to_datetime(xval, format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
            # fig = px.line(overall_date_lamps, x=overall_date_lamps['Date'], y='Lamps', labels={'Lamps': 'Number of Lamps'}, title='Timeline of Lamps Offered')
            # fig.update_traces(mode='markers+lines', marker=dict(size=10))  # Add markers (bubbles) on top
            # fig.update_xaxes(type='category', tickformat='%d-%m-%Y', tickangle=45, title_text='Date', tickfont=dict(size=16))  # Set x-axis label to 'Date' and adjust tick font size
            # fig.update_yaxes(tickfont=dict(size=16))  # Adjust y-axis tick font size
            # fig.update_layout(
            #     title=dict(text='Timeline of Lamps Offered', font=dict(size=24)),  # Increase title font size to 24
            #     xaxis=dict(title=dict(font=dict(size=18))), yaxis=dict(title=dict(font=dict(size=18)))  # Adjust label font size
            # )
            # st.plotly_chart(fig)

        with col2:
        # sector vs lamps
            fig = px.bar(rgnc, x='Sector', y='Lamps', labels={'Lamps': 'Number of Lamps'}, title='Lamps per Sector')
            fig.update_layout(
                xaxis_title='Sector',
                yaxis_title='Number of Lamps',
                barmode='group',  
                width=800,  # Set the width of the chart
                margin=dict(l=50, r=50, t=30, b=30), 
                title=dict(text='Lamps per Sector', font=dict(size=24)),  # Increase title font size to 24
            )

            colors = [['skyBlue', 'mediumPurple', 'cornflowerblue']] 
            for i, bar in enumerate(fig.data):
                bar.marker.color = colors[i]
            
            bar_width = 0.4
            for bar in fig.data:
                bar.update(width=bar_width)
                bar.marker.line.color = 'black'  
                bar.marker.line.width = 1.5

            # Increase size of x-axis and y-axis labels and ticks
            fig.update_xaxes(tickfont=dict(size=14), title_font=dict(size=18))
            fig.update_yaxes(tickfont=dict(size=14), title_font=dict(size=18))

            st.plotly_chart(fig)




        st.divider()
        footer = """<div style="text-align: center;">
                <a href="https://visitorbadge.io/status?path=https%3A%2F%2Frgnc-kartika-2023.streamlit.app%2F">
                    <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Frgnc-kartika-2023.streamlit.app%2F&label=ThankYouforVisiting&labelColor=%232ccce4&countColor=%23263759&style=flat-square" />
                </a>
            </div>"""
        st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
