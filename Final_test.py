import osmnx as ox 
from datetime import datetime,timedelta 
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo










def location():

    
    

    all_address={} 

    address_data=False

    allowed_methods=["walk","drive","bike"]

    method_data=False


    while not method_data:

     user_method=input("What is your preffered method of travel? walk,drive or bike?")


     if user_method not in allowed_methods:
         
         
         user_method=input("Invalid, please use walk,bike, or drive")

     

     else:
         
         all_address["method"]=user_method

         method_data=True



         

     
       
    while not address_data:    #used to try to except to catch any or all errors, OSMNX is very strict with what addresses are allowed and OSM does not have some

        
        user_address=input("What is your address")




        try:  #I know AI uses this often, couldnt find alternative when ox.geocode fails to locate address. 

            ox.geocode(user_address)

            all_address["address"]=ox.geocode(user_address)

            all_address["name_address"]=user_address






            address_data=True 

            
        except Exception:
                
                user_address=input("Invalid address try again, include county or state") 

     


    

    destination_data=False 

    while not destination_data:
         

         user_destination=input("What is your destination?")


         try:
              
              ox.geocode(user_destination)



              all_address["destination"]=ox.geocode(user_destination) 
              
              destination_data=True

         except Exception:
              

              user_destination=input("Invalid, Try again, include county and state") 




    return all_address 









def graph():
    




    location_data=location() 


    address=location_data["address"]


    name_address=location_data["name_address"]





    a_lat,a_lon=address


    destination=location_data["destination"] 


    d_lat,d_lon=destination



    method=location_data["method"]


    distance=0



    if method == "walk":
        distance=1000

     
    if method=="bike":
        
        distance=2000

     
    if method=="drive":
        
        distance=3000



    Map = ox.graph_from_address(name_address, dist=distance, network_type=method)



    Arrival_node=ox.nearest_nodes(Map,a_lon, a_lat) 



    destination_node=ox.nearest_nodes(Map,d_lon,d_lat) 



    Map=ox.add_edge_speeds(Map)



    Map=ox.add_edge_travel_times(Map)




    route=ox.shortest_path(Map,Arrival_node,destination_node,weight="travel_time",cpus=1)




    gdf = ox.routing.route_to_gdf(Map, route)


    total_seconds = gdf["travel_time"].sum()


    location_data["seconds"] = total_seconds



    fig,ax=ox.plot_graph_route(Map,route,route_color="r",route_linewidth=4,node_size=0,route_alpha=1) 



    return (fig,ax), location_data




def time_calculation():



     route_map,location_data=graph()


     address=location_data["address"]


     seconds=location_data["seconds"]



     minutes_time = seconds / 60

     hours_time = seconds / 3600


     


     a_lat,a_lon=address


     tf = TimezoneFinder()

     tz = tf.timezone_at(lat=a_lat, lng=a_lon)

     
     local_time = datetime.now(ZoneInfo(tz))


     ETA = local_time + timedelta(seconds=seconds)

     ETA=ETA.strftime("%I:%M %p") 

     location_data["ETA"]=ETA

     location_data["Hours"]=hours_time

     location_data["Minutes"]=minutes_time


     return route_map, location_data






def main():


     map_plot,location_data=time_calculation() 

     ETA=location_data["ETA"]

     Hours=location_data["Hours"]

     Minutes=location_data["Minutes"]


     print("Your ETA is", ETA, "It will take" ,Hours, "and", Minutes)


     fig,ax=map_plot 

     import matplotlib.pyplot as plot 

     plot.show() 




main()









     










  















    



























