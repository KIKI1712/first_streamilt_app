import streamlit
import pandas
import requests
import snowflake.connector 
from urllib.error import URLError

streamlit.title('My parent healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#pick
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#display
streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#new section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?')
if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
else: 
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
#import request
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#take the json version of repsonse and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it on the screen as table
#streamlit.dataframe(fruityvice_normalized)

#don't run anything past here
streamlit.stop()


#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#challenge
fruit_choice = streamlit.text_input('What fruit would you like to add','jackfruit')
streamlit.write('thanks for adding ', fruit_choice)

#
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
