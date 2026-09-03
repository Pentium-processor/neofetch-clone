import argparse,json,distro,platform,os,psutil
from time import sleep

def convert_to_GB(mem_value):

    convert = lambda int_value:round(int_value/1e+6,2)
    return convert(mem_value)


parser=argparse.ArgumentParser()

tux_logo = '''
                          .88888888:.
                         88888888.88888.
                       .8888888888888888.
                       888888888888888888
                       88' _`88'_  `88888
                       88 88 88 88  88888
                       88_88_::_88_:88888
                       88:::,::,:::::8888
                       88`:::::::::  8888
                      .88  `::::'    8:88.
                      8888            `8:888.
                    .8888'             `888888.
                   .8888:..  .::.  ...:'8888888:.
                 .8888.'     :'     `'::`88:88888
                .8888        '         `.888:8888.
               888:8         .           888:88888
             .888:88        .:           888:88888:
            8888888.       ::           88:888888
            `.::.888.      ::          .88888888
           .::::::.888.    ::         :::`8888'.:.
          :::::::::.888   '         .::::::::::::
           ::::::::::::.8    '      .:8::::::::::::.
          ::::::::::::::.        .:888:::::::::::::
         :::::::::::::::88:.__..:88888:::::::::::'
         `'.:::::::::::88888888888.88:::::::::'
               `':::_:' -- '' -'-' `':_::::'`
'''

# ----CUSTOM FLAGS-----

parser.add_argument("-l","--logo",help="Displays only the logo", action="store_true")
parser.add_argument("--stdout",help="Displays the system specs without the logo to the output stream",action="store_true")
parser.add_argument("-scroll",help="scroller effect.",action="store_true")

args = parser.parse_args()

distro_info = distro.os_release_info()["pretty_name"] #Name of linux distro and version id
hardware_arch = platform.machine() # Hardware Architecture
python_version = platform.python_version() # Python Version
kernel_desc = platform.platform() # Provides Kernel Description

#If this function is not supported on your machine, the program will not display the battery percent value

if psutil.sensors_battery() is not None:

    battery_percent = str(round(psutil.sensors_battery()[0])) #Truncates the decimal value to a whole number battery percentage value
    charging_status = str(psutil.sensors_battery()[-1]) # Returns True if machine is charging

cpu_labels = ("model name","cache size","cpu cores")
mem_labels = ("MemAvailable:","MemFree:","MemTotal:")

cpu_info_file = open("/proc/cpuinfo","r").readlines()
mem_info_file = open("/proc/meminfo","r").readlines()
cpu_info_file.extend(mem_info_file)

cpu_specs,mem_specs = [],[]

for comp_info in cpu_info_file:


    if comp_info.strip().startswith(cpu_labels) == True and len(cpu_specs)<3:
        cpu_specs.append(comp_info.strip()[comp_info.index(":")+1:].strip())

    elif comp_info.strip().startswith(mem_labels) == True and len(mem_specs)<3:
        mem_specs.append(int(comp_info.strip()[comp_info.index(":")+1:comp_info.index("k")].strip()))


memory_gigabyte_values = list(map(convert_to_GB,mem_specs))

try:

 backslash_char = "\t"
 open_json_file=open("config.json","r")
 info_dict =json.loads(" ".join(open_json_file.readlines()))

 if info_dict["image_source"] is not None:
  open_logo_file = open(info_dict["image_source"],"r").readlines()

 if args.logo:

     if info_dict["color"] == None:
       exit("".join(open_logo_file))

     elif info_dict["image_source"] == None:
        exit("".join(tux_logo))

     else:
       exit(info_dict["color"]+"".join(open_logo_file))

 elif args.stdout:
     backslash_char = "\b"

 elif args.scroll:

     if info_dict["image_source"] != None:

      for line in open_logo_file:
         sleep(0.1)

         if info_dict["color"] == None:
           print(line,end="")
         else:
           print(info_dict["color"]+line,end="")

     else:

         for line in tux_logo:
             print(line,end="")
             sleep(0.01)

     exit("")



 elif info_dict["image_source"] is None:
     print(tux_logo)

 elif info_dict["color"] is None:
     print("".join(open_logo_file))

 else:
     print(info_dict["color"]+"".join(open_logo_file))

 print(backslash_char*info_dict["gap_value"]+distro_info)
 print(backslash_char*info_dict["gap_value"]+"-"*len(distro_info))

 if info_dict["display_cpu_model"]:
    print(backslash_char*info_dict["gap_value"]+cpu_labels[0]+": "+cpu_specs[0])

 if info_dict["display_cache_size"]:
    print(backslash_char*info_dict["gap_value"]+cpu_labels[1]+": "+cpu_specs[1])

 if info_dict["display_cpu_num"]:
    print(backslash_char*info_dict["gap_value"]+cpu_labels[2]+": "+cpu_specs[2])

 if info_dict["showMemAvail"]:
    print(backslash_char*info_dict["gap_value"]+mem_labels[0]+str(memory_gigabyte_values[2])+" GB")

 if info_dict["showMemFree"]:
    print(backslash_char*info_dict["gap_value"]+mem_labels[1]+str(memory_gigabyte_values[1])+" GB")

 if info_dict["showMemTotal"]:
    print(backslash_char*info_dict["gap_value"]+mem_labels[2]+str(memory_gigabyte_values[0])+" GB")

 if info_dict["display_kernel"]:
    print(backslash_char*info_dict["gap_value"]+"kernel: "+kernel_desc)

 if info_dict["display_python_version"]:
    print(backslash_char*info_dict["gap_value"]+"Python Version: "+"python "+python_version)

 if info_dict["display_os_arch"]:
    print(backslash_char*info_dict["gap_value"]+"Hardware Architecture: "+hardware_arch)

 if info_dict["display_charging_status"] and psutil.sensors_battery() is not None:
     print(backslash_char*info_dict["gap_value"]+"Charging Status: "+charging_status)

 if info_dict["display_battery_percent"] and psutil.sensors_battery() is not None:
     print(backslash_char*info_dict["gap_value"]+"Battery percent: "+battery_percent+"%")

 print("\u001b[37m")

except FileNotFoundError:

     if  os.path.exists("config.json") == False:

         exit("\u001b[31m config.json does not exist")

     if os.path.exists(info_dict["image_source"]) == False:

         exit('\u001b[31m'+f"File \'{info_dict['image_source']}\' does not exist "+'\u001b[37m')
