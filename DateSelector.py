import streamlit as st
import datetime


def event(tab):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    c1,c2 = tab.columns(2)
    start_date = c1.date_input('Start date', today)
    end_date = c2.date_input('End date', tomorrow)
    if start_date < end_date:
        tab.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
    else:
        tab.error('Error: End date must fall after start date.')