import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim, Rect, TextBox, DotStim
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy import event, data
import random

exp_info = {'participant_nr': '', 'age': '','number of trials':[10,50,100,150]}
dlg = DlgFromDict(exp_info)
trialn= exp_info['number of trials']

win = Window(size=(1200, 800), fullscr=False, monitor='samsung')

mouse = Mouse(visible=False)

clock = Clock()

kb = Keyboard()
kb.clearEvents()

welcome_txt_stim = TextStim(win, text="Welcome to this experiment!", color=(1, 0, -1), font='Calibri')
welcome_txt_stim.draw()
win.flip()
wait(2)

instruct_txt = """ 
Please type the first four letters of your last name followed by the last two digits of your birth year. 
When you are finished, hit the return key.
"""
instruct=TextStim(win,instruct_txt,pos=(0,0.75))
instruct.draw()
win.flip()

kb = Keyboard()
p_name=''
while True:
    keys = kb.getKeys()
    for key in keys:
        p_name=p_name+key.name
        display=TextStim(win,p_name)
        display.draw()
        instruct.draw()
        win.flip()
    if 'return' in keys:
        p_name=p_name
        break 

task_instruct_txt = """ 
In this experiment, you will see a collection of moving dots.

On each trial the predominant movement of the dots will either be towards the left or the right.

You should indicate with the arrow keys which direction the motion is in. 

Sometimes it may be hard to tell; go with your best guess!
    
 """

task_instruct_txt = TextStim(win, task_instruct_txt, alignText='left', height=0.085)
task_instruct_txt.draw()
win.flip()

kb = Keyboard()
while True:
    keys = kb.getKeys()
    if 'return' in keys:
        break  

N_TRIALS = trialn
N_DOTS = 150
DOT_SIZE = 5  
DOT_SPEED = 0.5  
DOT_FIELD_SIZE = 2  
COHERENCE_LEVELS = [0.05, 0.1, 0.2, 0.4, 0.8] 
DIRECTIONS = [0, 180] 
FIXATION_MIN = 0.5 
FIXATION_MAX = 1.5  


fix = TextStim(win, "+", height=2)
dots = DotStim(
    win,
    fieldShape='circle', 
    nDots=N_DOTS,
    fieldSize=DOT_FIELD_SIZE,
    dotSize=DOT_SIZE,
    speed=DOT_SPEED,
    dotLife=12,  
    noiseDots='direction',
    signalDots='same'
)


trial_list = []
for coherence in COHERENCE_LEVELS:
    for direction in DIRECTIONS:
        
        for rep in range(0,trialn//10):  
            trial_list.append({
                'coherence': coherence,
                'direction': direction,
                'correct_response': 'left' if direction == 180 else 'right'
            })

trials = data.TrialHandler(trial_list, nReps=1, method='random')

for trial in trials:
    
    fixation_time = random.uniform(FIXATION_MIN, FIXATION_MAX)
    
    
    fix.draw()
    win.flip()
    wait(fixation_time)
    
    
    dots.coherence = trial['coherence']
    dots.dir = trial['direction']
    
    
    kb.clock.reset()
    kb.clearEvents()
    
    
    response = None
    rt = None
    
    while response is None:
        dots.draw()
        win.flip()
        
       
        keys = kb.getKeys(['left', 'right', 'escape'], waitRelease=False)
        if keys:
            response = keys[0].name
            rt = keys[0].rt
            
            
            if response == 'escape':
                win.close()
                quit()
    
    
    trials.addData('response', response)
    trials.addData('rt', rt)
    trials.addData('correct', response == trial['correct_response'])
    trials.addData('fixation_duration', fixation_time)
    

    win.flip()
    wait(0.5)

filename = p_name + '_random_dot_motion'
trials.saveAsExcel(filename + '.xlsx')


end_text = visual.TextStim(win, "Task complete! Thank you.", height=1)
end_text.draw()
win.flip()
wait(2)

win.close()
quit()
