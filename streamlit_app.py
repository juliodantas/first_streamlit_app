import streamlit as st
import pandas as pd
import requests
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

st.title('New Healthy Meals')

st.header('🥣Breakfast Menu')
st.text('🥗Omega 3 & Blueberry Oatmeal')
st.text('🐔Kale, Spinach & Rocket Smoothie')
st.text('🍞Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Let's put a pick list here so they can pick the fruit they want to include

#st.multiselect("Pick some fruits:", list(my_fruit_list.index))

#Let's put a pick list here so they can pick the fruit they want to include

#st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


#Display the table on the page

#st.dataframe(my_fruit_list)
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#st.text(fruityvice_response.json())
fruityvice_normalize = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalize)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

add_my_fruit = st.text_input('What fruit would you like to add?', 'Jackfruit')
st.write('Thanks for adding', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

