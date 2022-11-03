import time
import L1_ina as ina 
import L1_log as log 

def UpdateFile():
    value = ina.readVolts()
    log.tmpFile(value, "a.txt")
    log.tmpFile(value, "b.txt")
    return value;
    
def UpdateVoltsFile():
    value = ina.readVolts()
    log.tmpFile(value, "v.txt")
    return value;
    
def UpdateFileSpecified(content2write, fileName="default.txt"):
    log.tmpFile(content2write, fileName)
    return;
    
if __name__ == "__main__":
    while(True):
        UpdateVoltsFile()
        print("tmp Updated")
        time.sleep(.2)
