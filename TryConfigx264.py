import os
import random
import time
import io
import logging

# initializations

number_of_configs = 17; # number of options for one build configuration
number_of_iters = 0; # number of configurations to be executed
all_configs = [] # storing all used configurations
all_times = [] # storing all execution times
command = '' # stores own configuration command
start_time = time.time() # for measuring the execution time of one configuration
end_time = time.time()



# define configurations
aq_mode = [0,1,2] #Default=1 //0=off, 2=experimental
b_adapt = [1,2] #Default=1  (options: 0,1,2) // 0 not recommended
b_bias = [-80,-50,-30,0,30,50,80] #Default=0 (range -100 to 100)
b_pyramid = ["none", "normal"] #Default=normal //requires bframes 2 or higher //strict only for blu-ray
bitrate = [500,1000,1500,2000,2500,3000] #Default=Not set
bframes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] #Default=3 //recommended max of 16 combined with --b-adapt 1 or 4 to 5 with --b-adapt 2
crf = [18,19,20,21,22,23,24,25] #//Default=23.0 //recommended values from 18-25, 1-pass encoding
deblock = ["-4:-4","-3:-3","-2:-2","-1:-1","0:0","1:1","2:2","3:3","4:4"] #Default= 0:0 (range -6 to 6)
keyint =["infinite", 50, 100, 150, 200, 250, 350]#Default=250 // positive integers or infinite(=deactivate IDR-Frames)
ratetol = ["inf", 0.01, 1, 10, 50, 100] #Default=1.0 (0.01-100, inf) //For 1-pass
rc_lookahead = [0,20,40,60,80,100,120,140,160,180,200,220,250] #Default=40 (range 0-250), the higher the values, the higher the computation time
ref = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] #Default=3 (range 0-16) #quality does not increase after 4
qp = [0,10,20,30,40,50,69]#Default=Not Set, range 0-69
weightp = [0,1,2] #Default=2
me = ["dia", "hex", "umh", "esa", "tesa"] #Default=hex //from dia to tesa more accurate, but slower, hex only for slow pcs
subme = [5,6,7,8,9,10,11] #Default=7 (range 0-11) //from 0 to 11 more accurate, but slower //don't use lower than 5
trellis = [1,2] #Default=1 //Don't use 0(=deactivation)



# run independently
preset = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
profile = ["baseline","main","high"]   # Default: high
tune = ["film", "animation", "grain", "stillimage", "psnr", "ssim", "fastdecode", "zerolatency"] # Default: not set

# not yet integrated, since pass 2 or 3 need more than one run
pass_ = [1,2,3] # Default= Not Set //enables: --ref 1, --no-8x8dct, --partitions i4x4, --me ida, --subme MIN, --trellis 0
stats = ["x264_2pass.log"] #Default='x264_2pass.log'


#container for storing the configuration options
options1 = [aq_mode, b_adapt, b_bias, b_pyramid, bitrate, bframes, crf, deblock, keyint, 
					ratetol, rc_lookahead, ref, qp, weightp, me, subme, trellis]

#container for storing the names of the configuration options for building the compile command later on 
options2 = ["aq-mode", "b-adapt", "b-bias", "b-pyramid", "bitrate", "bframes", 
			"crf", "deblock", "keyint", "ratetol", "rc-lookahead", "ref", "qp", "weightp", "me", "subme", "trellis"]

# preset, profile and tune are configurations with predefined options (like bitrate 1000, crf 29, ...)
# so we choose randomly either 0 (= build an random configuration out of the 17 options) or a predefined configuration
choose_opts1 = [0, preset, profile, tune] 
choose_opts2 = ["0", "preset", "profile", "tune"]


# choose random configuration
def build_command():

	if not(os.path.isfile("Cat.y4m")):
				print("Source file does not exist")

	if input_config == 'o':

		compile_command = command
		print(compile_command)

	elif input_config == 'r':

		#choose randomly either 0 (= build an random configuration out of the 17 options) or a predefined configuration
		choice = random.choice(range(0,2)) 

		if(choice == 0):
	
			config_opt = [] 
			compile_command = "x264"
	
			for i in range(0,number_of_configs):
	
				config_opt.append(random.choice(options1[i])) # choose random values out of the 17 options
				compile_command += " --"+options2[i]+" "+str(config_opt[i])
			print(compile_command)
	
		else:
			choice2 = random.choice(range(1,4)) 
			# take the predefined configuration and choose an random predefined option for it
			compile_command = "x264 --"+str(choose_opts2[choice2])+" "+str(random.choice(choose_opts1[choice2]))
			print(compile_command)
	return compile_command

# logging all execution times and configurations
def log_configs():
	logging.basicConfig(filename='execution_times.log',level=logging.DEBUG)
	logging.debug(all_times)
	logging.debug(all_configs)



# reading in a configuration file and executing it
def read_configs(txtfile):

	file = open(txtfile, 'r')

	for line in file:
		line  = line.replace("\n", "")
		all_configs.append(line)
		print(line)
		line += ' -o Cat.mkv Cat.y4m'
		start_time = time.time()
		os.system(line)
		end_time = time.time() - start_time
		all_times.append(end_time)


# Providing options to the user

input_config = input("Own live input configuration (o), random configuration (r), own configuration file (f): ")

if input_config == 'r':

	number_of_iters = int(input("Enter the number of random configurations you want to run: "))

elif input_config == 'o':
	number_of_iters = 1;
	command = input("Enter your configuration command (e.g x264 --preset fast): ")

elif input_config == 'f':
	command = input("Enter the name of your configuration file: ")


# executing configurations and measuring execution times
if input_config == 'o' or input_config == 'r':

	# run configurations
	for i in range(0,number_of_iters):
		compile_command = build_command()
		all_configs.append(compile_command)
		compile_command += " -o Cat.mkv Cat.y4m"
		start_time = time.time()
		os.system(compile_command)
		end_time = time.time() - start_time
		all_times.append(end_time)
elif input_config == 'f':
	read_configs(command)


# print and save end results
log_configs()
print('\n\nConfigurations:\n\n'+'\n'.join(all_configs))
print('\nExecution times:\n')
for j in all_times:
	print(j)
