env_name=$1
for i in 1
do
  date_str=`date +%Y.%m.%d_%H.%M.%S`
  echo " program start time : " + $date_str
  nohup python -u main.py --config=config.${env_name} > out/${env_name}_$date_str.txt 2>&1 &
  sleep 30
done
