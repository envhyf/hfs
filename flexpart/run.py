"""Scripts runs flexpart with specified release box, time"""

from datetime import datetime, timedelta
import os
import subprocess
import csv

flexpart_dir = "/mnt/working/flexpart/"
#meteo_dir = raw_input("Meteo directory (e.g. /mnt/meteo/): ")
#output_dir = raw_input("Output directory (e.g. /tmp/out/): ")
#csv_source = raw_input("Location of the csv file containing run specifications (e.g. /home/user/runs.csv): ")

meteo_dir = "/mnt/meteo/aegean/"
out_dir = "/mnt/working/"
csv_source = "/mnt/working/scripts/runs.csv"

csv_input = csv.reader(open(csv_source, 'r'))

for line in csv_input:

  run_name = line[0]
  box = line[1].split()
  output_dir = out_dir + run_name + "/"
  
  if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

  # Create pathnames
  pathnames = "%soptions/\n%s\n%s\n%sAVAILABLE" % (flexpart_dir, output_dir, meteo_dir, meteo_dir)

  with open("%spathnames" % flexpart_dir, "w") as f:
    f.write(pathnames)
    f.flush()
    f.close()
    
  RELEASES ="\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 +++++++++++++++++ HEADER +++++++++++++++++++++\n\
 ++++++++++++++++++++++++++++++++++++++++++++++\n\
           1\n\
         001\n\
\n\
    20%s     %s\n\
    20%s     %s\n\
   %s\n\
   %s\n\
   %s\n\
   %s\n\
           1\n\
  0.0000000E+00\n\
   200.0000\n\
      %s\n\
      %s\n\
SAMPLE_1.0" % (line[2], line[3], line[4], line[5], box[0], box[1], box[2], box[3], line[6], line[6])

  with open("%soptions/RELEASES" % flexpart_dir, "w") as f:
    f.write(RELEASES)
    f.flush()
    f.close()

  run_end = datetime(2000+int(line[4][0:2]), int(line[4][2:4]), int(line[4][4:6]), \
    int(line[5][0:2]), int(line[5][2:4])) - timedelta(days=int(line[7]))
    
  COMMAND = "\
+++++++++++++ HEADER +++++++++++++++++\n\
+++++++++++++ HEADER +++++++++++++++++\n\
+++++++++++++ HEADER +++++++++++++++++\n\
+++++++++++++ HEADER +++++++++++++++++\n\
+++++++++++++ HEADER +++++++++++++++++\n\
+++++++++++++ HEADER +++++++++++++++++\n\
+++++++++++++ HEADER +++++++++++++++++\n\
-1\n\
%s\n\
20%s %s00\n\
3600\n\
3600\n\
   900\n\
 99999999\n\
900   SYNC\n\
-5.0  CTL\n\
4     IFINE\n\
1     IOUT\n\
1     IPOUT\n\
1     LSUBGRID\n\
1     LCONVECTION\n\
1     LAGESPECTRA\n\
0     IPIN\n\
1     IOFR\n\
0     IFLUX\n\
0     MDOMAINFILL\n\
2     IND_SOURCE\n\
2     IND_RECEPTOR\n\
0     MQUASILAG\n\
0     NESTED_OUTPUT\n\
0     LINIT_COND        INITIAL COND. FOR BW RUNS: 0=NO,1=MASS UNIT,2=MASS MIXING RATIO UNIT" \
  % (run_end.strftime("%Y%m%d %H%M00"), line[4], line[5])
    
  with open("%soptions/COMMAND" % flexpart_dir, "w") as f:
    f.write(COMMAND)
    f.flush()
    f.close()

  os.system("vim -c wq %soptions/COMMAND" % flexpart_dir)
  
  #os.system("./FLEXPART_GFORTRAN")
  os.chdir(flexpart_dir)
  h = subprocess.Popen("./FLEXPART_GFORTRAN", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  stdout, stderr = h.communicate()

  print stdout
  with open("log.run", "a") as f:
    f.write(stdout)
    f.write(stderr)
    f.close()
