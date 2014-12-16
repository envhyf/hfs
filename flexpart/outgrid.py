OUTGRID = open('OUTGRID', 'w')

OUTGRID_TOP="""********************************************************************************
*                                                                              *
*      Input file for the Lagrangian particle dispersion model FLEXPART        *
*                       Please specify your output grid                        *
*                                                                              *
********************************************************************************

1.  ------.----       4X,F11.4
       21.0000       GEOGRAFICAL LONGITUDE OF LOWER LEFT CORNER OF OUTPUT GRID
    OUTLONLEFT        (left boundary of the first grid cell - not its centre)

2.  ------.----       4X,F11.4
        34.0000       GEOGRAFICAL LATITUDE OF LOWER LEFT CORNER OF OUTPUT GRID
    OUTLATLOWER       (lower boundary of the first grid cell - not its centre)

3.  -----             4X,I5
      114               NUMBER OF GRID POINTS IN X DIRECTION (= No. of cells + 1)
    NUMXGRID

4.  -----             4X,I5
      114             NUMBER OF GRID POINTS IN Y DIRECTION (= No. of cells + 1)
    NUMYGRID

5.  ------.---        4X,F10.3
         0.070        GRID DISTANCE IN X DIRECTION
    DXOUTLON

6.  ------.---        4X,F10.3
         0.070        GRID DISTANCE IN Y DIRECTION
    DYOUTLAT

"""

OUTGRID.write(OUTGRID_TOP)

for i in xrange(1, 81):
  OUTGRID.write("%s. -----.-           4X, F7.1\n" % (i+6))
  OUTGRID.write("      %s.0\n" % (i*100))
  OUTGRID.write("    LEVEL 1           HEIGHT OF LEVEL (UPPER BOUNDARY)\n\n")

OUTGRID.close()
