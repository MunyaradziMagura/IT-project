import simpy
import random
import secrets

#  generate the pipe 
def pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp):
    # which sensor is being simulated
    sensor_id = 0
    highest_temp = 0
    # because there are only three sensors
    while True and sensor_id < 3:
        
        # add the last temp to the new 
        if highest_temp > 0:
            start_temperature += highest_temp - start_temperature
        #  create an instance of the water within the pipe
        water = sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp)

        # run the water instance for this sensor i.e. simulate water running though this section of the pipe 
        env.process(water)

        # time until the next sensor is reached by water 
        time = random.expovariate(1.0 / sensor_interval_time)

        # create a new sensor when time has passed
        yield env.timeout(time, highest_temp)

        # incriment the sensors by 1
        sensor_id += 1


# this function is the waters journey through the pipe 
def sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp):
        # time left for the sensor
    sensor_time_left = env.active_process   
    print(f"distance travled is {sensor_time_left}")
    if sensor_id == 3:
        print("HELLO WORLD")
        print(f"distance travled is {sensor_time_left}")
    # record the time the water starts changing tempreture at this sensor
    current_time = env.now
    print("Sensor:",sensor_id," started changing tempretures at",current_time," its current tempreture is ",start_temperature)
    # temperature 
    temperature = start_temperature
    # vibration 

    # request the sensor data
    with sensor.request() as req:
        # stop if no sensor is found 
        yield req
        con_time = random.expovariate(1.0 / sensor_interval_time)
        
        while True:
            
            # random number generator
            interarrival = random.expovariate(sensor_id + 1)
            # simulate vibration spikes 
            vibration = secrets.randbelow(start_vibration)
            
            # ensure the vibration is always above 0
            while vibration == 0:
                vibration = secrets.randbelow(start_vibration)

            #  send warning if the tempreture is too hot or vibration is too much
            if temperature >= warning_temp[1] and temperature < warning_temp[2]: 
                print("WARNING PIPE IS WARMING UP")
            if temperature >= warning_temp[2]: 
                print("COLD-RED PIPE IS HOT!!!")
            if vibration > limit_vibration:
                print(f"WARNING VIBRATION LIMIT REACHED. PIPE INTEGRETTY AT RISK.VIBRATION: {vibration}")
            # if the temp reaches the pipe limit then we simulate the user manually lowering it
            if temperature > limit_temperature:
                print("pipe temperture limit reached")
                temperature -= random.expovariate(1.0/interarrival) + (highest_temp / 3)
            else:
                temperature += random.expovariate(1.0/interarrival)

            # get the final tempreture 
            highest_temp = temperature
            
            # instead of yielding the arrival time, yield a Timeout Event
            yield env.timeout(interarrival,highest_temp)

            # to make things interesting, we add some printouts
            print( f'temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters')


# notifications need to be in diffenrt tables
# data can be generated in sec or min

# initlise the descrete event simulation enviroment
env = simpy.Environment()

sensor = simpy.Resource(env, capacity=1)

start_temperature = 24
# [good, warning, cold-red]
warning_temp = [start_temperature, 38, 39]
start_vibration = 10
limit_temperature = 40
limit_vibration = 1
sensor_interval_time = 20

env.process(pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp))

env.run(until=60)