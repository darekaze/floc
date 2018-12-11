python ./tc_generator/mid.gen.py
python lineCov.py mid_b1 mid mid.json
python faultLoc.py tarantula
python faultLoc.py crosstab
python faultLoc.py barinel
