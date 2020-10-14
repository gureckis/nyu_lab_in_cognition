import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
import numpy as np
import numpy.random as npr
import pandas as pd
from datetime import datetime
from ipycanvas import Canvas, hold_canvas
import seaborn as sns
import math


def draw_stimulus(include_source, n_background_dots, n_source_dots, source_sd, source_border, width, height):

    canvas = Canvas(width=425, height=425, layout=widgets.Layout(
               justify_self='center', grid_area='canvas'))
    border = 4
    stroke = 2
    dot_radius = 2

    with hold_canvas(canvas):
        # draw box
        canvas.clear()
        canvas.stroke_style='black'
        canvas.stroke_rect(stroke,stroke,width,height)

        if include_source:
            bgdots = n_background_dots
            sourcedots = n_source_dots
        else:
            bgdots = n_background_dots+n_source_dots
            sourcedots = 0


        for _ in range(bgdots):
            canvas.fill_style = npr.choice(sns.color_palette("Paired").as_hex())
            x = npr.uniform(border,width-border)
            y = npr.uniform(border,height-border)
            canvas.fill_arc(x, y, dot_radius, 0, 2 * math.pi)

        if sourcedots > 0:
            x_center = npr.uniform(source_border,width-source_border)
            y_center = npr.uniform(source_border,width-source_border)
            x = np.clip(npr.normal(x_center, source_sd, sourcedots), source_border, width-source_border)
            y = np.clip(npr.normal(y_center, source_sd, sourcedots), source_border, width-source_border)

            for i in range(n_source_dots):
                canvas.fill_style = npr.choice(sns.color_palette("Paired").as_hex())    
                canvas.fill_arc(x[i], y[i], dot_radius, 0, 2 * math.pi)
    return canvas


class Detection_Experiment():

    def __init__(self, subj_num):
        self.subject_num = subj_num
        self.output_file = 'sdt-'+str(subj_num)+'.csv'

        # create two buttons with these names, randomize the position
        if npr.random()<0.5:
            self.labels = [['Present', widgets.ButtonStyle(button_color='darkseagreen')], 
                           ['Absent', widgets.ButtonStyle(button_color='salmon')]]
            self.position = 'left'
        else:
            self.labels = [['Absent', widgets.ButtonStyle(button_color='salmon')],
                           ['Present', widgets.ButtonStyle(button_color='darkseagreen')]]
            self.position = 'right'

        self.buttons = [
            widgets.Button(description=desc[0], layout=widgets.Layout(
                width='auto', grid_area=f'button{idx}'), value=idx, style=desc[1])  # create button
            for idx, desc in enumerate(self.labels)
        ]  # puts buttons into a list

        self.canvas = Canvas(width=425, height=425, layout=widgets.Layout(
               justify_self='center', grid_area='canvas'))
        
        # create output widget for displaying feedback/reward
        self.out = widgets.Output(layout=widgets.Layout(
            width='auto', object_position='center', grid_area='output'))  # output widgets wrapped in VBoxes

        np.random.seed(24)
        self.create_trials(25, [10, 15, 25, 60])
        self.done = False
    
    def create_trials(self, ntrials, vals):
        signal_present = np.array([0]*(ntrials*len(vals))+[1]*(ntrials*len(vals)))
        l = [[val]*ntrials for val in vals]
        l = [item for sublist in l for item in sublist]
        signal_type = np.array([0]*(ntrials*len(vals))+l)


        self.trials=pd.DataFrame({'signal_present': signal_present, 'signal_type': signal_type})
        self.trials=self.trials.sample(frac=1).reset_index(drop=True) # shuffle
        self.trials['trial_num']=np.arange(self.trials.shape[0])
        self.trials['button_position']=self.position
        self.trials['subject_number']=self.subject_num
        self.trial_iterator=self.trials.iterrows()
        self.responses = []
        self.rt = []
        self.correct_resp = []

    # create function called when button clicked.
    # the argument to this fuction will be the clicked button
    # widget instance
    def on_button_clicked(self, button):
        # "linking function with output'
        if not self.done:
            with self.out:
                # what happens when we press the button
                choice = button.description
                if choice=='Present':
                    choice_code = 1
                elif choice=='Absent':
                    choice_code = 0
                
                # reminds us what we clicked
                self.responses.append(choice_code)
                
                # record reaction time here?
                if choice_code == self.current_trial['signal_present']:
                    correct = 1
                else:
                    correct = 0
                self.correct_resp.append(correct)
                
                self.rt.append((datetime.now()-self.dt).total_seconds() * 1000)
                
                self.next_trial()
        else:
            clear_output()
            self.save_data(self.output_file)
            print("The experiment is finished!")
            print("Data saved to .csv")
            print("Also available as exp.trials")
            print("-------------")
            print("Thanks so much for your time!")

    def save_data(self, fn):
        # create dataframe
        self.trials['responses'] = self.responses
        self.trials['rt'] = self.rt
        self.trials['correct_resp'] = self.correct_resp
        
        self.trials.to_csv(self.output_file)

    def draw_stimulus(self, include_source, n_background_dots, n_source_dots, source_sd, source_border, width, height):

        border = 4
        stroke = 2
        dot_radius = 2

        with hold_canvas(self.canvas):
            # draw box
            self.canvas.clear()
            self.canvas.stroke_style='black'
            self.canvas.stroke_rect(stroke,stroke,width,height)

            if include_source:
                bgdots = n_background_dots
                sourcedots = n_source_dots
            else:
                bgdots = n_background_dots+n_source_dots
                sourcedots = 0


            for _ in range(bgdots):
                self.canvas.fill_style = npr.choice(sns.color_palette("Paired").as_hex())
                x = npr.uniform(border,width-border)
                y = npr.uniform(border,height-border)
                self.canvas.fill_arc(x, y, dot_radius, 0, 2 * math.pi)

            if sourcedots > 0:
                x_center = npr.uniform(source_border,width-source_border)
                y_center = npr.uniform(source_border,width-source_border)
                x = np.clip(npr.normal(x_center, source_sd, sourcedots), source_border, width-source_border)
                y = np.clip(npr.normal(y_center, source_sd, sourcedots), source_border, width-source_border)

                for i in range(n_source_dots):
                    self.canvas.fill_style = npr.choice(sns.color_palette("Paired").as_hex())    
                    self.canvas.fill_arc(x[i], y[i], dot_radius, 0, 2 * math.pi)

    def next_trial(self):
        try:
            self.current_trial = next(self.trial_iterator)[1]  
            self.draw_stimulus(include_source=self.current_trial['signal_present'], 
                               n_background_dots=30*30, 
                               n_source_dots=self.current_trial['signal_type'], 
                               source_sd=10, 
                               source_border=20, 
                               width=400, 
                               height=400)
            self.dt = datetime.now()  # reset clock

        except StopIteration:
            self.done=True


    def start_experiment(self):
        # linking button and function together using a button's method
        [button.on_click(self.on_button_clicked) for button in self.buttons]
        
        self.next_trial()

        return widgets.GridBox(children=self.buttons+[self.canvas],
                               layout=widgets.Layout(
            width='50%',
            justify_items='center',
            grid_template_rows='auto auto',
            grid_template_columns='10% 40% 40% 10%',
            grid_template_areas='''
                           ". canvas canvas ."
                           ". button0 button1 ."
                           "output output output output"
                           '''
        ))
