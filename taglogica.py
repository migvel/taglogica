from bge import logic
from bge import events
import subprocess as sub
import aud
import os


mouse = logic.mouse
cwd = os.getcwd()
logic.globalDict["objectlist"] = {'bc999dd32e302d31362d':'/bracelet/basic/arm60-25','04e5759121258031362d':'/vaas77','fc999dd32e302d31362d':'/bracelet/basic/arm70-20',
'5cd59ed32e302d31362d':'/bracelet/basic/arm65-35','8c319ed3000000000000':'obj1.blend','0a46d614000000000000':'obj2.blend'}

device = aud.device()
beep = aud.Factory('/home/sio2/tecroom/blender/scripts/rfid_catalog/sounds/beep.wav')

logic.globalDict["pollcnt"] = 0
logic.globalDict["uidbuf"] = ""


#print(cwd)
def pollingctrl():
    if mouse.events[events.LEFTMOUSE] == 1:
    #this triggers once, for one tick even if the mouse is held
        ob = logic.getCurrentController().owner

        if(ob['pollingstatus'] == False):
            ob['pollingstatus'] = True
        else:
            ob['pollingstatus'] = False

        print("Polling status: "+str(ob['pollingstatus']))


def debug():
    print("debug!!!!")
    handle = device.play(beep)

def polling():
    ob = logic.getCurrentController().owner
    if(ob["pollingstatus"] == True):
        p = sub.Popen(cwd+"/rfid/readuid",stdout=sub.PIPE,stderr=sub.PIPE)
        p.wait()

        uidtemp = str(p.stdout.read(), "utf-8")
        uidtemp = uidtemp.replace(' ','')
        uidtemp = uidtemp[:len(uidtemp)-1]
        if(len(uidtemp)>0):
            if(uidtemp != logic.globalDict["uidbuf"]):
                
                print("Tag readed: "+str(uidtemp))
            
                #play sound
                if(ob["tagdetected"] == True):
                    ob["tagdetected"] = False
                else:
                    ob["tagdetected"] = True
                print("New tag detected")
                
                #load object
                print(logic.globalDict["objectlist"][uidtemp])

                #blendfile = uidtemp
                logic.LibFree(cwd+"/models/"+logic.globalDict["objectlist"][uidtemp])
                
                scene = logic.getCurrentScene()
                print(cwd+logic.globalDict["objectlist"][uidtemp])
                logic.LibLoad(cwd+"/models/"+logic.globalDict["objectlist"][uidtemp], 'Mesh')
                player = scene.objects[ob.name]
                player.replaceMesh(logic.globalDict["objectlist"][uidtemp].replace(".blend",""))
                ob.localScale = [0.1,0.1,0.1]


            logic.globalDict["uidbuf"] = uidtemp
