#module to work with xml files
import xml.etree.ElementTree as ET
#module for working with times
import datetime
#module to work with operating system
import os


# Directory of Xml file being parsed
tree = ET.parse(r"C:\Users\adeye\Desktop\Plan B\TVGuide.xml")
root = tree.getroot()

print("The python script to parse data is running.\n")
# Getting directory of images folder
img_dir = os.path.join(os.getcwd(),'imgs\\')

# Dictionary to add image to channel id
idict = {
    '1101': 'TAO.jpg',
    '1102': 'RTE2.png',
    '1103': 'VM1.png',
    '1104': 'TG4.jpg',
    '1105': 'RTEN.png',
    '1106': 'VM2.png',
    '1226': 'RTER1.jpg',
    '1227': 'RTE2FM.png',
    '1228': 'RTELFM.jpg',
    '1229': 'RTERNG.jpg',
    '1230': 'RTER1E.jpg',
    '1231': 'RTEP.png',
    '1232': 'RTE2XM.png',
    '1233': 'RTEJR.jpg',
    '1234': 'RTEG.jpg',
    '2101': 'RTE1.jpg',
    '2102': 'RTE21.png',
    '2103': 'VM3.png',
    '2107': 'VM4.png',
    '2108': 'CHAL.png',
    '2111': 'RTE11.png',
    '2117': 'RTEJR.jpg',
    '2118': 'SKY.png',
    '2120': 'SAOR.png',
    '2130': '2RN.png',
    '2241': 'RMI.jpg',
    '2242': 'UCB.jpg',

}

# Create a dictionary with the combined paths of channel images
channel_img = {}
for channel_id, img_filename in idict.items():
    img_path = os.path.join(img_dir, img_filename)
    channel_img[channel_id] = img_path
# Variable for background image
bg_dir = os.path.join(os.getcwd(),'imgs\\BG.jpg')
#css styling of table
css = """
<style>
h1 {
    font-size: 40px;
    color: #ffff;
    display: inline-block;
    backdrop-filter: blur(1px);
    border-radius: .4rem;
}
body{
    background: url(imgs/BG.jpg) center / cover;
    background-repeat: cover;
    background-size: contain;
    
   }
table{
    background-color: #fff5;
    backdrop-filter: blur(4px);
    box-shadow: 0.4rem .4rem #0005;
    border-radius: .8rem;
}
table th{
    font-size: 20px;
    background-color: #fff4;
    padding: .6rem 1rem;
    }
table tr.header,table tr:hover {
  background-color: #f1f1f1a6;
  
}
th.channel-id {
    text-align: center;
}
th.channel-title {
    text-align: left;
    }
th.des {
    text-align: left;
    }
th.rating {
    text-align: left;
    }
td.channel-id {
    text-align: center;
    }

img.channel-icon {
        display: flex;
        height: 50px;
        width: 50px;
        margin-right:.5rem;
        vertical-align: middle;
    }
td.channel-lg {
    display: flex;
    align-items: center;
    }

td.start-time {
    text-align:center;
    }
    
td.stop-time {
    text-align:center;
    }
td.channel-title {
    text-align: left;
    }
td.timezone {
    text-align: center;
    }
td.rating {
    text-align: left;
    padding-left: 50px;
    
    }
#ch_input {
  background-image: url('https://cdn3.iconfinder.com/data/icons/linecons-free-vector-icons-pack/32/search-512.png');
  background-position: 5px;
  background-repeat: no-repeat;
  background-size: 35px 35px;
  width: 19%; 
  font-size: 16px; 
  padding: 12px 20px 12px 50px; 
  border: 1px solid #ddd; 
  margin-bottom: 12px; 
  border-radius: .2rem;
    }
</style>
"""
# Table creation
table = '<title> EPGdata</title>'
table+='<h1>See below a table of the EPG data that has been obtained via the tuner</h1>\n<br></br>'
table+= '<input type="text" id="ch_input" onkeyup="func()" placeholder="Search for a channel using the channel name/id ..." title="search"><br></br><br></br>'
table += '\n<table id="ch_table">\n<tr><th class="channel-id">Channel ID</th><th>Channel Logo and Name</th><th>Start Time</th><th>Stop Time</th><th>Time Zone</th><th class="channel-title">Program Title</th><th class="rating">Parental Rating</th><th class="des">Program Description</th></tr>\n'
for programme in root.findall('programme'):
    #Loop through all programme elements in Xml file and parse the inputted fields
    # Get the channel ID for this programme
    channel_id = programme.attrib['channel']
    # Find the corresponding channel element
    channel = root.find(f"channel[@id='{channel_id}']")
    # Get the display name of the channel
    display_name = channel.find('display-name').text
    # Get the icon URL
    icon_url = channel_img.get(channel_id, '')
    # Get the start and stop times into date,time and timezone
    start_time = programme.attrib['start']
    stop_time = programme.attrib['stop']
    start_year = start_time[:4]
    start_month = start_time[4:6]
    start_day = start_time[6:8]
    start_hour = start_time[8:10]
    start_minute = start_time[10:12]
    start_timezone = start_time[15:]
    stop_year = stop_time[:4]
    stop_month = stop_time[4:6]
    stop_day = stop_time[6:8]
    stop_hour = stop_time[8:10]
    stop_minute = stop_time[10:12]
    start_time_obj = datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_hour),int(start_minute))
    stop_time_obj = datetime.datetime(int(stop_year), int(stop_month), int(stop_day), int(stop_hour), int(stop_minute))
    start_time_parse = start_time_obj.strftime('%H:%M %Y/%m/%d')
    stop_time_parse = stop_time_obj.strftime('%H:%M %Y/%m/%d ')
    # Get the title and description of the programme
    title = programme.find('title').text
    description = programme.find('desc').text
    # Get the rating of the programme
    rating = programme.find('rating/value').text
    table += f'<tr><td class="channel-id">{channel_id}</td><td class="channel-lg"><img src="{icon_url}" alt="" class="channel-icon">{display_name}</td><td class="start-time">{start_time_parse}</td><td class="stop-time">{stop_time_parse}</td><td class="timezone">{start_timezone}</td><td class="channel-title">{title}</td><td class="rating">{rating}</td><td>{description}</td></tr>\n'
    # Javascript code to filter by channel name/id
    script= '<script>\n function func(){\n var input,filter,table,tr,td,i,txt;\n'
    script+= ' input = document.getElementById("ch_input");\n filter = input.value.toUpperCase();\n'
    script+= ' table = document.getElementById("ch_table");\n tr = table.getElementsByTagName("tr")\n\n'
    script+='for( i=0; i<tr.length; i++){\n'
    script+='   td = tr[i].getElementsByTagName("td")[0];\n'
    script +='      if(td){\n'
    script+='           txt = td.textContent || td.InnerText;\n'
    script+='               if(txt.toUpperCase().indexOf(filter) > -1){\n'
    script+='                   tr[i].style.display = "";\n'
    script+='               }else{\n'
    script+='                   tr[i].style.display ="none";\n'
    script+='               }\n'
    script+='           }\n'
    script+='       }\n'
    script+='for( i=0; i<tr.length; i++) {\n'
    script+='   td = tr[i].getElementsByTagName("td")[1];\n'
    script+='       if(td){\n'
    script+='           txt=td.textContent || td.innerText;\n'
    script+='           if(txt.toUpperCase().indexOf(filter) > -1){\n'
    script+='               tr[i].style.display ="";\n'
    script+='            }\n'
    script +='        }\n'
    script +='     }\n'
    script +='  }\n'
    script+= '</script>'
    # Storing all data within html varaible
    html = f"<!DOCTYPE html><html>\n<head>{css}</head>\n<body>{table}{script}</body>\n</html>"
    # Write data to html file
    with open('EPGdata.html', 'w') as f:
        f.write(html)



