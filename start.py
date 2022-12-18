import os
import properties
import shutil
import zipfile
import datetime
import json
if os.path.exists("datapacks_list") == False:
    os.mkdir("datapacks_list")
d = datetime.date.today()
def run(serverJarName:str,JavaCwd:str,platform:bool,Xmx:int,XmxCapacityUnit:bool,Xms:int,XmsCapacityUnit:bool):
    os.chdir(JavaCwd)
    os.chdir("bin")
    if platform == "False":
        java_path = os.getcwd() + "/java"
    else:
        java_path = os.getcwd() + "\\java.exe"
    if XmsCapacityUnit == True:
        cmdXms = " -Xms"+str(Xms)+"G "
    else:
        cmdXms = " -Xms"+str(Xms)+"M "
    if XmxCapacityUnit == True:
        cmdXmx = " -Xmx"+str(Xmx)+"G "
    else:
        cmdXmx = " -Xmx"+str(Xmx)+"M "
    os.chdir("..")
    os.chdir("..")
    os.system(java_path + cmdXms + cmdXmx + "-jar " + serverJarName + " nogui")
    print("Server is down.")
    if properties.LogDelete == True:
        shutil.rmtree("logs")
    if properties.DailyBackup == True:
        create()
def zipSomeone(files):
    OutPutName = "backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip"
    f = zipfile.ZipFile(OutPutName, "w", zipfile.ZIP_DEFLATED)
    for file in files:
        f.write(file)
    f.close()
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')    
    pre_len = len(os.path.dirname(source_dir))
    for parent, _, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()
def create():
    make_zip("world","world.zip")
    files = ["world.zip"]
    if os.path.exists("world_nether"):
        make_zip("world_nether","world_nether.zip")
        files.append("world_nether.zip")
    if os.path.exists("world_the_end"):
        make_zip("world_the_end","world_the_end.zip")
        files.append("world_the_end.zip")
    zipSomeone(files=files)
    os.remove("world.zip")
    if os.path.exists("world_nether"):
        os.remove("world_nether.zip")
    if os.path.exists("world_the_end"):
        os.remove("world_the_end.zip")
    if os.path.exists("Backup"):
        pass
    else:
        os.mkdir("Backup")
    os.chdir("Backup")
    if os.path.exists("backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip"):
        os.remove("backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip")
    os.chdir("..")
    shutil.move("backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip","Backup")
while True:
    usrInput = input(">>>")
    if usrInput == "start":
        run(serverJarName=properties.JarName,JavaCwd=properties.Cwd,platform=properties.Platform,Xmx=properties.Xmx,XmxCapacityUnit=properties.XmxCapacityUnit,Xms=properties.Xms,XmsCapacityUnit=properties.XmsCapacityUnit)
    elif usrInput == "seed":
        with open("server.properties", "r") as f:
            line = f.readline()
            counts = 1
            while line:
                if counts >= properties.seedline:
                    break
                line = f.readline()
                counts += 1
            line = line[11:]
            print("Seed:"+line)
            f.close()
    elif usrInput == "removeworld":
        shutil.rmtree("world")
        if os.path.exists("world_nether"):
            shutil.rmtree("world_nether")
        if os.path.exists("world_the_end"):
            shutil.rmtree("world_the_end")
    elif usrInput == "createbackup":
        if os.path.exists("Backup"):
            pass
        else:
            os.mkdir("Backup")
        os.chdir("Backup")
        if os.path.exists("backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip"):
            os.remove("backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip")
        os.chdir("..")
        make_zip("world","world.zip")
        files = ["world.zip"]
        if os.path.exists("world_nether"):
            make_zip("world_nether","world_nether.zip")
            files.append("world_nether.zip")
        if os.path.exists("world_the_end"):
            make_zip("world_the_end","world_the_end.zip")
            files.append("world_the_end.zip")
        zipSomeone(files=files)
        os.remove("world.zip")
        if os.path.exists("world_nether"):
            os.remove("world_nether.zip")
        if os.path.exists("world_the_end"):
            os.remove("world_the_end.zip")
        shutil.move("backup-"+str(d.year)+"."+str(d.month)+"."+str(d.day)+".zip","Backup")
    elif usrInput == "applybackup":
        usrInput = input("Apply image name: ")
        if os.path.exists("Backup") == False:
            os.mkdir("Backup")
            pass
        else:
            if os.path.exists("world"):
                shutil.rmtree("world")
            if os.path.exists("world_the_end"):
                shutil.rmtree("world_the_end")
            if os.path.exists("world_nether"):
                shutil.rmtree("world_nether")
            os.chdir("Backup")
            if os.path.exists("BackupImage") == False:
                os.mkdir("BackupImage")
            shutil.move(usrInput,"BackupImage")
            os.chdir("BackupImage")
            with zipfile.ZipFile(usrInput) as f:
                f.extractall()
            shutil.move(usrInput,"..")
            with zipfile.ZipFile("world.zip") as f:
                f.extractall()
            shutil.move("world","..")
            os.remove("world.zip")
            if os.path.exists("world_nether"):
                with zipfile.ZipFile("world_nether.zip") as f:
                    f.extractall()
                shutil.move("world_nether","..")
                os.remove("world_nether.zip")
            if os.path.exists("world_the_end"):
                with zipfile.ZipFile("world_the_end.zip") as f:
                    f.extractall()
                shutil.move("world_the_end","..")
                os.remove("world_the_end.zip")
            os.chdir("..")
            shutil.move("world","..")
            if os.path.exists("world_nether"):
                shutil.move("world_nether","..")
            if os.path.exists("world_the_end"):
                shutil.move("world_the_end","..")
            os.chdir("..")
    elif usrInput == "removebackup":
        usrInputYear = input("Which year: ")
        usrInputMonth = input("Which month: ")
        usrInputDay = input("Which day: ")
        if os.path.exists("Backup") == False:
            os.mkdir("Backup")
            pass
        else:
            os.chdir("Backup")
            if os.path.exists("backup-"+str(usrInputYear)+"."+str(usrInputMonth)+"."+str(usrInputDay)+".zip"):
                os.remove("backup-"+str(usrInputYear)+"."+str(usrInputMonth)+"."+str(usrInputDay)+".zip")
            os.chdir("..")
    elif usrInput == "addpack":
        usrInput = input("Which datapack: ")
        if os.path.exists(usrInput) == False:
            pass
        else:
            os.mkdir(usrInput[:-4])
            shutil.move(usrInput,usrInput[:-4])
            os.chdir(usrInput[:-4])
            with zipfile.ZipFile(usrInput) as f:
                f.extractall()
            os.rename("pack.mcmeta","pack.mcmeta"[:-7]+".json")
            with open("pack.json","r") as f:
                json_data = json.load(f)
                pack_data = json_data["pack"]
                pack_format = pack_data["pack_format"]
                description = pack_data["description"]
                shutil.move(usrInput,"..")
                os.chdir("..")
                f.close()
            shutil.rmtree(usrInput[:-4])
            shutil.move(usrInput,"world")
            os.chdir("world")
            shutil.move(usrInput,"datapacks")
            os.chdir("..")
            print(os.getcwd())
            os.chdir("datapacks_list")
            with open(usrInput[:-4], "w") as f:
                f.write("pack_format: "+str(pack_format)+" | description: "+description)
                f.close()
            os.chdir("..")
    elif usrInput == "removepack":
        usrInput = input("Which datapack: ")
        if os.path.exists("world"):
            os.chdir("world")
            if os.path.exists("datapacks"):
                os.chdir("datapacks")
                if os.path.exists(usrInput):
                    os.remove(usrInput)
                    os.chdir("..")
                    os.chdir("..")
                    os.chdir("datapacks_list")
                    os.remove(usrInput[:-4])
                    os.chdir("..")
    elif usrInput == "allpack":
        f = os.listdir("datapacks_list")
        os.chdir("datapacks_list")
        num = len(f)
        if num == 1:
            print("There is only one datapack enabled")
        elif num == 0:
            pass
        else:
            print("There are "+str(num)+" datapacks enabled")
        print("\n")
        for file in f:
            with open(file,"r") as d:
                inf = d.read()
                d.close()
            print(file+" | "+inf)
        os.chdir("..")
    elif usrInput == "exit":
        exit()
    elif usrInput == "help":
        print("""
start           =>Run Server.
seed            =>Find Seed.
removeworld     =>Remove World.
createbackup    =>Create a Backup Image.
applybackup     =>Restore a Backup Image.
removebackup    =>Remove a Backup Image.
addpack         =>Add a Datapack.
removepack      =>Remove a Datapack.
allpack         =>Print all of Datapack on Screen.
exit            =>Exit.
help            =>Get Help.
        """)
    else:
        print("There is no such keyword.")