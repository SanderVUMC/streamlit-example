import string
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Parcel Review Tool")

# Load data
parcels = pd.read_csv("parcel_info.csv")  
appeals = pd.read_csv("appeals.csv")
triennial = pd.read_csv("2023_triennial_update.csv")

options = st.sidebar.selectbox("Select Parcel ID", 
                              ["Input Parcel ID", "Appealed Parcels"])

def get_criteria(parcel):

  criteria = {
    "PARID": parcel["PARID"], 
    "Built": parcel["YRBLT"],
    "Beds": parcel["BEDS"],
    "FullBaths": parcel["fullbaths"],
    "HalfBath": parcel["Half Bath"],
    "SqFt": parcel["SFLA"],
    "Grade": parcel["GRADE_DESC"],
    "Extwall": parcel["EXTWALL_DESC"]
  }
  
  return criteria

def find_matches(df, parcel, criteria,hood):

  # Criteria ranges
  
  df = df[df["NBHD"]==hood]
  df = df[df["YRBLT"].notna()]

  # Get criteria min/max values
  
  min_year = int(df['YRBLT'].min()) 
  max_year = int(df['YRBLT'].max())
  
  # Get year built from target parcel 
  target_parid = criteria['PARID'].values[0]
  target_year = int(criteria['Built'].values[0])
  target_sqft = int(criteria['SqFt'].values[0])
  target_grade = criteria['Grade'].values[0]
  target_extwall = criteria['Extwall'].values[0]

  # Calculate default min and max
  default_min_year = target_year - 10
  default_max_year = target_year + 10
  
  
  # Set final min and max
  final_min_year = min(default_min_year, min_year) 
  final_max_year = max(default_max_year, max_year)

  min_beds = int(df['BEDS'].min())
  max_beds = int(df['BEDS'].max())

  if min_beds == max_beds:
    min_beds = 1
    
  min_full_baths = int(df['fullbaths'].min())
  max_full_baths = int(df['fullbaths'].max())

  if min_full_baths == max_full_baths:
    min_full_baths = 1

  min_half_baths = int(df['Half Bath'].min())
  max_half_baths = int(df['Half Bath'].max())

  if min_half_baths == max_half_baths:
    min_half_baths = 0

  min_sqft = int(df['SFLA'].min())
  max_sqft = int(df['SFLA'].max())

  default_min_sqft = target_sqft - 200
  default_max_sqft = target_sqft + 200

  final_min_sqft = min(default_min_sqft, min_sqft) 
  final_max_sqft = max(default_max_sqft, max_sqft)

  # Get unique grades
  grades = df['GRADE_DESC'].unique()
  extwalls = df['EXTWALL_DESC'].unique()
  # User select criteria ranges
  
  

  year_range = st.slider("Select year built:", final_min_year, final_max_year, (default_min_year, default_max_year),step=1)
  beds_range = st.slider("Select beds:", min_beds, max_beds, (min_beds, max_beds),step=1)
  full_baths_range = st.slider("Select full baths:", min_full_baths, max_full_baths, (min_full_baths, max_full_baths),step=1)
  half_baths_range = st.slider("Select half baths:", min_half_baths, max_half_baths, (min_half_baths, max_half_baths),step=1)
  sqft_range = st.slider("Select sqft:", final_min_sqft, final_max_sqft, (default_min_sqft, default_max_sqft),step=1)
  selected_grades = st.multiselect("Select grades:", grades,default = target_grade)
  selected_extwalls = st.multiselect("Select extwalls:", extwalls,default = target_extwall,)
  
  ###always add target parcel's grade and extwall
  selected_grades.append(target_grade)
  selected_extwalls.append(target_extwall)

  # Filter by criteria
  if st.button("Find Similar Parcel"): 
     df_matches = df[df['YRBLT'].between(year_range[0], year_range[1])]
     df_matches = df_matches[(df['BEDS'] >= beds_range[0]) & (df['BEDS'] <= beds_range[1])]
     df_matches = df_matches[df['fullbaths'].between(full_baths_range[0], full_baths_range[1])]
     df_matches = df_matches[df['Half Bath'].between(half_baths_range[0], half_baths_range[1])]
     df_matches = df_matches[df['SFLA'].between(sqft_range[0], sqft_range[1])]
     df_matches = df_matches[df['GRADE_DESC'].isin(selected_grades)]
     df_matches = df_matches[df['EXTWALL_DESC'].isin(selected_extwalls)]

  
     # Exclude current parcel
     triennial_value = triennial[["PARID","2023 Total Parcel Value"]]
  
     df_value = pd.merge(df_matches,triennial_value, how='inner',on='PARID')
     first_column = df_value.pop('2023 Total Parcel Value') 
  
     # insert column using insert(position,column_name, 
     # first_column) function 
     df_value.insert(0, '2023 Total Parcel Value', first_column) 
     df_value_output = df_value[['2023 Total Parcel Value', 'PARID', 'OWN1','YRBLT','STORIES','STYLE_DESC','BSMT_DESC','ATTIC_DESC','SFLA','EXTWALL_DESC','BEDS','GRADE','GRADE_DESC','NBHD','NBHD_DESC','CLASS','SALEDT','SALE_PRICE','SALEVAL_DESC','fullbaths','Half Bath','Acres']]
    
     # Get target row index
     idx = df_value_output.index[df_value_output['PARID'] == target_parid]  
     if (idx.empty):
        st.warning("No match parcels.")
     else:    
        
        parcel_row = df_value_output.loc[df_value_output['PARID'] == target_parid]
        final_output = pd.concat([parcel_row, df_value_output.drop(parcel_row.index)], axis=0).reset_index(drop=True)

        final_output.YRBLT =  final_output.YRBLT.astype(int)
        final_output.STORIES =  final_output.STORIES.astype(int)
        final_output.SFLA =  final_output.SFLA.astype(int, errors='ignore')
        final_output.BEDS =  final_output.BEDS.astype(int, errors='ignore')
        final_output.SALE_PRICE =  final_output.SALE_PRICE.astype(int, errors='ignore')
        final_output.fullbaths =  final_output.fullbaths.astype(int, errors='ignore')
        final_output['Half Bath'] =  final_output['Half Bath'].astype(int, errors='ignore')
        parcel_count = len(final_output)
        st.write(f"Total match parcels: {parcel_count}")
        st.table(final_output.style.applymap(
        lambda _: "background-color: CornflowerBlue;", subset=([0], slice(None))
        ))
     

     df_matches = df_matches[df_matches['PARID'] != parcel_id]
  

     # Handle no matches
     if len(df_matches) == 0:
        st.warning("No similar property.")   
    
    

if options == "Input Parcel ID":
    parcel_id = st.text_input("Enter Parcel ID") 

elif options == "Appealed Parcels":
    # Default reason
    reason = "Value in Dispute"
    
    # Allow user to change reason
    reasons = appeals["Reason"].dropna().unique()
   
    reason = st.selectbox("Select appeal reason", reasons, index=0)
    
    # Filter appeals by selected reason 
    reason_appeals = appeals[appeals["Reason"] == reason]
    
    # In Review Case only
    review_appeals = reason_appeals[reason_appeals["Case Status"] == 'In Review']
    
    # Get parcel IDs
    #parcel_ids = review_appeals["PARID"].unique()
    CHOICES = {}
    for index, row in review_appeals.iterrows():
       appeal_parid = row["PARID"]
       nbhd = row["NBHD"]
       parid_nbhd = "PARCEL ID:"+appeal_parid+" - NEIGHBORHOOD: "+nbhd
       CHOICES[appeal_parid] = parid_nbhd
    
    def format_func(option):
       return CHOICES[option]


    parcel_id = st.selectbox("Select from appeal cases:", options=list(CHOICES.keys()), format_func=format_func)
    

if parcel_id:
    
    # Lookup parcel details
 
  parcel = parcels[parcels["PARID"] == parcel_id]
  
  if not parcel.empty:
    # Get neighborhood
    hood = parcel["NBHD"].values[0]
    total_records_in_hood = len(parcels[parcels["NBHD"] == hood])
    st.header(f"{hood} Neighborhood, has {total_records_in_hood} parcels")
    
    # Get prior year value  
    parcel_record = triennial[triennial["PARID"] == parcel_id]
    prior_value = parcel_record["2022 Total Parcel Value"].values[0]

    # Calculate value change
    curr_value = parcel_record["2023 Total Parcel Value"].values[0]
    value_change = curr_value - prior_value
    pct_change = value_change / prior_value
    estimated_tax_change = round((value_change*0.35)/100,0)
    # Display parcel details
    st.subheader(f"{parcel_id} Details")
    st.write(parcel)

    # Check for appeals
    appeal = appeals[appeals["PARID"] == parcel_id]
    if appeal.empty:
        st.write("No appeals found.")
    else:
        st.subheader("Appel Information (including history)")
        st.write(appeal)
        
    # Value change analysis
    st.subheader(f"{parcel_id} Change")
    st.write(f"Prior Year Value: {prior_value}")
    st.write(f"Current Value: {curr_value}")
    st.write(f"Value Change : {value_change}")
    st.write(f"Percent Change : {pct_change*100:.1f}%")

    # Neighborhood change analysis
    hood_changes = triennial[triennial["NBHD"] == hood]
    hood_changes = hood_changes[hood_changes["Percent Change"].notna()]
    
    min_change = hood_changes["Value Change"].min()
    max_change = hood_changes["Value Change"].max()  
    median_change = hood_changes["Value Change"].median()
    avg_change = round(hood_changes["Value Change"].mean(),2)

    min_pct_change = hood_changes["Percent Change"].min()
    max_pct_change = hood_changes["Percent Change"].max()  
    median_pct_change = hood_changes["Percent Change"].median()
    avg_pct_change = round(hood_changes["Percent Change"].mean(),2)

    st.subheader("Neighborhood Value Changes")
    st.write("Min: ", min_change)
    st.write("Max: ", max_change) 
    st.write("Median: ", median_change)
    st.write("Average: ", avg_change)
    
    st.subheader("Neighborhood Percent Changes")
    st.write("Min: ", min_pct_change)
    st.write("Max: ", max_pct_change) 
    st.write("Median: ", median_pct_change)
    st.write("Average: ", avg_pct_change)
    st.write("Your change: ", round(pct_change,2))
    
    st.subheader(f"Estimated Tax Change/year: ${estimated_tax_change}")
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(hood_changes["Percent Change"], bins=20)


    # Add axis labels
    ax.set_xlabel('Percent Change')  
    ax.set_ylabel('Number of parcels')
    # Add text with value counts
    for count, patch in zip(counts, patches):
       ax.text(patch.get_x()+patch.get_width()/2, patch.get_height(), int(count), ha='center', va='bottom') 

    ax.hist(hood_changes["Percent Change"], bins=20)
    ax.axvline(pct_change, color='r', label='Selected Parcel')
    ax.legend()  


    st.pyplot(fig)

    st.subheader("Find similar property in my neighborhood")
    #if st.button("Similar Parcel"):   
       # Get criteria from parcel  
    criteria = get_criteria(parcel)

       # Find matches
    find_matches(parcels, parcel, criteria,hood)

  else:
     st.error("Did not find this parcel.")
