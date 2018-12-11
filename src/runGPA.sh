NUM=$1

if [ "$NUM" -ge 1 -a "$NUM" -le 12 ]; then
  python lineCov.py gpa_b$NUM gpa grade.json
  python faultLoc.py tarantula
  python faultLoc.py crosstab
  python faultLoc.py barinel
else
  echo "Please enter a version number (1-12).."
fi
