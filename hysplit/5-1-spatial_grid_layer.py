import arcpy
import glob
import os
import pdb

workingDir = "F:/directory/with/merged/layers"
grid = "F:/grid.shp"

arcpy.env.workspace = workingDir
os.chdir(workingDir)

stations = glob.glob("*.shp")
print stations
stations.remove("grid.shp")

print "Define projections."
for station in stations:
    print "Started %s." % station
    arcpy.DefineProjection_management("%s/%s" % (workingDir, station),"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")    
    print "Done."

print "Spatial."
for station in stations:
    print "Started %s." % station
    arcpy.SpatialJoin_analysis("%s" % grid, "%s/%s" % (workingDir, station), "%s/merged_%s" % (workingDir, station),"JOIN_ONE_TO_ONE","KEEP_ALL","""Id "Id" true true false 6 Long 0 6 ,First,#,grid,Id,-1,-1;id_1 "id_1" true true false 11 Double 0 11 ,First,#,merge1,id,-1,-1""","INTERSECT","#","#")
    print "Done."