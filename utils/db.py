import os
from supabase import create_client
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("⚠️ Configure SUPABASE_URL e SUPABASE_KEY no .env ou Secrets do Streamlit Cloud.")
        st.stop()

    return create_client(url, key)


def fetch_table(table, filters=None, order=None):
    supabase = get_supabase()
    q = supabase.table(table).select("*")
    if filters:
        for k, v in filters.items():
            q = q.eq(k, v)
    if order:
        q = q.order(order)
    return q.execute().data


def insert_row(table, data):
    supabase = get_supabase()
    return supabase.table(table).insert(data).execute().data


def update_row(table, match, data):
    supabase = get_supabase()
    q = supabase.table(table).update(data)
    for k, v in match.items():
        q = q.eq(k, v)
    return q.execute().data


def delete_row(table, match):
    supabase = get_supabase()
    q = supabase.table(table).delete()
    for k, v in match.items():
        q = q.eq(k, v)
    return q.execute().data
