import streamlit as st
from urllib.parse import quote_plus
import time
import base64
from PIL import Image

# --- Set your custom favicon/app icon ---
icon = Image.open("FSBO SIGN 2.jpg")
st.set_page_config(
    page_title="FSBO SEARCH IN ANY AREA",
    page_icon=icon,  # Uses your uploaded image as the favicon/app icon
    layout="centered"
)

# --- Embed your uploaded background image as base64 ---
def get_base64_of_uploaded_file():
    with open("BACKGROUND.JPG.jpg", "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_from_uploaded():
    bin_str = get_base64_of_uploaded_file()
    page_bg_img = f'''
    <style>
    .stApp {{
      background-image: url("data:image/jpg;base64,{bin_str}");
      background-size: cover;
      background-repeat: no-repeat;
      background-attachment: fixed;
    }}
    .main {{
      background-color: rgba(255, 255, 255, 0.9);
      padding: 20px;
      border-radius: 10px;
      margin: 20px;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_bg_from_uploaded()

# --- Custom font, font size, and color ---
st.markdown("""
<style>
/* Change the font for the whole app */
html, body, [class*="st-"]  {
    font-family: 'dingle';
    font-size: 25px;
    color: #000000;
}
/* Change the main title font, size, and color */
.stApp h1 {
    font-family: 'dingle', staatliches;
    font-size: 48px;
    color: #000000;
    text-shadow: 1px 1px 2px #fff;
    font-weight: Regular;
}
/* Change all subheaders */
.stApp h2, .stApp h3 {
    color: #2c3e50;
    font-family: 'dingle', Arial, sans-serif;
}
/* Change sidebar font and color */
.css-1d391kg, .css-1v0mbdj {
    color: #1a5d1a !important;
    font-size: 18px !important;
    font-family: 'dingle', Arial, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("FSBO IN YOUR AREA")
st.markdown("### SEARCH AND GET INSTANT LINKS TO FSBO LISTINGS ACROSS ALL PLATFORMS")

# Sidebar for search settings
st.sidebar.header("🔧 REFINE YOUR SEARCH")
st.sidebar.markdown("---")

location = st.sidebar.text_input("📍 Location (city, state)", "Austin TX", help="Enter the city and state where you want to search for land")

st.sidebar.markdown("**Lot Size & Price Requirements:**")
col1, col2 = st.sidebar.columns(2)
with col1:
    min_acres = st.number_input("Min Acres", min_value=0.0, value=1.0, step=0.5)
with col2:
    max_acres = st.number_input("Max Acres", min_value=0.0, value=20.0, step=1.0)

max_price = st.sidebar.number_input("💰 Max Price ($)", min_value=0, value=100000, step=5000, format="%d")

st.sidebar.markdown("**Land Features:**")
features = st.sidebar.multiselect(
    "Select desired features:",
    ['water access', 'creek', 'pond', 'well', 'electricity', 'road access',
     'wooded', 'cleared', 'fenced', 'hunting', 'fishing', 'mineral rights',
     'timber', 'pasture', 'buildable', 'mobile home ok', 'no restrictions',
     'owner financing', 'cash only', 'surveyed', 'corner lot'],
    default=[],
    help="Select any features you want in your land"
)

st.sidebar.markdown("**Property Type & Financing:**")
land_type = st.sidebar.selectbox(
    "🏞️ Land Type",
    ['any', 'residential', 'agricultural', 'commercial', 'recreational', 'timber', 'ranch']
)

financing = st.sidebar.selectbox(
    "💳 Financing Preference",
    ['any', 'owner financing', 'cash only', 'conventional loan ok']
)

# Generate custom search terms based on user input
base_terms = [
    "land for sale by owner",
    "FSBO land",
    "owner financed land",
    "raw land for sale",
    "vacant land owner"
]

terms = base_terms.copy()

# Add size-specific terms
if max_acres <= 5:
    terms.extend(['small lot for sale', 'building lot owner'])
elif min_acres >= 10:
    terms.extend(['acreage for sale', 'large tract owner'])

# Add feature-specific terms
for feature in features:
    if feature in ['water access', 'creek', 'pond']:
        terms.append('waterfront land owner')
    elif feature == 'hunting':
        terms.append('hunting land FSBO')
    elif feature == 'owner financing':
        terms.append('owner will carry land')

# Add land type terms
if land_type != 'any':
    terms.append(f"{land_type} land FSBO")

# Remove duplicates
terms = list(set(terms))

# Generate search URLs
loc_url = location.replace(' ', '-').lower()
loc_clean = loc_url.replace('-', '')

urls = {
    "🔍 Craigslist": f"https://{loc_clean}.craigslist.org/search/rea?query={quote_plus(terms[0])}&sort=date",
    "📘 Facebook Marketplace": f"https://www.facebook.com/marketplace/{loc_url}/search?query={quote_plus('land for sale by owner')}",
    "🌍 LandWatch": f"https://www.landwatch.com/land-for-sale/{loc_url}",
    "🚜 LandAndFarm": f"https://www.landandfarm.com/search/{loc_url}-land-for-sale/",
    "🏠 Zillow FSBO": f"https://www.zillow.com/homes/for_sale/{loc_url}_rb/?searchQueryState=%7B%22usersSearchTerm%22%3A%22{loc_url}%20land%20for%20sale%20by%20owner%22%7D",
    "🏢 LoopNet": f"https://www.loopnet.com/search/vacant-land-for-sale/{loc_url}/",
    "🌲 LandHub": f"https://www.landhub.com/land-for-sale/{loc_url}",
    "🇺🇸 Lands of America": f"https://www.landsofamerica.com/land-for-sale/{loc_url}/"
}

# Main content area
st.markdown("---")

# Display current search configuration
with st.expander("📋 Your Current Search Settings", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**📍 Location:** {location}")
        st.write(f"**📏 Size:** {min_acres} - {max_acres} acres")
        st.write(f"**💰 Max Price:** ${max_price:,}")
    
    with col2:
        st.write(f"**🏞️ Land Type:** {land_type}")
        st.write(f"**💳 Financing:** {financing}")
        st.write(f"**✨ Features:** {', '.join(features) if features else 'None specified'}")

# Display search terms being used
with st.expander("🔍 Search Terms Being Used"):
    st.write("The following search terms will be used to find land listings:")
    for i, term in enumerate(terms, 1):
        st.write(f"{i}. {term}")

# Main search results section
st.markdown("---")
st.subheader("🔗 Search These Websites")
st.write("Click any link below to search for land on that platform:")

# Display search URLs in a nice format
for name, url in urls.items():
    st.markdown(f"### [{name}]({url})")
    st.write(f"Search for FSBO land in {location}")
    st.markdown("---")

# Download functionality
st.subheader("📥 Download Search URLs")
st.write("Get all search URLs in a text file for easy access:")

if st.button("📄 Generate Download File", type="primary"):
    # Create downloadable content
    url_text = f"""LAND SEARCH URLS - {location.upper()}
Generated on: {time.strftime('%Y-%m-%d at %H:%M:%S')}
{'='*60}

SEARCH CONFIGURATION:
Location: {location}
Size: {min_acres} - {max_acres} acres
Max Price: ${max_price:,}
Land Type: {land_type}
Financing: {financing}
Features: {', '.join(features) if features else 'None specified'}

SEARCH TERMS USED:
{chr(10).join([f'{i}. {term}' for i, term in enumerate(terms, 1)])}

SEARCH URLS:
{'='*60}

"""
    
    for name, url in urls.items():
        url_text += f"{name}:\n{url}\n\n"
    
    url_text += """INSTRUCTIONS:
1. Copy any URL above
2. Paste it into your web browser
3. Press Enter to search
4. Look for 'For Sale By Owner' or 'FSBO' listings
5. Contact sellers directly

TIP: Check these sites daily as good deals go fast!
"""
    
    st.download_button(
        label="💾 Download URLs as Text File",
        data=url_text,
        file_name=f"land_search_urls_{loc_url}_{time.strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

# Tips and instructions
st.markdown("---")
st.info("💡 **Pro Tips:** Check these sites daily, set up Google Alerts for your search terms, and be ready to act fast on good deals!")

st.success("🎯 **How to Use:** Click the links above to search each platform. Look for listings marked 'FSBO', 'For Sale By Owner', or 'Owner Financing'.")

# Footer
st.markdown("---")
st.markdown("*BUILT FOR THOSE WHO WANT THE INSIDE SCOOP 😉*")