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

#create a repitable code block
def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized

#new section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input("What fruit would you like information about?")
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
 else: 
  back_from_function = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
  
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
#streamlit.stop()


#import snowflake.connector
streamlit.header("The fruit load list contains:")
#snowflake-related function
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("select * from fruit_load_list")
  return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 streamlit.dataframe(my_data_rows)
 

#challenge
fruit_choice = streamlit.text_input('What fruit would you like to add','jackfruit')
streamlit.write('thanks for adding ', fruit_choice)

#
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
