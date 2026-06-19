import platform
import argparse
import psutil
import json
from time import sleep
import subprocess
import distro
parser=argparse.ArgumentParser()
parser.add_argument("-l","--logo",help="Displays only the logo",
                    action="store_true")
parser.add_argument("--stdout",help="Displays the system specs without the logo to the output stream",action="store_true")
parser.add_argument("-scroll",help="scroller effect.",action="store_true")
args = parser.parse_args()
kernel=platform.platform()
physical_cpus=psutil.cpu_count(logical=False)
open_json_file=open("config.json","r")
info_dict=json.loads(" ".join(open_json_file.readlines()))
ps_logo=f'''
⠀ ⠀⠀⠀⠀⠀⠀⠀ ⣿⣷⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣤⠀⣿⣿⣿⣿⡇⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣠⣤⣶⣾⣿⣿⡿⣿⣿⣿⣿⣶⣿⣿⣿⠿⠿⢿⣶⣦⣤⡀
⢰⣿⣿⣿⡿⠛⠉⢀⣀⣿⣿⣿⣿⣿⠀  ⣀⣠⣴⣾⣿⣿⣿⠇
⠈⠻⠿⣿⣿⣿⣿⣿⠿ ⣿⣿⣿⣿⢠⣶⣾⣿⣿⡿⠿⠟⠋⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⢿⠸⠟⠛⠋⠁⠀

'''
try:
 if info_dict["image_source"] != "null":
  open_txt_file=open(info_dict["image_source"],"r")
 def output(command="",msg=""):
    result=subprocess.run(command,shell=True,text=True,capture_output=True)
    if command =="" and msg=="" :
        pass
    else:
        if command != "uptime -p":
         print("\t\t\t"+msg+result.stdout.strip())
        else:
         print("\t\t\t"+msg+result.stdout[result.stdout.index("up")+2:].strip())

 def display_sys_specs(logo="",color="\u001b[37m"):
    global info
    info=f'''
             {logo}
                           '''
    if args.scroll == True:
      for char in info:
          print(color+char,end="")
          sleep(0.001)
      else:
          print("\n")
    else:
     print(color+info)
    if args.logo == True:
        quit("")
    else:
     if info_dict["display_distro_info"] == True:
         print("\n\t\t\t"+distro.os_release_info()["pretty_name"]+"\n"+"\t\t\t"+len(distro.os_release_info()["pretty_name"])*"-")
     if info_dict["display_cpu_num"] == True:
        print("\t\t\tNumber of physical cpu cores:"+str(physical_cpus))
     if info_dict["display_kernel"] == True:
        print("\t\t\tKernel:"+kernel)
     if info_dict["display_CPU_MODEL"] == True:
        output(command="lscpu | grep -wi 'model name' | awk -F ':' '{print $2}'",msg="CPU MODEL:")
     if info_dict["display_user"] == True:
        output(command='whoami',msg="USER:")
     if info_dict["display_uptime"] == True:
        output(command="uptime -p",msg="Uptime:")
     if info_dict["display_shell"] == True:
        output(command='echo "$SHELL"',msg="Shell:")
     if info_dict["display_pwd"] == True:
        output(command='echo "$PWD"',msg="PWD:")
     if info_dict["display_python_version"] == True:
        output(command='python3 --version',msg="Python Version:")
     if info_dict["display_os_arch"] == True:
         output(command='uname -m',msg="OS ARCHITECTURE:")
     if info_dict["number_of_threads_per_core"] == True:
         output(command="lscpu | grep -wi 'per core' | awk -F ':' '{print $2}'",msg="number of threads per core:")
     if info_dict["display_clockspeed"] == True:
         output(command="lscpu | grep -wi 'cpu Mhz' | awk -F ':' '{print $2}'",msg="CPU CLOCKSPEED:")
    print("\u001b[0m")
 if __name__ == "__main__"  :
  if info_dict["image_source"] == "null" and args.stdout != True:
   display_sys_specs(logo=ps_logo,color=info_dict["Color"])
  elif args.stdout==True:
      display_sys_specs()
  else:
   display_sys_specs(logo="".join(open_txt_file.readlines()),color=info_dict["Color"])
except FileNotFoundError:
    exit('\u001b[31m'+f"File \'{info_dict['image_source']}\' does not exist "+'\u001b[37m')
