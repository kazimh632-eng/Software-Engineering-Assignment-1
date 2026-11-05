import requests
import streamlit as st

API = 'http://127.0.0.1:5001'
st.set_page_config(page_title='Student Manager', page_icon='🎓')
st.title('Student Management')

def refresh(): st.rerun()
def show_error(response):
    if not response.ok: st.error(response.json().get('error', response.text))

try:
    response = requests.get(f'{API}/students', timeout=3)
    response.raise_for_status()
    students = response.json()
except requests.RequestException:
    st.error('API connect nahi ho rahi. Pehle app.py server chalao.')
    st.stop()

st.subheader('All students')
st.dataframe(students, use_container_width=True, hide_index=True)

with st.expander('Add student'):
    with st.form('add'):
        name=st.text_input('Name'); department=st.text_input('Department'); email=st.text_input('Email')
        if st.form_submit_button('Add'):
            r=requests.post(f'{API}/students', json={'name':name,'department':department,'email':email})
            if r.ok: st.success('Student added'); refresh()
            else: show_error(r)

if students:
    ids={f"{s['id']} — {s['name']}":s for s in students}
    selected=st.selectbox('Select student to update or delete', list(ids))
    student=ids[selected]
    with st.form('update'):
        name=st.text_input('Name', student['name']); department=st.text_input('Department',student['department']); email=st.text_input('Email',student['email'])
        if st.form_submit_button('Update'):
            r=requests.put(f"{API}/students/{student['id']}",json={'name':name,'department':department,'email':email})
            if r.ok: st.success('Updated'); refresh()
            else: show_error(r)
    if st.button('Delete selected student'):
        r=requests.delete(f"{API}/students/{student['id']}")
        if r.ok: st.success('Deleted'); refresh()
        else: show_error(r)
