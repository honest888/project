 
import re
import os,csv ,json
from datetime import datetime

BATTERY_THRESHOLDS = [
    #{"percent": 50, "color": "#71cb72"},
    #{"percent": 30, "color": "#f6d756"},
    #{"percent": 0, "color": "#f23a3a"},
    {"measure": 13.00, "percent": 100, "color": "#71cb72"},
    {"measure": 12.75, "percent": 90, "color": "#71cb72"},
    {"measure": 12.50, "percent": 80, "color": "#71cb72"},
    {"measure": 12.30, "percent": 70, "color": "#71cb72"},
    {"measure": 12.15, "percent": 60, "color": "#71cb72"},
    {"measure": 12.05, "percent": 50, "color": "#71cb72"},
    {"measure": 11.95, "percent": 40, "color": "#f6d756"},
    {"measure": 11.81, "percent": 30, "color": "#f6d756"},
    {"measure": 11.66, "percent": 20, "color": "#f23a3a"},
    {"measure": 11.51, "percent": 10, "color": "#f23a3a"},
    {"measure": 11.50, "percent": 0, "color": "#f23a3a"}
]




import numpy,json


class RGB(numpy.ndarray):
    @classmethod
    def from_str(cls, rgbstr):
        return numpy.array([
        int(rgbstr[i:i+2], 16)
        for i in range(1, len(rgbstr), 2)
        ]).view(cls)
    
    def __str__(self):
        self = self.astype(numpy.uint8)
        return '#' + ''.join(format(n, 'x') for n in self)
 
 
def getHalfwayColor(c1,c2):
    c1 = RGB.from_str(c1) 
    c2 = RGB.from_str(c2)
    
    return ((c1 + c2) / 2)
     

class ConfigFileReader():
    def __init__(self):
        self.file_path =  None
        path_options = [
            # os.path.join(os.getcwd(), 'config.json') ,
            os.path.join('home/pi/savvyvan', 'proj','webapp', 'config.json') ,
            os.path.join('/home/pi/savvyvan', 'proj','webapp', 'config.json') , 
            os.path.join(os.getcwd(), 'config.json') ,
        ]
        for path in path_options:
            if os.path.exists(path):
                self.file_path = path
            else: 
                pass
                # print("* Path Not Found")
        
        self.data = self.readFile()
    def readFile(self):
        
        return json.loads(open(self.file_path, 'r', encoding="utf-8").read() ) 
    def updateDataFile(self, new_data):
        with open(self.file_path, 'w') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        
        

    def getBaseFolderPath(self):
        base_folder_path = self.data['base_folder_path'].encode('unicode_escape').decode() 
        if not os.path.exists(base_folder_path):
            print("*** In-Valid base_folder_path")
        return  base_folder_path
    
    def getGPIOStatFolderPath(self):
        required_path = os.path.join(ConfigFileReader().getBaseFolderPath(),self.data['gpio_stat_folder_path'])
        return required_path.encode('unicode_escape').decode() 
    
    
    def getBatteryDataFilePath(self):
        required_path =  os.path.join(ConfigFileReader().getBaseFolderPath(),self.data['battery_file_path'])
        return required_path.encode('unicode_escape').decode() 
    
    def getBatteryRefreshInterval(self):
        return self.data['battery_status_refresh_interval']
    
    
    def getMenuFolderPath(self):
        menu_folder_path = os.path.join(self.getBaseFolderPath(),self.data['menu_folder_path'])
        if not os.path.exists(menu_folder_path):
            print("*** In-Valid menu_folder_path")
        return  menu_folder_path
    
    def getMenuPythonFiles(self):
        menu_folder_path = self.getMenuFolderPath()
        python_files = []
        if os.path.exists(menu_folder_path):
            python_files = [x for x in  os.listdir(menu_folder_path) if str(x).endswith(".py")]
        return python_files
    
    
            
    def getMenuPythonFilePath(self, file_name): 
        require_path = os.path.join(self.getMenuFolderPath(), file_name )
        if os.path.exists(require_path):
            return str(require_path).encode('unicode_escape').decode() 
        else:
            return None
     
    def getMappedPythonFilePath(self, file_path):
        if file_path in self.getPythonFileListing():
            require_path = os.path.join(self.getBaseFolderPath(), file_path )
            if os.path.exists(require_path):
                return str(require_path).encode('unicode_escape').decode() 
        return None
    
    
    def getBackgroundColor(self):
        return self.data['background_color'] 
    

            
    def getTotalTilesToDisplay(self):
        return int(self.data['total_title_to_display'])    
     
    def setTotalTilesToDisplay(self, new_count):
        self.data['total_title_to_display'] = int(new_count)     
        self.updateDataFile(self.data)
    
    def getImagesFolderPath(self):
        return os.path.join(self.getBaseFolderPath(), self.data['images_folder_path'])
            
    def getImagesList(self):
        return os.listdir(self.getImagesFolderPath())
    
    
    
    def getImagePath(self, file_name):
        if file_name in self.getImagesList():
            require_path = os.path.join(self.getImagesFolderPath(), file_name )
            if os.path.exists(require_path):
                return str(require_path).encode('unicode_escape').decode() 
        return None
    
    def getPythonFileListing(self):
        return list(self.data['mapped_python_files'])   
    


    def getTilesListing(self):
        for index,x in enumerate(self.data['tiles']):
            self.data['tiles'][index]['tile_icon'] = self.data['tiles'][index]['tile_icon'].encode('unicode_escape').decode()  
         
        return list(self.data['tiles'])      
          
            
            
    def setTileIcon(self,index,file_name): 
        # self.data['tiles'][index]['tile_icon'] = self.getImagePath(file_name)
        self.data['tiles'][index]['tile_icon'] = file_name
        self.updateDataFile(self.data)
        return list(self.data['tiles'])  
    
    
    def set_is_active_tile(self,index,state): 
        self.data['tiles'][index]['is_active_tile'] = int(state)
        self.updateDataFile(self.data) 
    
    
     
            
            
    def setTileName(self,index,tile_name): 
        # self.data['tiles'][index]['tile_icon'] = self.getImagePath(file_name)
        self.data['tiles'][index]['tile_name'] = tile_name
        self.updateDataFile(self.data)
        return list(self.data['tiles'])   
    
       
       
    def setTileMappedPythonFile(self,index,file_name):  
        self.data['tiles'][index]['tile_file_mapping'] = file_name
        self.updateDataFile(self.data)
        return list(self.data['tiles'])   
    
    
    def get_weather_data(self): 
        return json.loads(self.data['weather_data'])   
    
    
    def set_weather_data(self,weather_data):   
        self.data['weather_data'] = json.dumps(weather_data)
        self.updateDataFile(self.data) 
    
    
    
    
    def getWifiFilePath(self):
        file_path = os.path.join(self.getBaseFolderPath(),  self.data['wifi_file_path']).encode('unicode_escape').decode()
        if not os.path.exists(file_path):
            print("*** Invalid Wifi Settings File Path")
        return  file_path
       
    def getAvaliableTileNames(self) :
        return [x['tile_name'] for x in self.data['avaliable_tiles']]
            
            
    def getAvaliableTileIcons(self) :
        return [x['tile_icon'] for x in self.data['avaliable_tiles']]

    def getSpecificTileIcon(self,tile_name): 
        return [ x['tile_icon'] for x in self.data['avaliable_tiles'] if str(tile_name) == str(x['tile_name'])][0]
            
    def getBatteryColor(self,level):
        color  = None
        range = [x for index,x in enumerate(BATTERY_THRESHOLDS) if x['percent']>=level and ((index+1)<len(BATTERY_THRESHOLDS) and BATTERY_THRESHOLDS[index+1]['percent']<=level)]
            # {"measure": 11.51, "percent": 10, "color": "#f23a3a"},
        # if not range:
        #     range = [x]    
        if len(range)>1:
            color = getHalfwayColor(range[0]['color'],range[-1]['color'])
        elif range:
            color = range[0]['color']
        return color
    
    def getTilesBackgroundColorClasses(self):
        return [
            self.data['tile_bg_class'],
            self.data['tile_shade_1'],
            self.data['tile_shade_2'],
        ]
    
    
    def setBackgroundColor(self, new_colors):
        self.data['background_color']  = new_colors
        self.data['tile_bg_class'] = new_colors['base_class']
        self.data['tile_shade_1'] = new_colors['shade1_class']
        self.data['tile_shade_2'] = new_colors['shade2_class']
        
        self.updateDataFile(self.data)
    
    def getAllColorClasses(self):
        return     {
            'avaliable_base_color_classes':self.data['avaliable_base_color_classes'],
            'avaliable_shade1_classes':self.data['avaliable_shade1_classes'],
            'avaliable_shade2_classes':self.data['avaliable_shade2_classes'],
            }
         
    
    def getChartData(self):
        battery_graph_file_path = os.path.join(self.getBaseFolderPath(),self.data['battery_graph_file_path'])
        data = open(battery_graph_file_path,'r',encoding="utf-8").read().split('\n')[ :] 
        data = [x for x in data if len(str(x))>10]
        # if len(data)>30:
        #     data = data[:30]
            
        data = [
            [
                x.split(" -> ")[0].split(" ")[-1].split(".")[0],
                x.split(" -> ")[-1]
            ]
            for x in data]
        
        data = {
            "labels": [str(x[0]) for x in data ],
            "dataset": [float(x[1]) for x in data[:]  ],
        }
         
        print("Graph Dataset")
        # print(data)
        return data
    
    def getParagraphText(self):
        required_path =  os.path.join(self.getBaseFolderPath(),self.data['settings_page_text_file_path']).encode('unicode_escape').decode()  
        data = str(open(required_path, 'r', encoding="utf-8").read())
        return data
        
    def setBatteryTileDisplayStatus(self,status):
        self.data['battery_tile_display_status'] = str(status).capitalize()
        self.updateDataFile(self.data)
    
    
    def set_weather_widget_display_status(self,status):
        self.data['weather_widget_display_status'] = str(status).capitalize()
        self.updateDataFile(self.data)
    
    
    
    def getBatteryTileDisplayStatus(self): 
        status = str(self.data['battery_tile_display_status']).capitalize()
        if status=='False':
            return False
        return True
    
    
    def get_weather_widget_display_status(self): 
        status = str(self.data['weather_widget_display_status']).capitalize()
        if status=='False':
            return False
        return True
    
    
        
    def getBatteryMinMax(self):
        return [
            self.data['battery_min'],
            self.data['battery_max']
        ]
    
    
    def getBatteryFlashValue(self):
        return float(self.data['battery_flash'])
    
    def get_weather_data_api_key(self):
        return self.data['weather_data_api_key']
    
    def display_external_link_icon(self): 
        status = str(self.data['display_external_link_icon']).capitalize()
        if status=='False':
            return False
        
        return True
         
    def getMaxTotalTilesToDisplay(self):
        return [x for x in range(1,int(self.data['max_total_title_to_display'])+1)] 
    
    def get_geo_location_city(self):
        return self.data['geo_location_city']
            
    def set_geo_location_city(self,city ):
        self.data['geo_location_city'] = city
        self.updateDataFile(self.data)
            
    def get_wifi_settings_page_run_py_file(self):
        path = os.path.join(self.getBaseFolderPath(),self.data['wifi_settings_page_run_py_file']).encode('unicode_escape').decode()  
        # return self.data['wifi_settings_page_run_py_file']
        return path
            
            
            
            
    def generateBatteryLevel(self, battery_level): 
        # print("battery_level = ",battery_level)
        min_max = [x['measure'] for x in BATTERY_THRESHOLDS]
        min_max = [
            min(min_max),
            max(min_max),
        ]
        start_range = [x['percent'] for x in BATTERY_THRESHOLDS[::-1] if x['measure']>=battery_level] 
        end_range = [x['percent'] for x in BATTERY_THRESHOLDS   if x['measure']<=battery_level] 
        if start_range : start_range=start_range[0] 
        if end_range : end_range=end_range[0] 
        # print(start_range)
        # print(end_range)
        if battery_level<min_max[0]:
            percentage = 0
        elif battery_level>min_max[1]:
            percentage = 100
        else:
            percentage = (start_range+end_range)/2 
        return {
            "battery_level":battery_level,
            "percentage":percentage
        } 
  
  
            
class WPA_Supplicant_Reader():
    def __init__(self): 
        self.file_path = ConfigFileReader().getWifiFilePath() 
        self.data = self.readFile()
    def readFile(self):
        content = open(self.file_path, 'r', encoding="utf-8").read()  
        return content
    
    def updateDataFile(self, new_data):
        with open(self.file_path, 'w') as f:
            f.writelines(new_data)
            
    def getNetwrokList(self):
        networks = self.data.replace(' =','=').replace('= ','=')
        networks = networks.split("network=")[1:]
        return networks
    def getNetworkSSID(self):
        networks = self.getNetwrokList()
        ssids = []
        for x in networks:
            for y in x.split("\n"):
                y = y.strip()
                if 'ssid=' in y:
                    ssids.append(y.replace('ssid=','')[1:-1]) 
        ssids = dict.fromkeys(ssids)
        return ssids
    
    def deleteGivenSSID(self,ssid):
        networks = self.getNetwrokList()
        # print(len(networks) )
        networks = ['network='+(x) for x in networks if str(ssid) not in str(x)]
        new_data =  self.data.replace(' =','=').replace('= ','=')
        new_data = "".join(new_data.split("network=")[:1]) + "".join( networks)
        self.data = new_data
        self.updateDataFile(self.data) 
        
        
    def addNewNetwrok(self,ssid,password):
        network =  """network={{\nssid="{}"\npsk="{}"\n}}\n""".format(ssid,password)
        self.data =  self.readFile() + "\n" + network
        self.updateDataFile(self.data) 
        

if __name__ == '__main__':
    reader = ConfigFileReader() 
    print(reader.getBatteryFlashValue()) 