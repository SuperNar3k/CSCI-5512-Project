### Implementing the solution to the code cracking problem using genetic algorithms.
### 
### Type on the home screen to change the target phrase
### Use the slider to change genetic algorithm parameters
### Click 'CRACK' to run the algorithm with the specified variables
### Displays best individual of the current generation
### Displays a progress bar that indicates the amount of completion of the algorithm
### Displays the first few individuals of the current generation

### Import modules
import os.path
from tkinter import *
from tkinter import ttk

import search_utils


### UI parameters
LARGE_FONT = ('Verdana', 12)
EXTRA_LARGE_FONT = ('Consolas', 36, 'bold')
canvas_width = 800
canvas_height = 600
black = '#000000'
white = '#ffffff'
p_blue = '#042533'
lp_blue = '#0c394c'

### Instance fields for the genetic algorithm variables
code = 'Social Security Number'  # the code to attempt to crack
max_population = 100  # number of samples in each population
mutation_rate = 0.1  # probability of mutation
f_thres = len(code)  # fitness threshold
ngen = 1200  # max number of generations to run the genetic algorithm

generation = 0  # counter to keep track of generation number

### Lists for characters for the possibility of usage in the gene pool
u_case = [chr(x) for x in range(65, 91)]  # list containing all uppercase characters
l_case = [chr(x) for x in range(97, 123)]  # list containing all lowercase characters
punctuations1 = [chr(x) for x in range(33, 48)]  # lists containing punctuation symbols
punctuations2 = [chr(x) for x in range(58, 65)]
punctuations3 = [chr(x) for x in range(91, 97)]
numerals = [chr(x) for x in range(48, 58)]  # list containing numbers

### Set the gene pool with the required lists
gene_pool = []
gene_pool.extend(u_case)
gene_pool.extend(l_case)
gene_pool.append(' ') # append the space char


### Update functions for global variables from the slider values
def update_max_population(slider_value):
    global max_population
    max_population = slider_value

def update_mutation_rate(slider_value):
    global mutation_rate
    mutation_rate = slider_value

def update_f_thres(slider_value):
    global f_thres
    f_thres = slider_value

def update_ngen(slider_value):
    global ngen
    ngen = slider_value


# This is the fitness function!
def fitness_fn(_list):
    fitness = 0
    # create string from list of characters
    phrase = ''.join(_list)
    # add 1 to fitness value for every matching character
    for i in range(len(phrase)):
        if code[i] == phrase[i]:
            fitness += 1
    return fitness

### UI setup and creation
# Function to bring a new frame on top
def raise_frame(frame, init=False, update_target=False, target_entry=None, f_thres_slider=None):
    frame.tkraise()
    global code
    if update_target and target_entry is not None:
        code = target_entry.get()
        f_thres_slider.config(to=len(code))
    if init:
        population = search_utils.init_population(max_population, gene_pool, len(code))
        genetic_algorithm_stepwise(population)

# Setup the frames
root = Tk()
f1 = Frame(root)
f2 = Frame(root)
for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')

# Home Screen (f1) widgets
target_entry = Entry(f1, font=('Consolas 46 bold'), exportselection=0, foreground=p_blue, justify=CENTER)
target_entry.insert(0, code)
target_entry.pack(expand=YES, side=TOP, fill=X, padx=50)
target_entry.focus_force()

max_population_slider = Scale(f1, from_=3, to=1000, orient=HORIZONTAL, label='Max population',
                              command=lambda value: update_max_population(int(value)))
max_population_slider.set(max_population)
max_population_slider.pack(expand=YES, side=TOP, fill=X, padx=40)

mutation_rate_slider = Scale(f1, from_=0, to=1, orient=HORIZONTAL, label='Mutation rate', resolution=0.0001,
                             command=lambda value: update_mutation_rate(float(value)))
mutation_rate_slider.set(mutation_rate)
mutation_rate_slider.pack(expand=YES, side=TOP, fill=X, padx=40)

f_thres_slider = Scale(f1, from_=0, to=len(code), orient=HORIZONTAL, label='Fitness threshold',
                       command=lambda value: update_f_thres(int(value)))
f_thres_slider.set(f_thres)
f_thres_slider.pack(expand=YES, side=TOP, fill=X, padx=40)

ngen_slider = Scale(f1, from_=1, to=5000, orient=HORIZONTAL, label='Max number of generations',
                    command=lambda value: update_ngen(int(value)))
ngen_slider.set(ngen)
ngen_slider.pack(expand=YES, side=TOP, fill=X, padx=40)

button = ttk.Button(f1, text='CRACK',
                    command=lambda: raise_frame(f2, init=True, update_target=True, target_entry=target_entry,
                                                f_thres_slider=f_thres_slider)).pack(side=BOTTOM, pady=50)

# f2 widgets
canvas = Canvas(f2, width=canvas_width, height=canvas_height)
canvas.pack(expand=YES, fill=BOTH, padx=20, pady=15)
button = ttk.Button(f2, text='EXIT', command=lambda: raise_frame(f1)).pack(side=BOTTOM, pady=15)


### Function to execute the genetic algorithm and update the text on the canvas
def genetic_algorithm_stepwise(population):
    root.title('Genetic Algorithm')
    for generation in range(ngen):
        # generating new population after selecting, recombining and mutating the existing population
        population = [
            search_utils.mutate(search_utils.recombine(*search_utils.select(2, population, fitness_fn)), gene_pool, mutation_rate) for i
            in range(len(population))]
        # genome with the highest fitness in the current generation
        current_best = ''.join(max(population, key=fitness_fn))
        # collecting first few examples from the current population
        members = [''.join(x) for x in population][:48]

        # clear the canvas
        canvas.delete('all')
        # displays current best on top of the screen
        canvas.create_text(canvas_width / 2, 40, fill=p_blue, font='Consolas 46 bold', text=current_best)

        # displaying a part of the population on the screen
        for i in range(len(members) // 3):
            canvas.create_text((canvas_width * .175), (canvas_height * .25 + (25 * i)), fill=lp_blue,
                               font='Consolas 16', text=members[3 * i])
            canvas.create_text((canvas_width * .500), (canvas_height * .25 + (25 * i)), fill=lp_blue,
                               font='Consolas 16', text=members[3 * i + 1])
            canvas.create_text((canvas_width * .825), (canvas_height * .25 + (25 * i)), fill=lp_blue,
                               font='Consolas 16', text=members[3 * i + 2])

        # displays current generation number
        canvas.create_text((canvas_width * .5), (canvas_height * 0.95), fill=p_blue, font='Consolas 18 bold',
                           text=f'Generation {generation}')

        # displays blue bar that indicates current maximum fitness compared to maximum possible fitness
        scaling_factor = fitness_fn(current_best) / len(code)
        canvas.create_rectangle(canvas_width * 0.1, 90, canvas_width * 0.9, 100, outline=p_blue)
        canvas.create_rectangle(canvas_width * 0.1, 90, canvas_width * 0.1 + scaling_factor * canvas_width * 0.8, 100,
                                fill=lp_blue)
        canvas.update()

        # Check for code completion
        fittest_individual = search_utils.fitness_threshold(fitness_fn, f_thres, population)
        if fittest_individual:
            break

### Run it
raise_frame(f1)
root.mainloop()
