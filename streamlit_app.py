# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col



st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get name on order
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get active Snowflake session
cnx=st.connection("snowflake")
session=cnx.session()


# Get fruit options from Snowflake and convert to pandas
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .to_pandas()
)

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'],
    max_selections=5
)

# If ingredients selected, prepare insert
if ingredients_list:

    # Convert list to a single string
    ingredients_string = ', '.join(ingredients_list)

    # Build INSERT statement (table has TWO columns)
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(
            f'✅ Your Smoothie is ordered, {name_on_order}!'
        )
st.write("🥝 SmoothieFroot API Response")
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
