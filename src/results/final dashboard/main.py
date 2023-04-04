import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image
import folium
from streamlit_folium import folium_static
st.set_page_config(layout="wide")


@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    df1 = data.filter(
        [
            "Chlorophyll",
            "Dissolved Oxygen",
            "Dissolved Oxygen Matter",
            "Salinty",
            "Temperature",
            "Turbidity",
            "pH",
            "Suspended Matter",
        ]
    )
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Date"] = pd.to_datetime(data["Date"]).dt.date
    data["Year"] = pd.to_datetime(data["Date"]).dt.strftime("%Y")
    data["Month"] = pd.to_datetime(data["Date"]).dt.strftime("%m")
    data["Day"] = pd.to_datetime(data["Date"]).dt.strftime("%d")
    return data, df1

with open("styles.css", "r") as source_style:
 st.markdown(f"<style>{source_style.read()}</style>", 
             unsafe_allow_html = True)

st.header("Monitoring the Water Quality in Bhopal Region using Satellite Imagery and GIS Techniques")
image = Image.open(r'logo.png')
st.image(image)

header_project = st.container()
data_collection = st.container()
data_analysis = st.container()



data_df, df1 = load_data("merged_data.csv")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=[
            "Project Information",
            "Data Collection",            
            "Interactive Data Analysis",
            "Insights",
            "Dashboards",
            "Contributors"
        ],
        default_index=0,
    )


if selected == "Project Information":

    with header_project:
        st.subheader("Introduction")
        introduction_str=""" 
        The primary objective of this challenge is to find effective ways to monitor water quality in the Bhopal region using satellite imagery.
        The purpose of this project is to reduce the cost of the monitoring process, as the current method utilizing IoT sensors requires a 
        significant amount of maintenance, making it an expensive process. The main goal of the project is to identify parameters that can be 
        used to monitor water quality, establish a standardized way of collecting real-time data, identify any discrepancies in the current 
        monitoring process, and improve them as much as possible. To achieve these objectives, a detailed data analysis will be conducted. We 
        will examine a range of satellite imagery data and extract the relevant parameters that can be used to monitor water quality. By 
        analyzing this data, we will be able to identify patterns and trends that can be used to improve the monitoring process. Finally, we 
        will develop a visualization dashboard using either Tableau or Power BI to present the collected data in a user-friendly and visually 
        appealing manner. The dashboard will provide key metrics and insights related to water quality in the region, allowing for easy 
        monitoring and informed decision-making based on the data collected.
        
        
        The challenge, which united an international team of AI engineers over 5 weeks, was led by Vaasu Bisht and Eeman Majumder. The common 
        language for the chapter was English. Platforms such as GitHub, Notion, Asana, and a dedicated Slack channed were used to coordinate and 
        keep track of the engineer's work.
        """
        st.text(introduction_str)

        st.subheader("Our Solution")

        our_solution_str=""" 
        The team developed a user-friendly visualization dashboard that integrates the processed data from satellite imagery and GIS techniques. The dashboard 
        provides real-time updates on key water quality parameters, including temperature, pH, dissolved oxygen, and turbidity. It also allows for easy monito-
        ring of trends and patterns in the data, enabling users to quickly identify any discrepancies in water quality and take necessary corrective action. 
        The dashboard's visually appealing interface and user-friendly design make it an effective tool for decision-making and collaboration between various 
        stakeholders, including government agencies, NGOs, and local communities. Overall, the dashboard is a valuable asset in the ongoing efforts to protect 
        and improve the water quality in the Bhopal region.
        """
        st.text(our_solution_str)


        st.subheader("The Data")

        the_dat_Srt=""" 
        For our water quality monitoring project in the Bhopal region, we collected data from various lakes using satellite imagery and GIS techniques. The lakes
        we focused on include Upper Lake, Lower Lake, Kaliyasot dam, Kerwa Dam, Shahpura Lake, Sarangpani Lake, Motia talab, Hathaikheda dam/lake, Nawab Munshi 
        Hussain Khan Talab, Nawab Siddiqui Hasan Khan Talaab, Jawahar Baal Udyan Lake, Lendiya Talab, Manit lake, and bhojtal lake.

        To effectively monitor the water quality in these lakes, we collected various parameters related to water quality, including pH, salinity, turbidity, 
        temperature, chlorophyll, suspended matter, dissolved oxygen, and dissolved organic matter (DOM). These parameters were chosen based on their relevance 
        to water quality and their ability to provide insights into the health of the lakes.
        """
        st.text(the_dat_Srt)


if selected == "Data Collection":
    with data_collection:
        st.title("Data Collection")
        introduction_string = """
        Collecting data using the Google Earth Engine API can be a complex and daunting task. Our team found that one of the major challenges in the process was 
        the lack of a standardized approach to data collection. Without a standardized methodology, the data collected from different sources can vary greatly, 
        making analysis and comparison difficult. This is where our team stepped in, developing a standardized function and classes to improve the data collection 
        process.

        Our standardized function and classes not only made data collection more efficient, but also helped to maintain consistency across multiple data sources. 
        With our solution, we were able to collect data from various sources in a streamlined manner, ensuring that the collected data was consistent and accurate. 
        We believe that our contribution will be valuable to researchers and scientists working in the field, and we are proud to have developed a solution that 
        improves the quality and reliability of data collected using the Google Earth Engine API.
        """
        st.text(introduction_string)

        st.title("Get Salanity")

        code = """
def get_Salanity(start_date, end_date):

    # Selecting the satellite and AOI  
    # Sentinel 2A
    # copernicus/s2_sr 
    sentinel = ee.ImageCollection("COPERNICUS/S2_SR").
               filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).
               filterDate(start_date, end_date)
    AOI = geometry

    sentinel_AOI = sentinel.filterBounds(AOI)

    #calculate NDSI
    def calculate_NDSI(image):
        ndsi = image.normalizedDifference(['B11', 'B12']).rename('NDSI')
        return image.addBands(ndsi)
    ndsi = sentinel_AOI.map(calculate_NDSI)

    # Mean NDSI
    def calculate_mean_NDSI(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['NDSI']),
                                geometry = AOI,
                                scale = image.projection().nominalScale().getInfo(),
                                maxPixels = 100000,
                                bestEffort = True);
        return mean.get('NDSI').getInfo()
        
    # NDSI Mean Collection
    Images_ndsi = ndsi.select('NDSI').toList(ndsi.size())
    ndsi_coll = []
    for i in range(Images_ndsi.length().getInfo()):
        image = ee.Image(Images_ndsi.get(i-1))
        temp_ndsi = calculate_mean_NDSI(image)
        ndsi_coll.append(temp_ndsi)

    # Dates Collection
    dates = np.array(ndsi.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]

    # Dataframe for Salinity

    df = pd.DataFrame(ndsi_coll, index = day, columns = ['Salinity'])
    df.index = pd.to_datetime(df.index, format="%Y/%m/%d")
    df.sort_index(ascending = True, inplace = True)

    return df
    """

    st.code(code, language='python')



    st.title("Get Chlorophyll")

    code = """
    def get_chlorophyll(start_date, end_date):

        # Selecting the satellite and AOI  
        # Sentinel 2A
        # copernicus/s2_sr 
        sentinel = ee.ImageCollection("COPERNICUS/S2_SR").
                filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).
                filterDate(start_date, end_date)
        AOI = geometry

        sentinel_AOI = sentinel.filterBounds(AOI)
        # NDCI calculation
        def calculate_NDCI(image):
            ndci = image.normalizedDifference(['B5', 'B4']).rename('NDCI')
            return image.addBands(ndci)
        ndci = sentinel_AOI.map(calculate_NDCI)  

        # NDCI mean
        def calculate_mean_NDCI(image):
            image = ee.Image(image)
            mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['NDCI']),
                            geometry = AOI,
                            scale = image.projection().nominalScale().getInfo(),
                            maxPixels = 100000,
                            bestEffort = True);
            return mean.get('NDCI').getInfo()    
        
        # NDCI mean collection    
        Images_ndci = ndci.select('NDCI').toList(ndci.size())
        ndci_coll = []
        for i in range(Images_ndci.length().getInfo()):
            image = ee.Image(Images_ndci.get(i-1))
            temp_ndci = calculate_mean_NDCI(image)
            ndci_coll.append(temp_ndci)
        # Dates collection
        dates = np.array(ndci.aggregate_array("system:time_start").getInfo())
        day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]

        # Dataframe for chlorophyll
        df = pd.DataFrame(ndci_coll, index = day, columns = ['Chlorophyll'])
        df.index = pd.to_datetime(df.index, format="%Y/%m/%d")
        df.sort_index(ascending = True, inplace = True)

        return df
    """

    st.code(code, language='python')


    st.title("Get Turbidity")

    code = """
    def get_turbidity(start_date, end_date):

        # Selecting the satellite and AOI  
        # Sentinel 2A
        # copernicus/s2_sr 
        sentinel = ee.ImageCollection("COPERNICUS/S2_SR").
                filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).
                filterDate(start_date, end_date)
        AOI = geometry

        sentinel_AOI = sentinel.filterBounds(AOI)

        #calculate NDTI
        def calculate_NDTI(image):
            ndti = image.normalizedDifference(['B4', 'B3']).rename('NDTI')
            return image.addBands(ndti)
        ndti = sentinel_AOI.map(calculate_NDTI)

        # Mean NDTI
        def calculate_mean_NDTI(image):
            image = ee.Image(image)
            mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['NDTI']),
                                    geometry = AOI,
                                    scale = image.projection().nominalScale().getInfo(),
                                    maxPixels = 100000,
                                    bestEffort = True);
            return mean.get('NDTI').getInfo()
        
        # NDTI mean collection 
        Images_ndti = ndti.select('NDTI').toList(ndti.size())
        ndti_coll = []
        for i in range(Images_ndti.length().getInfo()):
            image = ee.Image(Images_ndti.get(i-1))
            temp_ndti = calculate_mean_NDTI(image)
            ndti_coll.append(temp_ndti)

        # Dates Collection
        dates = np.array(ndti.aggregate_array("system:time_start").getInfo())
        day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]

        # Dataframe for Turtbidity

        df = pd.DataFrame(ndti_coll, index = day, columns = ['Turbidity'])
        df.index = pd.to_datetime(df.index, format="%Y/%m/%d")
        df.sort_index(ascending = True, inplace = True)

    return df
    """

    st.code(code, language='python')



    st.write("You can find other functions here -  [link](https://github.com/OmdenaAI/omdena-bhopal-water-quality-monitoring/blob/main/Standard_function.ipynb)")




    st.video(r"datcollection_dashboard.mp4", format="video/mp4")
#         st.text(
#             """ In the first week of the project, we conducted research on different types of APIs for 
# collecting water quality data in Bhopal. After careful consideration, we chose the 
# Google Earth Engine API for our data collection. \n    streamlit run main.py
# In the second week, we started collecting data using the Google Earth Engine API, 
# using Sentinel 2A and Landsat 8 satellite imagery to collect data on various water 
# quality parameters, including chlorophyll, turbidity, salinity, pH, dissolved oxygen, 
# dissolved organic matter, and suspended matter."""
#         )

if selected =='Insights':
        
        st.header("Water Quality Index and Parameters Identification")
        
        str_text_body = """ 
            There are several water quality parameters available, but the team has chosen the following 8 important 
        parameters to monitor water quality.\n

        1-pH:One of the most crucial indicators of water quality is pH. The pH scale determines how basic or acidic a 
        solution is. \n
        2- Salinity: The quantity of dissolved salts in water is known as salinity.
        Water that is cloudy or hazy due to numerous tiny particles that are often unseen to the unaided eye is said to 
        be turbid. Water quality is typically impacted by suspended sediments, such as clay, dirt, and silt particles, 
        which frequently enter the water from disturbed locations.\n

        3- Temperature: The aquatic system is significantly influenced by water temperature, which also affects the habitat's 
        suitability for supporting aquatic life. Lower oxygen solubility in warmer water restricts the amount of oxygen
        available.\n

        4- Chlorophyll: A popular indicator of water quality and eutrophication level is chlorophyll-a.
        The concentration of phytoplankton is determined by the amount of chlorophyll present in a water sample. 
        Greater concentrations, which often occur when high algal production is sustained, indicate poorer water quality.\n


        5- Suspended matter: Fine particles make up suspended matter, which is in suspension. Plankton, tiny pieces of plant matter,
        and minerals are among those that naturally occur in river water, whilst others are a result of human activity
        (organic and inorganic matter). Water can become more turbid due to suspended materials, harming the ecology 
        of rivers and streams.\n

        6- Dissolved oxygen (DO) is a gaseous form of molecular oxygen (O2) that comes from the environment. 
        The concentrations of dissolved oxygen in water are influenced by salinity and temperature. 
        Temperature and salinity have an opposite relationship with oxygen solubility in water;
        as these two variables rise, so does DO.\n
        7- The organic matter percentage in solution that passes through a 0.45 m filter is referred to as
        "dissolved organic matter" (DOM). The mass of other elements, such as nitrogen, oxygen, and hydrogen,
        that are present in organic material is also included in DOM. The total mass of the dissolved organic matter
        is referred to here as DOM. \n

        This figure shows paramters values for safe and danger zone. \n
        """
        st.text(str_text_body)
        image = Image.open(r'Parameter-Thresholds.png')
        st.image(image)
        st.header("Findings")
        st.subheader('Per-year Findins')
        str_findings= """
        1- pH level had outlier in 2019, 2022. However it could be concluded that each year the distribution ranges changes
        2- Turbidity had outliers values since 2019, however the disrtibution didn't change across the years
        3- Temperautre had outliersin every-year. However we have no information in 2022.
        In covid year the disribution of temperatures varies. However before and  after 2020 the temperatures variation across years is not large
        4- Salinty had large number of outliers in 2019. However distribution and ranges across year varies.
        5- Disssolved oxygen matter is the most consisent features across years. There are small number of outliers
        6- Dissolved oxygen had outliers since 2019. However the disrtibution across years are quit similar.
        """
        st.text(str_findings)
        st.subheader('Per-Month Findins')
        str_findings= """
        1- Chrolophyll values across year pe-month ar not so good except for 2022 fisrt month has bad zone values. 
        2- Dissloved oxygen for 20220 values where in bad zone and begging of2021. Hoever the rest are in good zone values
        3- Dissolved oxygen matters for 2019,2018 the values where in bad zone ranges. However, 
        for 2020,2021,2022 for first 2 months andlast 3 months the values where in good zone range however
        from month 3-9 the values are too high
        4- Salinty values are between 0-1 for most year hence, lies whithin bad zone values
        5- Trubidity values are less than 0 for all months hence lies within good zone 
        6- pH values are in good zone ranges for all years and months
        """
        st.text(str_findings)
        st.subheader('Overall Conclusion')
        str_findings="""
        Our data collection efforts yielded a rich dataset of water quality parameters for Lendyia lake in the Bhopal region.
        We found that chlorophyll levels varied widely showing high levels of chlorophyll, indicating high levels of algae and other aquatic plants. 
        Turbidity levels were generally within the acceptable range.
        pH levels were generally within the acceptable range.
        Dissolved oxygen levels were generally within the acceptable range as well, however there were some outliers.
        For the dissolved oxygen matters: Mmre than **50%** of the values lie in **need treatment zone**.
        Overall, the data provides a comprehensive view of water quality in the Bhopal region and can be
        used to inform future efforts to monitor and manage water resources in the area.


        """
        st.text(str_findings)
        st.subheader('Conclusion')
            
        conlsution = """
        In conclusion, monitoring water quality using satellite imagery, GIS techniques, and 
        machine learning is crucial to ensure safe water consumption and protect the 
        environment. These technologies provide a broad and detailed view of the region, 
        which is essential for developing appropriate strategies to address water quality 
        issues. The project's findings and recommendations can inform stakeholders to 
        implement effective and sustainable monitoring programs to ensure the long-term 
        """

        st.text(conlsution)


if selected == "Interactive Data Analysis":


    st.sidebar.subheader("Visualisation Settings")

    # add a select widget to the sidebar
    chart_select = st.sidebar.selectbox(
        label = "Select the Lake",
        options = ['Hathaikheda dam', 'Sarangpani lake', 'Upper lake' , 'Lower lake']
    )

    if chart_select == 'Hathaikheda dam':
        df = pd.read_csv('Hathaikheda.csv')
        st.subheader('Hathaikheda Dam')
        
        shape_tuple = [[23.276159781091796, 77.48381495776124], [23.275981245796764, 77.48359275012776], [23.275902400663092, 77.48316359668537], [23.275606730996113, 77.48333525806233], [23.275429328880875, 77.4835283771114], [23.275035101112213, 77.48348546176716], [23.274995678271157, 77.48324942737385], [23.27456202624964, 77.4839789882259], [23.27420721900009, 77.48374295383259], [23.273734141197263, 77.48339963107868], [23.27333990841148, 77.48202634006306], [23.273537024950212, 77.48425793796345], [23.273300485068734, 77.48524499088093], [23.273162503277234, 77.48616767078205], [23.272176914895812, 77.48786282687946], [23.272019220078107, 77.48932194858357], [23.272019220078107, 77.49069523959919], [23.270718230709516, 77.49168229251667], [23.270245140516476, 77.49288392215534], [23.270402837434148, 77.49348473697468], [23.269678267622574, 77.49371020641799], [23.26928402283434, 77.49276606884474], [23.268574379275776, 77.49285189953322], [23.267806444763416, 77.49248135600928], [23.267451619521786, 77.49175179515723], [23.266741966203956, 77.49192345653418], [23.265992883601633, 77.49123681102637], [23.26528322251516, 77.4914943030918], [23.264691835389545, 77.49085057292822], [23.264337001854468, 77.49115098033789], [23.264179297757845, 77.49188054118994], [23.262996511084673, 77.49196637187842], [23.263390774475408, 77.49278176341895], [23.26410044563953, 77.49312508617285], [23.264415853832798, 77.49278176341895], [23.26528322251516, 77.4929534247959], [23.26587460701633, 77.49415505443457], [23.2662688618924, 77.49445546184424], [23.266111160081945, 77.49501336131934], [23.26630828731585, 77.49535668407324], [23.266347712727633, 77.49582875285986], [23.266544839611605, 77.49660122905615], [23.265559202275632, 77.49668705974463], [23.26516494529999, 77.49582875285986], [23.264691835389545, 77.49595749889258], [23.263982167374618, 77.49570000682715], [23.263785036699794, 77.49509919200781], [23.262681099532323, 77.49574292217139], [23.269265160829594, 77.50084984813574], [23.269895952020086, 77.50127900157813], [23.274547944814806, 77.49939072643164], [23.275178710991543, 77.49973404918555], [23.27541524753774, 77.50012028728369], [23.27600658706548, 77.4999057105625], [23.275809474181273, 77.49917614971045], [23.27608543213749, 77.49883282695654], [23.277303103570617, 77.49905442493679], [23.277657902573278, 77.49832486408474], [23.277579058432142, 77.49780987995388], [23.27817038835291, 77.49755238788845], [23.27686945906157, 77.49729489582302], [23.276554080349985, 77.49669408100368], [23.277224259219434, 77.49579285877468], [23.277894434716618, 77.4957070280862], [23.277539636344073, 77.49523495929958], [23.27686945906157, 77.49540662067653], [23.2764752355554, 77.49523495929958], [23.276435813140612, 77.49454831379177], [23.27592332068646, 77.49506329792263], [23.275292558035876, 77.49416207569362], [23.275253135271036, 77.49360417621853], [23.27434640845934, 77.49476289051296], [23.273557945345097, 77.4948058058572], [23.27320313542108, 77.49411916034938], [23.273873331150828, 77.49308919208767], [23.273597368611647, 77.49248837726833], [23.274228139289725, 77.49171590107204], [23.274858906980878, 77.491887562449], [23.274977175590436, 77.49094342487575], [23.27572620767904, 77.49064301746608], [23.274109870015103, 77.48939847248317], [23.27340025216221, 77.48926972645046], [23.273518522066873, 77.48669480579616], [23.273833907965955, 77.48613690632106], [23.274819484087697, 77.48545026081325], [23.27548967168506, 77.48510693805935]]

        # Create a Folium map
        m = folium.Map(location=[23.276159781091796, 77.48381495776124], zoom_start=15)

        # Add a marker to the map
        #folium.Marker([42.363600, -71.099500], popup="My Marker").add_to(m)

        # Add a polygon to the map using the shape tuple
        folium.Polygon(locations=shape_tuple, color='blue', fill_opacity=0.3).add_to(m)

        # Render the map in Streamlit
        folium_static(m)
    elif chart_select == 'Sarangpani lake' :
        df = pd.read_csv('SarangpaniLakefinal.csv')
        st.subheader('Sarangpani Lake')

        shape_tuple = [[23.244997616477278, 77.47025211456], [23.244248411693995, 77.4703594029206], [23.244061109840693, 77.47089584472357], [23.24396252981228, 77.4707027256745], [23.243775227557578, 77.47074564101874], [23.243647073231774, 77.47029502990424], [23.243499202702868, 77.47043450477301], [23.243440054445415, 77.47086365821539], [23.24331189979763, 77.47074564101874], [23.243035873984248, 77.47107823493658], [23.243213319215556, 77.47135718467413], [23.242986583600327, 77.47164686324774], [23.2428781446916, 77.47203310134589], [23.24237538132672, 77.47211893203436], [23.242188076843604, 77.4725588143128], [23.241902190546604, 77.47259100082098], [23.242188076843604, 77.47295578124701], [23.243400622259205, 77.47293432357489], [23.24357806700535, 77.47263391616522], [23.243785085577528, 77.47251589896857], [23.24409068383501, 77.47215111854254], [23.24450471906707, 77.47203310134589], [23.244997616477278, 77.47100313308417], [23.245165201181862, 77.47038086059271], [23.244997616477278, 77.47025211456]]

        # Create a Folium map
        m = folium.Map(location=[23.244997616477278, 77.47025211456], zoom_start=15)

        # Add a marker to the map
        #folium.Marker([42.363600, -71.099500], popup="My Marker").add_to(m)

        # Add a polygon to the map using the shape tuple
        folium.Polygon(locations=shape_tuple, color='blue', fill_opacity=0.3).add_to(m)

        # Render the map in Streamlit
        folium_static(m)
    elif chart_select == 'Upper lake' :
        df = pd.read_csv(r'UPlake.csv')
        st.subheader('Upper Lake')
        
        shape_tuple = [[23.232761790196488, 77.26237321404831], [23.232840660845348, 77.26511979607956], [23.233313883759763, 77.267179732603], [23.23402371498537, 77.26829553155319], [23.234674390292355, 77.26962590722458], [23.235364496999868, 77.27052712945358], [23.235679973163304, 77.27160001305954], [23.235857428177503, 77.2754838517131], [23.23654752876732, 77.27681422738449], [23.237710833111613, 77.2801627411211], [23.23704045557509, 77.28230850833302], [23.237631965340928, 77.28303806918507], [23.23721790878016, 77.28402512210255], [23.236054600138736, 77.28481905597096], [23.234634955515563, 77.28522675174122], [23.233705619513465, 77.28613082018144], [23.233547879191406, 77.28677455034502], [23.232719739441997, 77.28628102388627], [23.23011698106417, 77.28662434664018], [23.229663464942764, 77.28746119585283], [23.230471905649622, 77.28789034929521], [23.231142316180662, 77.28737536516435], [23.2314578023243, 77.28728953447587], [23.232049336833768, 77.28840533342607], [23.234454883497264, 77.28823367204912], [23.23591396444648, 77.2883195027376], [23.236769916674575, 77.28837124970295], [23.237972652882295, 77.28832833435871], [23.238445857598926, 77.28884331848957], [23.238840193580856, 77.28937976029255], [23.239786595182665, 77.2911178317342], [23.23915566152733, 77.29229800370075], [23.238662742533208, 77.29337088730671], [23.23836699026269, 77.2939287867818], [23.240133303907186, 77.29398622573325], [23.240862815331276, 77.2942651754708], [23.241138845640755, 77.29368581832358], [23.24275558312766, 77.2967328077645], [23.24279501550453, 77.29793443740317], [23.243248487000805, 77.29810609878012], [23.24305132567008, 77.2988571173043], [23.242538704846528, 77.30102434218833], [23.24275558312766, 77.3012174612374], [23.242538704846528, 77.30207576812217], [23.241907784205782, 77.30209722579428], [23.240074154157448, 77.30374946654746], [23.239582284800928, 77.3033402526046], [23.23879361605795, 77.3044560515548], [23.238280978875228, 77.30449896689903], [23.23837956310179, 77.30520707007896], [23.23972030135167, 77.30507832404625], [23.241041309685926, 77.30548601981651], [23.241829965142713, 77.3052499854232], [23.24636464354256, 77.30758887168419], [23.246108339743298, 77.31052857276451], [23.24644350615094, 77.31288891669762], [23.24693639639692, 77.31402617331993], [23.246522368712704, 77.31726628180992], [23.243885470822075, 77.31992887375313], [23.243865754796243, 77.32464956161934], [23.24524586956597, 77.32668804047066], [23.2445952458107, 77.32962774155098], [23.241540519998058, 77.32847690020084], [23.237064828731445, 77.32173919115543], [23.235704346568138, 77.3209237996149], [23.234225545876814, 77.32122420702457], [23.231583381184066, 77.32060193453312], [23.22923693734785, 77.31873511705875], [23.227166511475755, 77.31967925463199], [23.227718628181268, 77.32367038164615], [23.228527080666137, 77.32476472292423], [23.2284482074685, 77.32658862505436], [23.22909890995536, 77.32856273088932], [23.227205948459027, 77.33283280764103], [23.231405920486978, 77.33386277590274], [23.2339297837722, 77.33508586321354], [23.234126958581435, 77.33669518862247], [23.23446215508857, 77.33746766481876], [23.23661133621813, 77.33843326006412], [23.236493033569893, 77.3406434002924], [23.238563314771934, 77.34332560930729], [23.238997083906145, 77.34474181566715], [23.236473316451658, 77.34671592150211], [23.233811478746834, 77.34665154848575], [23.230952408744752, 77.34540700350284], [23.23069607533931, 77.34712361727237], [23.22935524642781, 77.3495054188776], [23.225983396561073, 77.35023497972965], [23.226003115228902, 77.35182284746647], [23.22322275432265, 77.35495566759586], [23.22237483132055, 77.3555564824152], [23.220383177047477, 77.35517024431705], [23.219259161029335, 77.35615729723453], [23.220402896542303, 77.35924720201969], [23.220126823349766, 77.36064195070743], [23.217129420526543, 77.36448287401676], [23.21513953868048, 77.3722302781781], [23.215652264728384, 77.37377523057067], [23.21403519897015, 77.37574933640563], [23.213206938196343, 77.37793801896179], [23.21498177642367, 77.37978337876403], [23.216874911208343, 77.37858174912536], [23.216243869261277, 77.37669347397888], [23.216283309470302, 77.37596391312682], [23.21782146853908, 77.37553475968444], [23.218768019161807, 77.37467645279968], [23.218215865447103, 77.37308858506286], [23.217150991122715, 77.37227319352233], [23.216953791242116, 77.37141488663757], [23.21750595017416, 77.3702132569989], [23.217663709449784, 77.36926911942565], [23.226931739816962, 77.35931275956237], [23.230993695038688, 77.35476373307311], [23.237145547181115, 77.35690950028503], [23.24120719155885, 77.36463426224792], [23.242271874000338, 77.37072824112975], [23.24146500445268, 77.37402233241525], [23.241760749856077, 77.37500938533273], [23.241326989706742, 77.37612518428293], [23.24146500445268, 77.37709077952829], [23.241425571682697, 77.3793438351008], [23.24237195494558, 77.38049182055917], [23.2428845764099, 77.38131794093576], [23.242825427879925, 77.38213333247629], [23.24331833149501, 77.38346370814767], [23.244392855063186, 77.38710078357187], [23.2449054687618, 77.38773378489938], [23.245211064452576, 77.38864573596445], [23.246285572774337, 77.3904374515864], [23.247965980688793, 77.39186194294962], [23.24806455775845, 77.3927417075065], [23.248271569367592, 77.3932459628013], [23.2489221751902, 77.39352491253885], [23.249503774678185, 77.39412572735819], [23.250489530729574, 77.39517715329202], [23.25052896082007, 77.39577796811136], [23.250883831109903, 77.39605691784891], [23.252047010439238, 77.39730146283182], [23.252441306214312, 77.39799883717569], [23.253210179622247, 77.39825632924112], [23.253239751587856, 77.39853527897867], [23.25381147496724, 77.39864256733927], [23.253683330285018, 77.39779498929056], [23.254560626029498, 77.39750531071695], [23.254570483252262, 77.3972263609794], [23.254767627554482, 77.39726927632364], [23.25569420187015, 77.39667919034036], [23.256137772401594, 77.39581015461954], [23.257143193475752, 77.39366438740763], [23.257005194953745, 77.39174392575296], [23.25717276456904, 77.39115383976969], [23.257606473183486, 77.39045646542581], [23.25834574597845, 77.38960888737711], [23.259952418048663, 77.38655116910013], [23.259794708763945, 77.38576796406778], [23.259430005328387, 77.38562848919901], [23.25893716126262, 77.38525297993692], [23.25878930768757, 77.38481309765848], [23.25866116778987, 77.38449123257669], [23.25867102470945, 77.38419082516702], [23.2585133139087, 77.38375094288858], [23.2585133139087, 77.38336470479044], [23.258641453948517, 77.38312867039713], [23.258276747357726, 77.38301065320047], [23.258197891747447, 77.38275316113504], [23.25836545986354, 77.38251712674173], [23.258542884698052, 77.38238838070902], [23.259410291600748, 77.38131549710306], [23.26018898162586, 77.38083269948038], [23.260681821063244, 77.38060739392313], [23.260849386056847, 77.38028552884134], [23.2610070940937, 77.37966325634989], [23.260612823651712, 77.37935212010416], [23.260179124818528, 77.37871911877664], [23.26018898162586, 77.37738874310526], [23.259873563429622, 77.37718489522013], [23.259794708763945, 77.37599399441751], [23.259755281413607, 77.37274315709146], [23.259962274872766, 77.37142351025614], [23.259666569832724, 77.3709299837974], [23.258749880039854, 77.3709299837974], [23.258434458438355, 77.371938494387], [23.25794161069187, 77.37243202084574], [23.257527617176724, 77.3727324282554], [23.256827768072675, 77.37216379994425], [23.256699626289503, 77.37163808697733], [23.256778482786025, 77.3707154070762], [23.25709390830572, 77.36865547055277], [23.25667005509127, 77.3643210207847], [23.256906624493407, 77.36367729062113], [23.25728119185494, 77.36321595067056], [23.25810917913012, 77.36287262791666], [23.258956875060232, 77.36301210278543], [23.25962714244449, 77.36434247845682], [23.261440790232854, 77.36369874829325], [23.26459490151867, 77.35921409482035], [23.268133331266753, 77.3603406226066], [23.27044952269547, 77.35925701016458], [23.26857686040193, 77.35815194005045], [23.26869513458863, 77.3574223791984], [23.27147454775133, 77.35643532628092], [23.272814953232093, 77.35405352467569], [23.273603420744116, 77.35374238842996], [23.27347529509099, 77.35129621380838], [23.26742368157959, 77.3513713156608], [23.266329630907173, 77.34983709210428], [23.262889719373813, 77.34974053257974], [23.26204204845505, 77.34892514103922], [23.259705997209306, 77.34849598759683], [23.259232867920748, 77.3478951727775], [23.258651310869563, 77.34746601933512], [23.258533027768998, 77.34710123890909], [23.259834136102622, 77.34659698361429], [23.26073110490676, 77.34668281430277], [23.261992765096263, 77.34758403653177], [23.26249545450083, 77.3468866621879], [23.262229325052232, 77.34485891217264], [23.262643303964868, 77.343303230944], [23.263934515646536, 77.34263804310831], [23.26349097105956, 77.3413934981254], [23.26119848043881, 77.34112527722391], [23.261139340031782, 77.33912971371683], [23.26075492674647, 77.33829286450418], [23.260636645512555, 77.33699578342713], [23.261188623706133, 77.33515042362488], [23.26171102953388, 77.33525771198548], [23.262272859931358, 77.33464616833008], [23.263633071085717, 77.33488220272339], [23.263524648966644, 77.33441013393677], [23.263702066933742, 77.33413118419922], [23.26426388893803, 77.33425993023194], [23.26433288445947, 77.33344453869141], [23.26260798570745, 77.3333157926587], [23.262312286536982, 77.33271497783936], [23.26288397100798, 77.33213562069214], [23.263928767325766, 77.33210343418396], [23.264411736440238, 77.33183521328247], [23.264934129634405, 77.3321999937085], [23.269339892651434, 77.32824105320252], [23.26900478380475, 77.32611674366272], [23.26788117740342, 77.32570904789246], [23.264182147765236, 77.32520989494928], [23.260929459225483, 77.322817364508], [23.261244874923086, 77.32133678513178], [23.25995363718446, 77.31938413696894], [23.2624473904227, 77.31808594780573], [23.264803106553163, 77.31558612900385], [23.263344341640675, 77.31535009461054], [23.26249426083723, 77.31340292272525], [23.263864326267523, 77.31225493726687], [23.265293516203123, 77.30977657613711], [23.264249447704838, 77.30686136316189], [23.26292866926457, 77.30719395707973], [23.260661630980252, 77.30590649675258], [23.259951941505633, 77.30372854303249], [23.259045110567154, 77.30310627054104], [23.258611406633225, 77.30108924936184], [23.2593703875916, 77.29905077051052], [23.259429528783496, 77.29753800462612], [23.25787213531151, 77.2961647136105], [23.25761585362968, 77.2944373710049], [23.25661043612016, 77.29340740274318], [23.25744828457133, 77.29053207467922], [23.255338867822914, 77.2900600058926], [23.256245723972988, 77.28674479555019], [23.253815538807324, 77.28547794777339], [23.25232708148967, 77.28544576126521], [23.25223836496593, 77.2836433168072], [23.251035757376755, 77.28121859985774], [23.249606414579567, 77.27922303635066], [23.252900753425767, 77.27552909322911], [23.25225532936966, 77.27367249595851], [23.248479894195732, 77.27139798271388], [23.24873619343772, 77.26897326576442], [23.247563127490764, 77.26835099327296], [23.24509866962702, 77.26934010334901], [23.243331852715343, 77.26684614394802], [23.242541515912762, 77.26333781455654], [23.241230380641372, 77.26357384894985], [23.241004702835557, 77.26196490850613], [23.239368227440828, 77.26110660162136], [23.23869785823103, 77.25986205663845], [23.23739654367992, 77.25999080267117], [23.23593421300107, 77.2582849177377], [23.234504708392336, 77.25975476827786], [23.234554001909604, 77.26116024580166], [23.232761790196488, 77.26237321404831]]

        # Create a Folium map
        m = folium.Map(location=[23.253257274034894, 77.33295226843963], zoom_start=12.4)

        # Add a marker to the map
        #folium.Marker([42.363600, -71.099500], popup="My Marker").add_to(m)

        # Add a polygon to the map using the shape tuple
        folium.Polygon(locations=shape_tuple, color='blue', fill_opacity=0.3).add_to(m)

        # Render the map in Streamlit
        folium_static(m)

    
    elif chart_select == 'Lower lake' :
        df = pd.read_csv('merged_data_lowerlake.csv')
        st.subheader('Lower Lake')
        
        shape_tuple = [[23.250243717639034, 77.39732060396913], [23.249893774429964, 77.39740107023958], [23.249706480504194, 77.39753518069033], [23.249558616692784, 77.39780340159182], [23.249529043910826, 77.39800724947695], [23.249499471122306, 77.39816281759981], [23.248784793405754, 77.39936444723848], [23.248587640258254, 77.39988479578737], [23.2484496328816, 77.40026030504946], [23.24816376000422, 77.40059826338533], [23.248015894482386, 77.4007001873279], [23.247399786376853, 77.40208957159761], [23.247325853212928, 77.40240070784334], [23.24703012014743, 77.40284059012178], [23.24702026236729, 77.40313026869539], [23.246616092754127, 77.40451428854708], [23.24640907857553, 77.40479860270266], [23.246157703783876, 77.40480396712069], [23.245788034112014, 77.40456256830934], [23.245447937109045, 77.40421924555544], [23.245206418420977, 77.40376863444094], [23.244826888170486, 77.4028620477939], [23.244531149564395, 77.40251336062197], [23.244299487198337, 77.40235242808107], [23.24419597835155, 77.40214858019594], [23.244102327420972, 77.40209493601564], [23.244087540425916, 77.40203056299929], [23.243969244406507, 77.40192863905672], [23.243984031414666, 77.40183207953218], [23.243698148966363, 77.40171406233553], [23.243407336881734, 77.4016014095569], [23.243141169333352, 77.40142974817995], [23.24274172553754, 77.40100403208946], [23.242638215482064, 77.40098793883537], [23.242475556661145, 77.40131516833519], [23.2425149891208, 77.4018033303759], [23.242786086965314, 77.40243633170341], [23.24308182944011, 77.4028493918917], [23.24328884878238, 77.40349312205528], [23.243466293677198, 77.40375061412071], [23.2436930284771, 77.40383644480919], [23.24374231859998, 77.4039276399157], [23.243658525380237, 77.40400274176811], [23.24370781551588, 77.404163674309], [23.24425986379083, 77.40518827815269], [23.244762620053503, 77.40597684760307], [23.245063287109065, 77.40644891638969], [23.245689263886522, 77.40713019747947], [23.246068791683307, 77.40741987605308], [23.24619694368251, 77.40766127486442], [23.24618708584078, 77.4079080380938], [23.24599485778162, 77.40831036944603], [23.245989928853383, 77.40857322592949], [23.246118080928344, 77.40868051429008], [23.246660261421564, 77.40870733638023], [23.246857417418124, 77.40862687010979], [23.247103862004007, 77.4086483277819], [23.247222155243495, 77.40857322592949], [23.247374950522545, 77.40872879405235], [23.248859777823114, 77.40899202314316], [23.249106218709095, 77.40926560846268], [23.249263940637128, 77.40954992261825], [23.24990468405166, 77.4098825165361], [23.250195481970312, 77.41014537301956], [23.250195481970312, 77.41051015344559], [23.250471492967566, 77.4107998320192], [23.250944653348064, 77.4104404160112], [23.25146217059193, 77.41049942460953], [23.251614961013246, 77.41077837434707], [23.25161988973359, 77.4117922493547], [23.25166917692712, 77.41190490213333], [23.251516386567918, 77.4126022764772], [23.251338952382703, 77.41279539552627], [23.251107301841135, 77.41347667661606], [23.25113687427309, 77.41383072820602], [23.251334023651964, 77.41395947423874], [23.251565673799693, 77.41387364355026], [23.251950113582307, 77.41387900796829], [23.252871778803744, 77.41265055623947], [23.253152712925235, 77.41214630094467], [23.25370965074959, 77.41161522355972], [23.254059583944773, 77.4115401217073], [23.254606660761798, 77.40915295568405], [23.25434051556363, 77.40908858266769], [23.25434051556363, 77.40888473478256], [23.25399058310574, 77.40869698015152], [23.253744151246266, 77.40871307340561], [23.25349771893132, 77.40855214086471], [23.253325216039862, 77.40813908067642], [23.253078782950656, 77.40796205488144], [23.25274894102829, 77.40798351255356], [23.252719368953816, 77.40773138490616], [23.252512364248943, 77.4076133677095], [23.2522905731371, 77.4072539517015], [23.251960350131522, 77.40700718847214], [23.25153155187405, 77.40635809389053], [23.251274092196805, 77.40561819366091], [23.250564352749844, 77.40558600715273], [23.25037213099957, 77.40562355807894], [23.25020948160985, 77.40522122672671], [23.250288341944778, 77.40517831138247], [23.249785606510578, 77.40379965594882], [23.249608170022473, 77.40371382526034], [23.249820108022504, 77.40337050250643], [23.249711674669214, 77.40323102763766], [23.24980532166135, 77.40280187419528], [23.249731389830927, 77.40263557723635], [23.250061618356128, 77.401310565983], [23.24996304276258, 77.40102625182742], [23.250367202233093, 77.3995993166315], [23.2503573446996, 77.39930963805789], [23.25086007797847, 77.39856398395175], [23.25093893792868, 77.3980329065668], [23.25072700170674, 77.39779150775546], [23.250243717639034, 77.39732060396913]]

        # Create a Folium map
        m = folium.Map(location=[23.250243717639034, 77.39732060396913], zoom_start=15)

        # Add a marker to the map
        #folium.Marker([42.363600, -71.099500], popup="My Marker").add_to(m)

        # Add a polygon to the map using the shape tuple
        folium.Polygon(locations=shape_tuple, color='blue', fill_opacity=0.3).add_to(m)

        # Render the map in Streamlit
        folium_static(m)

    # add a checkbox to show/hide dataset
    show_data = st.sidebar.checkbox("Show dataset")
    
    if show_data:
        st.write(df)

    global numeric_columns
    try:
        numeric_columns  = list(df.select_dtypes(['float','int' ]).columns)
    except Exception as e:
        print(e)
        

    # add a select widget to the sidebar
    chart_select = st.sidebar.selectbox(
        label = "Select the Chart Type",
        options = ['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
    )

    if chart_select == 'Scatterplots':
        st.sidebar.subheader('Scatterplot Settings')
        try:
            x_values = st.sidebar.selectbox('X axis', options = numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options = numeric_columns)
            plot = px.scatter(data_frame = df, x = x_values, y = y_values)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Lineplots':
        st.sidebar.subheader('Lineplots Settings')
        try:
            x_values = st.sidebar.selectbox('X axis', options = numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options = numeric_columns)
            plot = px.area(data_frame = df, x = x_values, y = y_values)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Boxplot':
        st.sidebar.subheader('Boxplot Settings')
        try:
            x_values = st.sidebar.selectbox('X axis', options = numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options = numeric_columns)
            plot = px.box(data_frame = df, x = x_values, y = y_values)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Histogram':
        st.sidebar.subheader('Histogram Settings')
        try:
            x_values = st.sidebar.selectbox('Select the variable to plot histogram', options = numeric_columns)
            bins = st.sidebar.slider("Select the number of bins", min_value=5, max_value=50, value=20, step=1)
            plot = px.histogram(data_frame = df, x = x_values, nbins=bins)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

if selected == "Contributors":

    st.subheader("Contributors")


    st.write("Project Leads-  [Vaasu Bisht](https://github.com/vaasu2002) and [Eeman Majumder](https://github.com/Eeman1113)")
    contributors = """

    Project Contributors in aplhabetical order:

    1.	Aditya Bhate
    2.	Aiswarya Jyothirmayi Devi
    3.	Akshit Srivastava 
    4.	Ameya Sharma
    5.	Ananya Mohanty 
    6.	Ananya Tiwari
    7.	Aniruddha Kumar
    8.	Astha Srivastava 
    9.	Ayushka Behere
    10.	Dhruvil Jain
    11.	Kshitij Singh
    12.	Mansuriya Raj Kalpeshbhai
    13.	Muskaan Bahri
    14.	Navneet Lamba 
    15.	Pranav Pratyush
    16.	Punya Saraogi
    17.	Pushpendra Kushwaha
    18.	Qurat Ul Aaein 
    19.	Reem Abdel-Salam
    20.	Rishit Chugh 
    21.	Rishita Bansal 
    22.	Sayan Kumar
    23.	Shilpa Gollamudi
    24.	Sourav Dutta 
    25.	Srijeeta Mukherjee
    26.	Wallace Ferreira
    """

    st.text(contributors)



if selected == "Dashboards":

    st.write("Turbidity vs DOM vs Salinity vs SPM - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/Book2_16791413197210/TurbidityvsDOMvsSalinityvsSPM?publish=yes)")
    st.write("Cholorphyll vs PH vs DO - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/ChyllvspHvsDO/CholorphyllvsPHvsDO?publish=yes)")
    st.write("pH v Salinity - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/pHvsSalinity/pHvSalinity_1?publish=yes)")
    st.write("Salinity - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/Salinity_16791415299290/Dashboard4?publish=yes)")
    st.write("Dissolved Oxygen - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/DissolvedOxygen/Dashboard3?publish=yes)")
    st.write("Turbidity - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/Turbidity_16791417059980/Dashboard2?publish=yes)")
    st.write("Chlorophyll - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/Chlorophyll/Dashboard1?publish=yes)")
    st.write("Monsoon Analysis Chlorophyll - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/Book1_16790547280580/MonsoonAnalysisChyllA?publish=yes)")
    st.write("Monsoon Analysis Turbidity - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/Tub/MonsoonAnalysisturbidity?publish=yes)")
    st.write("Monsoon Analysis pH - [link](https://public.tableau.com/app/profile/akshit.srivastava/viz/pHSalTemp/MonsoonAnalysispH?publish=yes)")
    st.write("Lendiya Lake (Dissolved Oxygen v Chlorophyll v Turbidity) [link](https://public.tableau.com/views/OmdenaBhopal-LendiyaLake/DOvsCvsTurb?:language=en-US&:display_count=n&:origin=viz_share_link)")
    st.write("Lendiya Lake (Drinking Water Quality) [link](https://public.tableau.com/views/OmdenaBhopal-LendiyaLake/DrinkingWaterQuality?:language=en-US&:display_count=n&:origin=viz_share_link)")
    st.write("Lendiya Lake (Temperature) [link](https://public.tableau.com/views/OmdenaBhopal-LendiyaLake/Temperature-Dash?:language=en-US&:display_count=n&:origin=viz_share_link)")




    st.write("Kaliyasot Dam Visualization Tool -  [link](https://papichoolo-eda-stream-kvsv2x.streamlit.app/)")



    
