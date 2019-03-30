NUM=$1

if [ "$NUM" -ge 1 -a "$NUM" -le 12 ]; then
  python3 lineCov.py gpa_b$NUM gpa grade.json
  python3 faultLoc.py tarantula
  python3 faultLoc.py crosstab
  python3 faultLoc.py barinel
else
  echo "Please enter a version number (1-12).."
fi
