# floc

A collection of self-implementation **f**ault **loc**alization tools

## Instruction

> **TL;DR** Try run the bash files (`runGPA.sh`)

1. Generate some random sample data generators:
```
python3 tc_generator/grade.gen.py
```

2. Generate the coverage matrix:
```
python3 lineCov.py gpa_b3 gpa grade.json
```

3. Run faultLoc.py to print out debugging result
```
python3 faultLoc.py tarantula
```

## Commands

#### Sample data generators
```
mid.gen.py [-c] [-r]
-c, --tc     (int) number of test cases to generate (default: 100)
-r, --range  (int) range of the list (from 0 to n) (default: n=20)

grade.gen.py [-c] [-n] [--name]
-c, --tc  (int) number of test cases to generate (default: 100)
-n, --el  (int) number of element inside each test case (default: 5)
--name    (str) The name of the output file (in .json) (default: grade)
```

#### Line Coverage
```
lineCov.py module func src
module  (str) Name of the program that needs to be tested in /tmods
func    (str) Name of the entry function
src     (str) Name of the JSON file containing the test cases in /testCases
```

#### Fault Localization
```
faultLoc.py tech
tech  (str) Name of the debugging technique

Available techniques: 
  tarantula, crosstab, barinel...
```

## Contributors

[@DaRekaze](https://github.com/darekaze) // [@reynoldpolyu](https://github.com/reynoldpolyu) // [@alisonsyxu](https://github.comalisonsyxu)
