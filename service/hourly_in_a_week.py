import memcache
import pandas as pd
import time
client = memcache.Client([('127.0.0.1', 11211)])

def play_back_a_week(set_interval_seconds):

    eta_data = pd.read_csv('example/pickup_eta_data', delimiter=',', index_col = 'hour_index' ,\
                 names =['id', 'hour_in_week', 'hour_index', 'lat','lng','eta', 'canceled', 'timed_out','unavailable'])

    rides_data = pd.read_csv('example/week_hourly_level2', delimiter=',', index_col = 'hour_index' ,\
                 names =['lat','lng','hour_in_week','hour_index','ratio','app_open', 'request_hail'])
    start_time = min(rides_data.index.values)
    #start_time = 1409613839
    end_time = max(rides_data.index.values)

    if end_time > start_time :
        iters = int(end_time - start_time)
        c_location_set = []
        #print('start loading hourly!\n')
        #for i in range(0,iters):
        for i in range(134,145):
            temp_rides_data = rides_data.loc[rides_data.index == i ]
            #print temp_rides_data.size
            temp_eta_data = eta_data.loc[eta_data.index == i]
            rides_data_i = []
            eta_data_i = []
            for index, row in temp_rides_data.iterrows():
                rides_data_i.append( str(row['lat']) + ' '
                                      + str(row['lng']) + ' '
                                      + str(row['ratio']) + ' '
                                      + str(row['app_open']) + ' '
                                      + str(row['request_hail']))
            for index, row in temp_eta_data.iterrows():
                eta_data_i.append( str(row['lat']) + ' '
                                      + str(row['lng']) + ' '
                                      + str(row['eta']) + ' '
                                      + str(row['canceled']) + ' '
                                      + str(row['timed_out']) + ' '
                                      + str(row['unavailable'])
                                      )
            c_location_set.append({'hour_in_week':list(temp_rides_data['hour_in_week'])[0],
                                   'data': rides_data_i,
                                   'eta': eta_data_i
                                   })
        print('loading done!\n')
        while 0 < 1:
            for i in range(0,len(c_location_set)):
                client.set_multi(c_location_set[i], time=set_interval_seconds*2, key_prefix="pfx_")
                #print(latlng_data_rides[0])
                time.sleep(set_interval_seconds*1.000)

    else:
        print 'no ride data to process\n'

if __name__ == '__main__':
    play_back_a_week(3)
