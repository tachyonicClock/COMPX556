



build: packing.cpp placement.cpp neighbourhood.h lns.h destruction.cpp lns.cpp repair.cpp packing.h
	g++ -o packing packing.cpp placement.cpp lns.cpp destruction.cpp repair.cpp

BL: build
	./packing BL problems/problem1.csv placements/1_BL.txt placements/1_BL.csv
	./packing BL problems/problem2.csv placements/2_BL.txt placements/2_BL.csv
	./packing BL problems/problem3.csv placements/3_BL.txt placements/3_BL.csv
	./packing BL problems/problem4.csv placements/4_BL.txt placements/4_BL.csv
	python3 renderer.py -o placements/1_BL.png --height 50  -i placements/1_BL.txt
	python3 renderer.py -o placements/2_BL.png --height 150 -i placements/2_BL.txt
	python3 renderer.py -o placements/3_BL.png --height 500 -i placements/3_BL.txt
	python3 renderer.py -o placements/4_BL.png --height 400 -i placements/4_BL.txt

LS: build
	./packing LS problems/problem1.csv placements/1_LS.txt placements/1_LS.csv
	python3 renderer.py -o placements/1_LS.png --height 50  -i placements/1_LS.txt
	# ./packing LS problems/problem2.csv placements/2_LS.txt placements/2_LS.csv
	# ./packing LS problems/problem3.csv placements/3_LS.txt placements/3_LS.csv
	# ./packing LS problems/problem4.csv placements/4_LS.txt placements/4_LS.csv
	# python3 renderer.py -o placements/2_LS.png --height 150 -i placements/2_LS.txt
	# python3 renderer.py -o placements/3_LS.png --height 500 -i placements/3_LS.txt
	# python3 renderer.py -o placements/4_LS.png --height 400 -i placements/4_LS.txt


LNS: build
	./packing LNS problems/problem1.csv placements/1_LNS.txt placements/1_LNS.csv
	python3 renderer.py -o placements/1_LNS.png --height 50  -i placements/1_LNS.txt
	# ./packing LNS problems/problem2.csv placements/2_LNS.txt placements/1_LNS.csv
	# python3 renderer.py -o placements/2_LNS.png --height 150 -i placements/2_LNS.txt
	# ./packing LNS problems/problem3.csv placements/3_LNS.txt placements/3_LNS.csv
	# python3 renderer.py -o placements/3_LNS.png --height 500 -i placements/3_LNS.txt
	# ./packing LNS problems/problem4.csv placements/4_LNS.txt placements/4_LNS.csv
	# python3 renderer.py -o placements/4_LNS.png --height 400 -i placements/4_LNS.txt

ALNS: build
	./packing ALNS problems/problem1.csv placements/1_ALNS.txt placements/1_ALNS.csv --max-iterations 5000 --annealing
	python3 renderer.py -o placements/1_ALNS.png --height 50  -i placements/1_ALNS.txt
	# ./packing ALNS problems/problem2.csv placements/2_ALNS.txt placements/2_ALNS.csv --max-iterations 1000 --annealing
	# python3 renderer.py -o placements/2_ALNS.png --height 150 -i placements/2_ALNS.txt
	# ./packing ALNS problems/problem3.csv placements/3_ALNS.txt placements/3_ALNS.csv --max-iterations 1000 --annealing
	# python3 renderer.py -o placements/3_ALNS.png --height 500 -i placements/3_ALNS.txt
	# ./packing ALNS problems/problem4.csv placements/4_ALNS.txt
	# python3 renderer.py -o placements/4_ALNS.png --height 400 -i placements/4_ALNS.txt
