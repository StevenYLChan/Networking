# CMPUT 313
# ASSIGNMENT 1
# STEVEN CHAN
import sys
import random
import math

# basic checker for number of arguments
if (len(sys.argv) < 10):
    raise ValueError("[ERROR] Invalid number of arguments.")
# there must be enough seeds for trials
if (int(sys.argv[9]) != len(sys.argv[10:])):
    raise ValueError("[ERROR] Number of trials does not match number of seeds.")
# pop off argv[0] which is input file
sys.argv.pop(0)
# output as required
for arg in sys.argv[:8]:
    print(arg)

# M (character): Indicates the error model used:  I for independent, B for Burst
argM = str(sys.argv[0])
#    A (integer): You can assume the feedback time is 50 bit time units.
argA = int(sys.argv[1])
#    K (integer):  The number of blocks. You should at least explore the range of values of K =0, 1, 2,10,40,100,400,1000.  Note that your K should be chosen such that F is a multiple of K.
argK = int(sys.argv[2])
#    F (integer)   The size of the frame in number of bits.   You can assume this is 4000 bits.
argF = int(sys.argv[3])
#    e (floating)  The probability that a bit is in error.  You will vary this for e = 0.0001, 0.0003, 0.0005, 0.0007,  0.001.
argE = float(sys.argv[4])
#    B burst length.  0 for the independent model.  For the burst model, set this to 50 and 500 bit times.
argB = int(sys.argv[5])
#    N non-burst length.  0 for the independent model.  For the burst model, set this to 5000 and 1000 bit times.
argN = int(sys.argv[6])
#    R (integer)   The length of the simulation in bit time units.   You must run this long enough to obtain stable results (for reasonable error rates).  This should be run on the order of 5,000,000 bit time units.
argR = int(sys.argv[7])
#    T  t1 t2 t3 ... tT (integer)   The number of trials, followed by seeds for the trials.  For this simulation, you can set T to 5.

# put seeds in list
argT = []
argT.append(sys.argv[8])
for arg in sys.argv[9:]:
    argT.append(arg)
# convert str arguments to int
argT = [int(arg) for arg in argT]
# output as required
print(argT)


# calculate 95% confidence interval
def ninefive_conf_interval(mean_value, stand_dev, t_dis):
    # sqrt(5) because sqrt(T) and T = trials = 5
    interm_val = (t_dis * (stand_dev / math.sqrt(5)))
    # c1 = x - t[] * s / sqrt(t)
    lower_bound = mean_value - interm_val
    # c2 = x + t[]* s / sqrt(t)
    upper_bound = mean_value + interm_val
    return lower_bound, upper_bound


# calculate standard deviation
def stand_dev(check, throughft, trials, corrected_Frames, total_frames, total_time, size_frame, ):
    # calculate standard deviation as s=sqrt(sum i=1 => T (xi-x)^2 / T-1)
    if check == 0:
        s = 0
        mean_value = total_frames / corrected_Frames
        # summation
        for i in range(trials):
            # (xi - x)^2
            s += ((throughft[i] - mean_value) ** 2)
            # T - 1
            s /= (trials - 1)
            s = math.sqrt(s)
            return s
    if check == 1:
        s1 = 0
        mean_value = (corrected_Frames * size_frame) / total_time
        for i in range(trials):
            # (xi - x)^2
            s1 += ((throughft[i] - mean_value) ** 2)
            # T - 1
            s1 /= (trials - 1)
            s1 = math.sqrt(s1)
            return s1


# create single frame bits
def make_Single_Frame(full_block):
    sFrame = list()
    # generate a random number x in (0,1) for each bit
    for bit in range(full_block):
        sFrame.append(randomUniform())
    return sFrame


# create burst frame bits
def make_Burst_Frame(full_block, burst_length, non_burst_length):
    bFrame = list()
    # generate a random number x in (0,1) for each bit in the burst periods
    # time alternates between burst periods and non-burst periods. Errors do not occur during non-burst periods (of length N)
    boolean_burst = 1
    count_length = 0
    for bit in range(full_block):
        boolean_burst, count_length, randU = switcher(boolean_burst, count_length, burst_length, non_burst_length)
        bFrame.append(randU)
    return bFrame


# return 1 so this bit will never be in error
def non_burst_call():
    # during non_burst, errors will never occur. This fulfills it by just sending a 1
    return 1


# calls funciton that returns a random number between (0,1)
def burst_call():
    return randomUniform()


# checks if it is a burst or non burst, calls the appropriate function. Need to alternate
def switcher(boolean_burst, count_length, burst_length, non_burst_length):
    option = {0: non_burst_call,
              1: burst_call,
              }
    # returns a number based on option
    randU = option[boolean_burst]()
    # if it passes burst_length then need to switch to non_burst, if it passes non_burst then need to switch to burst
    if boolean_burst == 1:
        count_length += 1
        if count_length >= burst_length:
            boolean_burst = 0
            count_length = 0
    elif boolean_burst == 0:
        count_length += 1
        if count_length >= non_burst_length:
            boolean_burst = 1
            count_length = 0
    return boolean_burst, count_length, randU


# checks whether it is independent model or burst model then creates a frame of that type
def model_check(error_model, full_block, burst_length, non_burst_length):
    if error_model == 'I':
        frame = make_Single_Frame(full_block)
    if error_model == 'B':
        frame = make_Burst_Frame(full_block, burst_length, non_burst_length)
    return frame


# return a random number between (0,1)
def randomUniform():
    return random.uniform(0, 1)


# parse the seed for random
def randomGenerator(seed):
    return random.seed(seed)


# calculate block size, full block size, checkbits
def block_size_calc(argF, argK):
    checkbits = 0
    # K=0 then no error correction is used and the frame of size F is just transmitted with its error detection capability
    if argK == 0:
        block_size = 0
        full_block = argF
    else:
        block_size = argF / argK
        # (m + r + 1) <= 2r
        while (block_size + checkbits + 1) > 2 ** checkbits:
            checkbits += 1
        checkbits *= argK
        full_block = argF + checkbits
    return block_size, full_block, checkbits


def sim(error_model, feedback_time, number_of_blocks, size_frame, prob_error, burst_length, non_burst_length,
        length_sim, trials):
    block_size, full_block, checkbits = block_size_calc(size_frame, number_of_blocks)
    average_Frame_Transmissions = list()
    throughput = list()
    tick = 0
    corrected_Frames = 0
    total_Frames = 0
    total_Time = 0
    # for each seed
    for test in trials[1:]:
        timer = 0
        finishedframe = 0
        # parse seed
        randomGenerator(test)
        # as long as the timer does not exceed the simulation time
        while timer <= length_sim:
            # make a frame
            frame = model_check(error_model, full_block, burst_length, non_burst_length)
            number_of_errors = 0
            # flag check
            in_error = False

            if block_size == 0:
                block_size = len(frame)

            for bit in frame:
                # process based on error model
                if error_model == 'I':
                    # if x<=e, then that bit is in error
                    if bit <= prob_error:
                        number_of_errors += 1
                        # no HSBC or more than 1 error
                        if checkbits == 0 or number_of_errors > 1:
                            in_error = True

                elif error_model == 'B':
                    error_prime = prob_error * (
                        (
                            non_burst_length + burst_length) / burst_length)
                    # if x<=e'=e*(N+B)/B,then that bit is in error
                    if bit <= error_prime:
                        number_of_errors += 1
                        # no HSBC or more than 1 error
                        if checkbits == 0 or number_of_errors > 1:
                            in_error = True
                tick = +1
                if tick >= block_size:
                    tick = 0
                    number_of_errors = 0
            # successful transmission
            if in_error == False:
                finishedframe += 1
            # increment timer
            timer = timer + full_block + feedback_time

        if finishedframe == 0:
            average_Frame_Transmissions.append(0)
            throughput.append(0)
        else:
            # average number of frame transmissions = the total number of frame transmissions including retransmission / the number of frames correctly received
            aft = (timer / (full_block + feedback_time)) / finishedframe
            average_Frame_Transmissions.append(aft)
            # throughput = F*the total number of correctly received frames / the total time required to correctly receive these frames
            tp = (size_frame * finishedframe) / timer
            throughput.append(tp)

        corrected_Frames += finishedframe
        total_Frames += timer / (full_block + feedback_time)
        total_Time += timer

    # call stand_dev with different inputs so need a flag indicator
    check = 0
    s = stand_dev(check, average_Frame_Transmissions, trials[0], corrected_Frames, total_Frames, 0, 0)
    # use stand dev to calculate confidence interval bounds
    lower_bound, upper_bound = ninefive_conf_interval(total_Frames / corrected_Frames, s, 2.776)

    # required outputs:  the average number of frame transmissions followed by the confidence interval for this metric
    output_avg = str(total_Frames / corrected_Frames)
    output_lower_bound = str(lower_bound)
    output_upper_bound = str(upper_bound)
    print(output_avg + " " + output_lower_bound + " " + output_upper_bound)

    # call stand_dev with different inputs so need a flag indicator
    check = 1
    s = stand_dev(check, throughput, trials[0], corrected_Frames, 0, total_Time, size_frame)
    # use stand dev to calculate confidence interval bounds
    lower_bound, upper_bound = ninefive_conf_interval((corrected_Frames * size_frame) / total_Time, s, 2.776)

    # required outputs: the throughput and confidence interval for throughput
    output_throughput = str((size_frame * corrected_Frames) / total_Time)
    output_lower_bound2 = str(lower_bound)
    output_upper_bound2 = str(upper_bound)
    print(output_throughput + " " + output_lower_bound2 + " " + output_upper_bound2)


sim(argM, argA, argK, argF, argE, argB, argN, argR, argT)
