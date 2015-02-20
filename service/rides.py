import pandas as pd



class rides_api:
    def __init__(self, rdata):
        self.rdata = rdata
    def status(self):
        gh_set = set(self.rdata['gh'])
        counts_in_gh = []
        #print(self.ddata)
        for gh in gh_set:
            gh_reverse = Geohash.decode_exactly(gh)
            data_list = []
            data_list.append(gh_reverse[0]-gh_reverse[2])
            data_list.append(gh_reverse[0]+gh_reverse[2])
            data_list.append(gh_reverse[1]-gh_reverse[3])
            data_list.append(gh_reverse[1]+gh_reverse[3])
            r_complete = set((self.rdata.loc[ (self.rdata['gh'] == gh) & (self.rdata['state'] == 'completed') ])['distinct_id'])
            r_failed = set((self.rdata.loc[ (self.rdata['gh'] == gh) & (self.rdata['state'] == 'failed') ])['distinct_id'])
            r_canceled = set((self.rdata.loc[ (self.rdata['gh'] == gh) & (self.rdata['state'] == 'canceled') ])['distinct_id'])

            data_list.append(len(r_complete))        ## copmleted rides
            data_list.append(len(r_failed))        ## failed rides
            data_list.append(len(r_canceled))       ## canceled rides
            counts_in_gh.append(" ".join(list(str(x) for x in data_list)))
        return(counts_in_gh)

    def create_stream_rides(sample_interval_hour, set_interval_seconds, hash_level):
        global latlng_data_rides
        global c_timestamp_rides
        rides_data = pd.read_csv('/Users/xianyun/Documents/mixpanel/rides_status.txt', delimiter=',', index_col = 'created_at' ,\
                     na_values =['"N'],names =['ride_id','created_at','lat','lng','hailed_at', 'status'])
        start_time = min(rides_data.index.values)
        start_time = 1409613839
        end_time = max(rides_data.index.values)

        if end_time > start_time :
            iters = int(round( (end_time - start_time)/3600/sample_interval_hour))

            for i in range(0,iters):
                temp_rides_data = rides_data.loc[(rides_data.index> start_time + i*3600*sample_interval_hour) & (rides_data.index< start_time + (i+1)*3600*sample_interval_hour) ]
                #print temp_rides_data.size
                rides_data_i = []
                for index, row in temp_rides_data.iterrows():
                    rides_data_i.append( {'gh':Geohash.encode(row['lat'], row['lng'])[0:hash_level], 'distinct_id':row['ride_id'], 'state':row['status']})
                rides_data_i = pd.DataFrame(rides_data_i)

                c_location_set = rides_api( rides_data_i)
                latlng_data_rides_c.append( c_location_set.status() )
                c_timestamp_rides_c.append( start_time + i*3600*sample_interval_hour)

            print('loading done!')
            while 0 < 1:
                for i in range(0,len(latlng_data_rides_c)):

                    latlng_data_rides = latlng_data_rides_c[i]
                    c_timestamp_rides = c_timestamp_rides_c[i]
                    #print(latlng_data_rides[0])
                    time.sleep(set_interval_seconds*1.000)

        else:
            print 'no ride data to process\n'
