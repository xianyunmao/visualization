import pandas as pd


class locations_api:
    def __init__(self, pdata, ddata):
        self.pdata = pdata
        self.ddata = ddata
    def status(self):
        gh_set = set(self.pdata['gh']) | set(self.ddata['gh'])
        counts_in_gh = []
        #print(self.ddata)
        for gh in gh_set:
            gh_reverse = Geohash.decode_exactly(gh)
            data_list = []
            data_list.append(gh_reverse[0]-gh_reverse[2])
            data_list.append(gh_reverse[0]+gh_reverse[2])
            data_list.append(gh_reverse[1]-gh_reverse[3])
            data_list.append(gh_reverse[1]+gh_reverse[3])
            p_in_hail_set = set((self.pdata.loc[ (self.pdata['gh'] == gh) & (self.pdata['state'] == 'in_hail') ])['distinct_id'])
            p_open_app_set = set((self.pdata.loc[ (self.pdata['gh'] == gh) & (self.pdata['state'] == 'app_open') ])['distinct_id'])
            d_in_hail_set = set((self.ddata.loc[ (self.ddata['gh'] == gh) & (self.ddata['state'] == 'in_hail') ])['driver_id'])
            d_available_set = set((self.ddata.loc[ (self.ddata['gh'] == gh) & (self.ddata['state'] == 'available') ])['driver_id'])
            d_occupied_set = set((self.ddata.loc[ (self.ddata['gh'] == gh) & (self.ddata['state'] == 'occupied') ])['driver_id'])

            data_list.append(len(p_in_hail_set))        ## pax in hail count
            data_list.append(len(p_open_app_set) - len(p_in_hail_set & p_open_app_set) )   ## pax open app count excluding in_hail
            data_list.append(len(d_in_hail_set))        ## driver in hail count
            data_list.append(len(d_occupied_set))       ## driver occupied count
            data_list.append(len(d_available_set) - len(d_available_set & (d_occupied_set | d_in_hail_set) ))
            counts_in_gh.append(" ".join(list(str(x) for x in data_list)))
        return(counts_in_gh)

    def create_stream(sample_interval_min, set_interval_seconds, hash_level):
        global latlng_data
        global c_timestamp
        pax_data = pd.read_csv('/Users/xianyun/Documents/program1/passenger_locations', delimiter=';', index_col = 'time' ,\
                     na_values =['"N'],names =['state','lat','lng','distinct_id', 'time'])
        drx_data = pd.read_csv('/Users/xianyun/Documents/program1/driver_locations', delimiter=',', index_col = 'time' ,\
                     na_values =['"N'],names =['driver_id','state', 'time', 'lat','lng', 'prec'])
        start_time = max( min(pax_data.index.values), min(drx_data.index.values))
        end_time = min( max(pax_data.index.values), max(drx_data.index.values))

        if end_time > start_time :
            iters = (end_time - start_time)/60/sample_interval_min
            while 0 < 1:
                for i in range(0,iters):
                    temp_pax_data = pax_data.loc[(pax_data.index>start_time + i*60*sample_interval_min) & (pax_data.index< start_time + (i+1)*60*sample_interval_min) ]
                    temp_drx_data = drx_data.loc[(drx_data.index>start_time + i*60*sample_interval_min)  & (drx_data.index< start_time + (i+1)*60*sample_interval_min) ]
                    pax_data_i = []
                    drx_data_i = []
                    for index, row in temp_pax_data.iterrows():
                        pax_data_i.append( {'gh':Geohash.encode(row['lat'], row['lng'])[0:hash_level], 'distinct_id':row['distinct_id'], 'state':row['state']})
                    for index, row in temp_drx_data.iterrows():
                        drx_data_i.append( {'gh':Geohash.encode(row['lat'], row['lng'])[0:hash_level], 'driver_id':row['driver_id'], 'state':row['state']})
                    pax_data_i = pd.DataFrame(pax_data_i)
                    drx_data_i = pd.DataFrame(drx_data_i)

                    c_location_set = locations_api(pax_data_i, drx_data_i)
                    latlng_data = c_location_set.status()
                    c_timestamp = start_time + (i+1)*60*sample_interval_min
                    #print latlng_data[0]
                    time.sleep(set_interval_seconds)

        else:
            print 'no overlap between driver data and pax data! no data to process\n'
