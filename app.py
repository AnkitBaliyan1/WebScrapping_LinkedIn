import utils as utils
import streamlit as st
from io import StringIO
from datetime import datetime, date

def dataframe_to_csv_download(dataframe):
    # Convert the DataFrame to a CSV string
    csv = dataframe.to_csv(index=False)
    csv_bytes = csv.encode('utf-8')

    # Create a buffer to hold the CSV string in bytes
    buf = StringIO()
    buf.write(csv)
    buf.seek(0)

    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Create a download button in the Streamlit app
    st.download_button(
        label="Download CSV File",
        data=csv_bytes,
        file_name=f"ScrappedData_{today}.csv",
        mime="text/csv",
    )



if __name__=='__main__':
    st.title('LinkedIn Job Scraper')
    st.write('This app scrapes LinkedIn for job listings.')
    url = st.text_area("Enter the url here..")

    if st.button("Get Records") and url:
        with st.spinner("Scrapping the given URL"):
            scrap_df = utils.scrap_data(url)
        st.dataframe(scrap_df)
        dataframe_to_csv_download(scrap_df)
        
        st.write('')
