import simpy

env = simpy.Environment()

interruption = env.event()

def my_proc1(env):
    while True:
        print("On proc1")
        print(env.active_process)  # will print "p1"
        yield env.timeout(10) | interruption # Magic point!
        print("I'm waking up at time:", env.now)

def my_proc2(env):
    while True:
        #wait at least 2 unit times
        yield env.timeout(8)
        print("On proc2")
        print(env.active_process)  # will print "p2"
        interruption.succeed() #trigger the interruption event


p1 = env.process(my_proc1(env))
p2 = env.process(my_proc2(env))

# Lets run this simulation (run line by line)

#Two Events at time 0: proc1, proc2
env.step() #runs the proc1
print(env.now)
env.step() #runs the proc2
print(env.now)

# One event at time 2:
env.step() #next event is proc2
print(env.now)

#but the previous event, trigger the "interruption event" in time 2 as well
env.step()
print(env.now)
env.step() #same time: 2
print(env.now)




