#STARTTIME="2021/01/27 15:00:00.000"
STARTTIME=`date --date="-2 days" +"%Y/%m/%d %H:00:00.000"`
START=`date "+%s%3N" -d "$STARTTIME"`
ENDTIME=`date +"%Y/%m/%d %H:00:00.000"`
END=`date "+%s%3N" -d "$ENDTIME"`

FILENAME="data/BTCUSDT-"`date "+%Y-%m-%d-%H" -d "$ENDTIME"`."json"

CWD="/home/path_to_your_dir/python/macd-bot/"

echo "$START  $END"

echo "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=48&startTime=$START&endTime=$END" 

curl -s "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=48&startTime=$START&endTime=$END" \
    | python -m json.tool > $FILENAME


#python3 $CWD/main.py -g -d $FILENAME
