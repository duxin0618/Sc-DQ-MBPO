env_name=$1
date_str=`date +%Y.%m.%d_%H.%M.%S`
echo " program start time : " + $date_str
python -u main.py --config=config.${env_name}

