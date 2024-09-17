# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name On Smoothie:")
st.write("The name on the Smoothie will be", name_on_order)

#take column name FRUIT_NAME from table smoothies.public.fruit_options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
    'Chose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections =5)

#if ingredients_list is not null
if ingredients_list:
    #st.write(ingredients_list);
    #st.text(ingredients_list);

    ingredients_string = "";
    
    for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen+' ';
    
    #st.write(ingredients_string);

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt);
    #st.stop();
    
    
    time_to_insert = st.button("Sumbit Order");

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+'', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width = True)
