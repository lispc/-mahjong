for i in `seq 1 4`; 
do
  sleep i; 
  (python controller.py > output/log${i}.txt) &
done;
wait
