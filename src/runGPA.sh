NUM=$1

if [ -n "$NUM" ]; then
  python lineCov.py gpa_b$NUM gpa grade.json
  python faultLoc.py tarantula
  python faultLoc.py crosstab
  python faultLoc.py dstar
else
  echo "Please enter a version number (1-12).."
fi
