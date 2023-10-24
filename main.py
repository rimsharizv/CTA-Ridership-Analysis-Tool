#
# Name: Rimsha Rizvi
# Project: Analyzing CTA2 L data in Python
#   This is a menu based project that retrieves data from CTA2 L daily ridership database and computes them according to the selected option
#

import sqlite3
import matplotlib.pyplot as plt

##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
    
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute("Select MIN(date(ride_date)), MAX(date(ride_date)) From Ridership;")
    row = dbCursor.fetchone();
    print("  date range:", row[0], '-', row[1])
  
    dbCursor.execute("Select sum(num_riders) From Ridership;")
    row = dbCursor.fetchone();
    print("  Total ridership:", f"{row[0]:,}")

    all_days = row[0]  # value of the total ridership

    dbCursor.execute("Select sum(num_riders) From Ridership where type_of_day = 'W';")
    row = dbCursor.fetchone();
    perc = 100 * (row[0]/all_days)  # calculating percentage of weekday/total
    print("  Weekday ridership:", f"{row[0]:,}", f"({perc:.2f}%)")

    dbCursor.execute("Select sum(num_riders) From Ridership where type_of_day = 'A';")
    row = dbCursor.fetchone();
    perc = 100 * (row[0]/all_days)  # calculating percentage of saturday/total
    print("  Saturday ridership:", f"{row[0]:,}", f"({perc:.2f}%)")

    dbCursor.execute("Select sum(num_riders) From Ridership where type_of_day = 'U';")
    row = dbCursor.fetchone();
    perc = 100 * (row[0]/all_days)  # calculating percentage of (sunday/holiday)/total
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({perc:.2f}%)")


##################################################################  
#
# Command "1"
#
# Retrieving station name that are similar to the user-input station.
#
def command1(dbConn):
  print()
  
  dbCursor = dbConn.cursor()
  stationname = input("Enter partial station name (wildcards _ and %): ")
  sql = 'select station_id, station_name from stations where station_name like "'+ stationname +'" group by station_name order by station_name;'
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  
  if len(rows) == 0:
    print("**No stations found...", end = '\n')
  else:
    for row in rows:
      id = row[0]
      name = row[1]
      print(id, ":", name)

##################################################################  
#
# Command "2"
#
# Retrieves and outputs ridership at each station along with a percentage that compares it to total L ridership
#

# total - calculates the overall sum of num riders from ridership
def total(dbConn):  # This function is used in command 2, 3, 4
  dbCursor = dbConn.cursor()
  sql = 'select sum(num_riders) from ridership;'
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  for row in rows:
    ridership = row[0]
  return ridership

def command2(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership all stations **", end = "\n")
  sql = 'select station_name, sum(num_riders) from Ridership join stations where(Ridership.station_id = stations.station_id) group by station_name order by station_name;'
  
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("**No stations found...", end = '\n')
  else:
    for row in rows:
      stationname = row[0]
      ridership = row[1]
      num_riders = total(dbConn)
      percentage = round(ridership*100/num_riders, 2); # calculates percentage of ridership/total riders
      print(stationname, ":", f"{ridership:,}", f"({percentage:.2f}%)")

##################################################################  
#
# Command "3"
#
# Outputs the top-10 busiest stations in terms of ridership (descending order)
#
def command3(dbConn):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **", end = "\n")
  sql = 'select station_name, sum(num_riders) from Ridership join stations where(Ridership.station_id = stations.station_id) group by station_name order by sum(num_riders) desc limit 10;'
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("**No stations found...", end = '\n')
  else:
    for row in rows:
      stationname = row[0]
      ridership = row[1]
      num_riders = total(dbConn)
      percentage = round(ridership*100/num_riders, 2); # calculates percentage of ridership/total riders
      print(stationname, ":", f"{ridership:,}", f"({percentage:.2f}%)")

##################################################################  
#
# Command "4"
#
# Outputs the top-10 least busiest stations in terms of ridership (ascending order)
#
def command4(dbConn):
  dbCursor = dbConn.cursor()
  print("** least-10 stations **", end = "\n")
  sql = 'select station_name, sum(num_riders) from Ridership join stations where(Ridership.station_id = stations.station_id) group by station_name order by sum(num_riders) asc limit 10;'
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("done", end = '\n')
  else:
    for row in rows:
      stationname = row[0]
      ridership = row[1]
      num_riders = total(dbConn)
      percentage = round(ridership*100/num_riders, 2); # calculates percentage of ridership/total riders
      print(stationname, ":", f"{ridership:,}", f"({percentage:.2f}%)")

##################################################################  
#
# Command "5"
#
# Recieves a color from the user and outputs all stop names that are within that line color
#

# ifcolorExists - function that returns 0 (false) or 1 (true) if the color exists in Lines
def ifcolorExists(dbConn, color):
  dbCursor = dbConn.cursor()
  sql = "select 1 from lines where exists (select color from lines where color='"+color+"');"
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  if len(rows) == 0:
    return 0;
  else:
    for row in rows:
      if row[0] == 1:
        return 1
  return 0

def command5(dbConn):
  print()
  # .capitalize() makes sure the first character is in upper case
  color = input("Enter a line color (e.g. Red or Yellow): ").lower().capitalize()

  # Capitalize() doesn't cover Purple-Express
  if color == "Purple-express":
    color = "Purple-Express"
    
  ifExists = ifcolorExists(dbConn, color)
  if ifExists == 0:
    print("**No such line...", end = '\n')
  else:
    sql = 'select stop_name, direction, ada from stops join lines join stopdetails where stops.stop_id = stopdetails.stop_id and stopdetails.line_id = lines.line_id and lines.color = "'+color+'" group by stop_name order by stop_name;'
    dbCursor = dbConn.cursor()
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    if len(rows) == 0:
      print("", end = '\n')
    else:
      for row in rows:
        stop_name = row[0]
        direction = row[1]
        if row[2] == 1:  # Is it accessible?
          accessible = 'yes'
        else:
          accessible = 'no'
        print(stop_name, ": direction =", direction, "(accessible?",accessible+")")

##################################################################  
#
# Command "6"
#
# Retrieves and outputs total ridership by month in ascending order.
# The plot graphs number of riders per month
#
def command6(dbConn):
  dbCursor = dbConn.cursor()
  sql = "select strftime('%m', ride_date) as Month, sum(num_riders) from ridership group by Month order by Month;"
  dbCursor.execute(sql)
  print("** ridership by month **")
  rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("", end = "\n")
    return
  else:
    for row in rows:
      month = row[0]
      ridership = row[1]
      print(month, ":", f"{ridership:,}")

  print()
  plot = input("Plot? (y/n)")
  if(plot == "n"):
    return
  elif(plot == "y"):
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    x = []
    y = []
    if len(rows) == 0:
      print("", end = "\n")
    else:
      for row in rows:
        # adding month and number of riders in lists
        x.append(row[0])
        y.append(row[1])
      # plotting the graph
      plt.xlabel("month")
      plt.ylabel("number of riders (x * 10^8)")
      plt.title("monthly ridership")
      plt.plot(x,y)
      plt.show()

##################################################################  
#
# Command "7"
#
# Retrieves and outputs total ridership by year in ascending order.
# The plot graphs number of riders per year
#
def command7(dbConn):
  dbCursor = dbConn.cursor()
  sql = "select strftime('%Y', ride_date) as Year, sum(num_riders) from ridership group by Year order by Year;"
  dbCursor.execute(sql)
  print("** ridership by year **")
  rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("", end = "\n")
    return
  else:
    for row in rows:
      month = row[0]
      ridership = row[1]
      print(month, ":", f"{ridership:,}")

  print()
  plot = input("Plot? (y/n)")
  if(plot == "n"):
    return
  elif(plot == "y"):
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    x = []
    y = []
    if len(rows) == 0:
      print("", end = "\n")
    else:
      for row in rows:
        # adding year and number of riders in lists
        x.append(row[0])
        y.append(row[1])
    # plotting the graph
    plt.xlabel("Years")
    plt.ylabel("Ridership Number")
    plt.title("Ridership per year")
    plt.plot(x,y)
    plt.show()


##################################################################  
#
# Command "8"
#
# Retrieves the daily ridership of the two input stations and outputs the first 5 days and last 5 days
# The plot graphs number of riders per each day over the specified year
#

# c8helper - returns number of stations from the given input station_name to check if none, multiple or 1 station found
def c8helper(dbConn, station_name):
  dbNumStat = dbConn.cursor()
  sql = "select count(*) from stations where station_name like '"+station_name+"';"
  dbNumStat.execute(sql)
  rows = dbNumStat.fetchall()
  return rows[0][0]


def command8(dbConn):
  print()
  year = input("Year to compare against? ")
  print()
  station1 = input("Enter station 1 (wildcards _ and %): ")
  num_stations = c8helper(dbConn, station1)

  # checking if there's only one station like the first station input
  if(num_stations<1):
    print("**No station found...", end = "\n")
    return
  elif num_stations>1:
    print("**Multiple stations found...")
    return
  else:
    print()
    station2 = input("Enter station 2 (wildcards _ and %): ")
    num_stations = c8helper(dbConn, station2)
    # checking if there's only one station like the second station input
    if(num_stations<1):
      print("**No station found...", end = "\n")
      return
    elif num_stations>1:
      print("**Multiple stations found...")
      return
    else:
      dbStation1 = dbConn.cursor()
      sqlstat1 = "select station_id, station_name from stations where station_name like '"+station1+"';"
    
      dbStation1.execute(sqlstat1)
      rows1 = dbStation1.fetchall()
      
      dbStation2 = dbConn.cursor()
      sqlstat2 = "select station_id, station_name from stations where station_name like '"+station2+"'"
      dbStation2.execute(sqlstat2)
      rows2 = dbStation2.fetchall()

      # Storing the id for both stations
      id1 = rows1[0][0]
      id2 = rows2[0][0]
      # Storing the station names for both stations
      station1 = rows1[0][1]
      station2 = rows2[0][1]
      
      print("Station 1:",id1,station1, end = "\n")
    
      dbCursor = dbConn.cursor()
      sql = "select ridership.ride_date, ridership.num_riders from ridership, stations where stations.station_id = ridership.station_id and stations.station_name = '"+station1+"' and strftime('%Y', ridership.ride_date) = '"+year+"' group by ridership.ride_date;"
      
      dbCursor.execute(sql)
      rows = dbCursor.fetchall()
      # storing total ridership for all days for station 1
      date1 = []
      ridership1 = []
      if len(rows) == 0:
        print("", end = "\n")
      else:
        for row in rows:
          dateval = row[0].split()
          date1.append(dateval[0])
          ridership1.append(row[1])
        for i in range(5):  # prints the first 5 days of daily ridership
          print(date1[i], ridership1[i], end = "\n")
        for j in range(-5,0):  # prints the last 5 days of daily ridership
          print(date1[j], ridership1[j], end = "\n")
      print("Station 2:",id2,station2, end = "\n")
    
      dbCursor = dbConn.cursor()
      sql = "select ridership.ride_date, ridership.num_riders from ridership, stations where stations.station_id = ridership.station_id and stations.station_name = '"+station2+"' and strftime('%Y', ridership.ride_date) = '"+year+"' group by ridership.ride_date;"
      
      dbCursor.execute(sql)
      rows = dbCursor.fetchall()
      # storing total ridership for all days for station 2
      date2 = []
      ridership2 = []
      if len(rows) == 0:
        print("", end = "\n")
      else:
        for row in rows:
          dateval = row[0].split()
          date2.append(dateval[0])
          ridership2.append(row[1])
        for i in range(5):  # prints the first 5 days of daily ridership
          print(date2[i], ridership2[i], end = "\n")
        for j in range(-5,0):  # prints the last 5 days of daily ridership
          print(date2[j], ridership2[j], end = "\n")
  
      print()
      # plotting graph
      plot = input("Plot? (y/n) ")
      if(plot == 'n'):
        return
      else:
        date1size = len(date1)
        day = list(range(0, date1size))
          
        plt.plot(day, ridership1, label = station1)
        plt.plot(day, ridership2, label = station2)
        plt.xlabel("day")
        plt.ylabel("number of riders")
        plt.legend(loc="upper right")
        title = "riders each day of "+year
        plt.title(title)
        plt.show()
  

##################################################################  
#
# Command "9"
#
# Retrieving and output all station names that are a part of the specified line color
# The plot graphs the locations of the stations overlaying a map of Chicagoland
#
def command9(dbConn):
  print()
  dbCursor = dbConn.cursor()
  color = input("Enter a line color (e.g. Red or Yellow): ").lower().capitalize()

  # Capitalize() doesn't cover Purple-Express
  if color == "Purple-express":
    color = "Purple-Express"

  sql = 'select distinct stations.station_name, stops.latitude, stops.longitude from stations join stops join stopdetails join lines where lines.line_id = stopdetails.line_id and stops.stop_id = stopdetails.stop_id and stations.station_id = stops.station_id and lines.color = "'+color+'" group by stations.station_name order by stations.station_name;'
  
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  # storing station names, latitude and longitude in lists
  nameslist = []
  latlist = []
  longlist = []
  if len(rows) == 0:
    print("**No such line...")
    return;
  else:
    for row in rows:
      name = row[0]
      lat = row[1]
      long = row[2]
      # saving as lists to plot later
      nameslist.append(name)
      latlist.append(lat)
      longlist.append(long)
      
    for i in range(len(nameslist)):
      print(nameslist[i], ": ("+ str(latlist[i])+",", str(longlist[i])+")")

  print()
  inp = input("Plot? (y/n) ")
  if(inp == 'n'):
    return
  else:
    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    plt.imshow(image, extent=xydims)

    if (color.lower() == "purple-express"):
      color="Purple"
      
    plt.title(color + " line")

    plt.plot(longlist, latlist, "o", c=color)
    for i in range(len(latlist)):
      plt.annotate(nameslist[i], (longlist[i], latlist[i]))

    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])

    plt.show()
      
##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

print()

inp = input('Please enter a command (1-9, x to exit): ')
# menu system
while (inp != "x"):
  if inp == "1":
    command1(dbConn)
  elif inp == "2":
    command2(dbConn)
  elif inp == "3":
    command3(dbConn)
  elif inp == "4":
    command4(dbConn)
  elif inp == "5":
    command5(dbConn)
  elif inp == "6":
    command6(dbConn)
  elif inp == "7":
    command7(dbConn)
  elif inp == "8":
    command8(dbConn)
  elif inp == "9":
    command9(dbConn)
  else:
    print("**Error, unknown command, try again...")

  print()
  inp = input('Please enter a command (1-9, x to exit): ')

#
# done
#