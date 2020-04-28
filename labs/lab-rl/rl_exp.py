import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
import numpy as np
import pandas as pd
from datetime import datetime


class RL_Experiment():

    def __init__(self, subj_num):
        self.subject_num = subj_num
        self.output_file = 'rlexp-'+str(subj_num)+'.csv'

        # create four buttons with these names
        self.labels = ['Bandit 0', 'Bandit 1', 'Bandit 2', 'Bandit 3']
        self.buttons = [
            widgets.Button(description=desc, layout=widgets.Layout(
                width='auto', grid_area=f'button{idx}'), value=idx)  # create button
            for idx, desc in enumerate(self.labels)
        ]  # puts buttons into a list

        # create instructions file
        self.instructions_file = open("images/rl-instructions.png", "rb")
        self.image = self.instructions_file.read()
        self.img = widgets.Image(
            value=self.image,
            format='png',
            width=900,
            height=1000,
            layout=widgets.Layout(width='auto', grid_area='instruct')
        )

        # create output widget for displaying feedback/reward
        self.out = widgets.Output(layout=widgets.Layout(
            width='auto', grid_area='output'))  # output widgets wrapped in VBoxes

        self.trial_num = 0
        self.total_reward = 0
        self.data = []
        np.random.seed(24)
        self.create_trials()
        self.done = False
        self.dt = datetime.now()

    def create_trials(self, std=2.0, nblocks=6, advantage=6, ntrials_block=35):
        blocks = []
        best_resp = []
        for i in range(nblocks):
            best = np.random.randint(0, 4)
            best_resp.append([best]*ntrials_block)

            best_multiple = advantage
            best_array = np.zeros(4)
            best_array[best] = 1.0
            block = np.random.normal(
                0, std, (ntrials_block, 4))+best_multiple*np.array([best_array]*ntrials_block)
            blocks.append(block)

        exp_rewards = np.array(blocks).reshape(ntrials_block*nblocks, 4)
        self.best_resp = np.array(best_resp).reshape(ntrials_block*nblocks,)
        self.trials = exp_rewards
        self.responses = []

    # create function called when button clicked.
    # the argument to this fuction will be the clicked button
    # widget instance
    def on_button_clicked(self, button):
        # "linking function with output'
        if not self.done:
            with self.out:
                # what happens when we press the button
                # can alter this to be a different vluae

                chose = int(button.description[-1])

                # clears any info visible now
                clear_output()

                # reminds us what we clicked
                points = self.trials[self.trial_num][chose]
                self.total_reward += points
                self.responses.append(chose)
                # record reaction time here?

                print("You choose Bandit ", chose)
                print(f"You earned {points:.2f} points!")
                print(f"Trial {self.trial_num} out of {self.trials.shape[0]}")
                print(f"--------")
                print(f"Your total so far is {self.total_reward:.2f} points!")

                if chose == self.best_resp[self.trial_num]:
                    maximizing = 1
                else:
                    maximizing = 0
                self.data.append([self.subject_num,
                                  self.trial_num,
                                  self.trial_num % 35,  # block number
                                  chose,
                                  points,
                                  self.best_resp[self.trial_num],
                                  maximizing,
                                  self.trials[self.trial_num][0],
                                  self.trials[self.trial_num][1],
                                  self.trials[self.trial_num][2],
                                  self.trials[self.trial_num][3],
                                  self.total_reward,
                                  (datetime.now()-self.dt).total_seconds() * 1000
                                  ])
                self.dt = datetime.now()  # reset clock

                self.trial_num += 1
                if self.trial_num >= 35*6:
                    self.done = True
        else:
            clear_output()
            self.save_data(self.output_file)
            print("The experiment is finished!")
            print(f"You earned {self.total_reward:.2f}")
            print("Data saved to .csv")
            print("Also available as exp.df")
            print("-------------")
            print("Thanks so much for your time!")

    def save_data(self, fn):
        # create dataframe
        self.df = pd.DataFrame(self.data, columns=['subject', 'trial', 'block', 'choice',
                                                   'reward','best_resp', 'max', 'reward0', 'reward1', 
                                                   'reward2', 'reward3', 'total_reward', 'rt'])
        # write to disk
        self.df.to_csv(self.output_file)
        pass

    def start_experiment(self):
        # linking button and function together using a button's method
        [button.on_click(self.on_button_clicked) for button in self.buttons]

        return widgets.GridBox(children=self.buttons+[self.out]+[self.img],
                               layout=widgets.Layout(
            width='70%',
            grid_template_rows='auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
                           "instruct instruct instruct instruct"
                           "button0 button1 button2 button3"
                           "output output output output"
                           '''
        ))
