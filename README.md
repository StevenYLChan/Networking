# Networking
#### Project 1 - Error Detection and Error Correction
A simulation of independent and burst errors with the resulting throughput and confidence intervals.
######Usage: 
  -python3 error_simulation.py argM argA argK argF argE argB argN argR argT argTx  
	ex. python3 a1.py I 50 0 4000 0.0001 0 0 5000000 5 24 24 70 83 53

######Output:
  -Throughput
  
  -Confidence Intervals

#### Project 2 - Routing Algorithms
A simulation of link-state, distance vector, hot potato I, hot potato II routing algorithms. 
######Usage: 
Single Run

	Python3 routing_simulation.py _list_file.txt
	
Batch Run

	Python3 batch_routing_simulation.py line_list_file.txt mesh_list_file.txt star_list_file.txt complete_list_file.txt tree_list_file.txt ring_list_file.txt adjacency_list_file.txt

######Output:
  -average transmissions
  
  -average path lengths
  
  -confidence intervals
