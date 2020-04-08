import requests
import pandas as pd
from fugle_realtime import intraday
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config import FUGLE_API_TOKEN,ACCESS_TOKEN
from PIL import Image
from io import BytesIO

#TODO
# string：菜雞，菜雞
# number：股票代碼
# string：適合買嗎？/ 適合賣嗎？
# string：給我圖表 / 給我蠟燭
# string：最佳五檔
# string：注冊某某 API
# string：好友清單
# string：發給某某（全部）

class TelegramBot:
    def __init__(self):
        """
        Initialize and create use constant variable.
        """
        self.chat_id = None
        self.in_msg = None
        self.first_name = None
        self.last_name = None
        self.api_db = {}
        self.share_db = {}
        self.temp_msg = ''
        self.temp_share_no = ''
        self.prev_action = ''
        self.out_msg = ''
        self.import_share_no()

    def process_data(self,in_msg):
        """
        To process and assign the first hand data.
        """
        in_msg = in_msg['message']

        # Assign to variable
        self.chat_id = in_msg['chat']['id']
        self.first_name = in_msg['from']['first_name']
        self.last_name = in_msg['from']['last_name']
        self.content = in_msg['text']

    def data_message_judge(self):
        """
        Main function to classify the situation.
        """
        success = None # To make sure message had been sent
        
        # To double-check that previous action
        if str(self.content) in self.share_db.keys():
            keyword = self.content
            success = self.serv_share_num(keyword,None)
            return success
        else:
            msg_received = self.content
            keyword = msg_received[:2]

        # Start with the sentence response function
        if keyword in ['菜雞','/s']: # serv_greeting
            success = self.serv_greeting()
        elif keyword in ['代號','股票','代碼','serv_share_num']: # serv_share_num
            success = self.serv_share_num(keyword,msg_received)
        elif keyword in ['適合','建議','serv_buy_sell']: # serv_buy_sell
            success = self.serv_buy_sell(keyword,msg_received)
        elif keyword in ['給我','serv_candle_stick']: # serv_candle_stick
            success = self.serv_candle_stick(keyword,msg_received)
        elif keyword in ['最佳','serv_top_share']: # serv_top_share
            success = self.serv_top_share()
        elif keyword in ['注冊']: # serv_api_register
            success = self.serv_api_register(msg_received)
        elif keyword in ['好友']: # serv_friend_list
            success = self.serv_friend_list()
        elif keyword in ['發送','轉發','分享','轉送','發給']: # serv_forward_msg
            success = self.serv_forward_msg(keyword,msg_received)
        else: # serv_others
            success = self.serv_others(msg_received)
        self.prev_action = ''

        # Return Boolean as confirmation
        return success

    def serv_greeting(self):
        """
        A welcome content for greeting.
        """
        print('【serv_greeting】')
        user_name = self.first_name + self.last_name
        text = "您好"+ user_name +"，菜雞非常高興能夠爲您服務。您可輸入以下關鍵字：\n\
                📌 查詢股票資訊【代碼、股票、代號】\n\
                📌 當冲交易 【適合、建議】\n\
                📌 查詢K綫圖【給我圖標（蠟燭）】\n\
                📌 至多最佳5檔【最佳x檔】\n\
                📌 注冊好友API【注冊 名稱 API】\n\
                📌 轉發資訊給好友【轉發 名稱】\n "
        self.out_msg = text
        success = self.send_message()
        return success

    def serv_share_num(self,keyword,msg_received):
        """
        To find out the latest price by share number.
        """
        print('【serv_share_num】')

        # Check whether is previous action
        if msg_received == None:
            share_no = keyword
        else:
            share_no = msg_received.split('{}'.format(keyword))[1]

        # Collect data from FUGLE API
        share_data = intraday.chart(apiToken = FUGLE_API_TOKEN,symbolId = '{}'.format(share_no), output = 'raw')
        
        # Template for Share detail
        try:
            share_date_time = list(share_data.keys())[-1]
            share_res = share_data[share_date_time]
            share_res_date_time = share_date_time.split('T')
            text = "【{} 最新資訊】\n\
                    🔺行業類別：{}\n\
                    🔺日期：{}\n\
                    🔺時間：{}\n\
                    🔺開盤價：{}\n\
                    🔺收盤價：{}\n\
                    🔺最高價：{}\n\
                    🔺最低價：{}\n\
                    🔺交易張數：{}\n\
                    🔺交易量：{}\n ".format(share_no, \
                                        self.share_db[share_no], \
                                        share_res_date_time[0], \
                                        share_res_date_time[1].split('.')[0], \
                                        share_res['open'], \
                                        share_res['close'], \
                                        share_res['high'], \
                                        share_res['low'], \
                                        share_res['unit'], \
                                        share_res['volume'])
        except:
            text = "非常抱歉，菜雞能力不及 😥，請重新輸入有效股票代號！"
            self.prev_action = "serv_share_num"
        self.out_msg = self.temp_msg = text
        self.temp_share_no = share_no
        success = self.send_message()
        return success

    def serv_buy_sell(self,keyword,msg_received):
        """
        To get information for buy sell in a day.
        """
        print('【serv_buy_sell】')

        # Check whether has share number in memory
        if self.temp_share_no:
            share_data = intraday.meta(apiToken = FUGLE_API_TOKEN, symbolId = '{}'.format(self.temp_share_no), output = 'raw')
            if share_data['canDayBuySell'] == True and share_data['canDaySellBuy'] == True:
                text = "菜雞調查後 😃，建議【{}】{}可進行當冲交易，但最終決定在您手中！😉".format(self.share_db[self.temp_share_no],self.temp_share_no)
            else:
                text = "菜雞調查後 😃，建議【{}】{}可不進行當冲交易，但最終決定在您手中！😉".format(self.share_db[self.temp_share_no],self.temp_share_no)
        else:
            text = "抱歉，菜雞不懂您 😥，無法得知您想瞭解的股票！請您重新輸入！"
            self.prev_action = "serv_buy_sell"
        self.out_msg = self.temp_msg = text
        success = self.send_message()
        return success

    def serv_candle_stick(self,keyword,msg_received):
        """
        To get the candle stick graph.
        """
        print('【serv_candle_stick】')

        # Check whether has share number in memory
        if self.temp_share_no:
            self.out_msg = "請稍後，菜雞在幫您取圖中，請不要怪我 ！😊"
            self.send_message()

            # Open Candle Stick Web to crop Picture
            driver = webdriver.Chrome()
            driver.get('https://s.yimg.com/nb/tw_stock_frontend/scripts/TaChart/tachart.a350178a.html?sid=' + str(self.temp_share_no))
            png = driver.get_screenshot_as_png()
            driver = driver.find_element_by_class_name('tafont')
            crop_location = driver.location
            crop_size = driver.size

            # Crop Picture
            img_candle_stick = Image.open(BytesIO(png))
            crop_size = {
                'top' : crop_location['y'] + 20,
                'bottom' : crop_location['y'] + crop_size['height'],
                'left' : crop_location['x'],
                'right' : crop_location['x'] + crop_size['width'] + 40
            }

            img_candle_stick = img_candle_stick.crop(
                (crop_size['left'],
                crop_size['top'], 
                crop_size['right'],
                crop_size['bottom'])
            )

            img_candle_stick.save('candle_stick.png')
            print('PHOTO HERE')
            # Send Picture
            self.out_msg = self.temp_msg = [img_candle_stick,'截圖 GET！這是【{}】{}之K綫圖。🎉'.format(self.share_db[self.temp_share_no],self.temp_share_no)]
        else:
            self.out_msg = self.temp_msg = "抱歉，菜雞不懂您 😥，無法得知您想瞭解的股票！請您重新輸入！"
            self.prev_action = "serv_candle_stick"
        success = self.send_message()
        return success

    def serv_top_share(self):
        """
        To get the best 5 sell and buy price by share number.
        """
        print('【serv_top_share】')  

        # Check whether has share number in memory
        if self.temp_share_no:
            share_data = intraday.quote(apiToken = FUGLE_API_TOKEN,symbolId = self.temp_share_no, output = 'raw')['order']
            
            # Creat Template For ask bid price
            text_ask = "您好 😁，菜雞偷了Fugle的最佳5檔機密，請參考！\n 最佳五檔（買價）：\n"
            text_bid = "您好 😁，菜雞偷了Fugle的最佳5檔機密，請參考！\n 最佳五檔（賣價）：\n"

            # Build Specific Text
            count = 1
            for ask,bid in zip(share_data['bestAsks'],share_data['bestBids']):
                temp_ask = '➡' + str(count)+'.價格: '+str(ask['price'])+' 交易張數：'+str(ask['unit'])+' 交易量：'+str(ask['volume']) + "\n " 
                temp_bid = '➡' + str(count)+'.價格: '+str(bid['price'])+' 交易張數：'+str(bid['unit'])+' 交易量：'+str(bid['volume']) + "\n " 
                text_ask = text_ask + "{}".format(temp_ask)
                text_bid = text_bid + "{}".format(temp_bid)
                count+=1
            # Send message by List    
            for send_content in [text_ask,text_bid]:
                self.out_msg = send_content
                success = self.send_message()

            # Save Temp Data
            self.temp_msg = [text_ask,text_bid]
        else:
            self.out_msg = self.temp_msg = "抱歉，菜雞不懂您 🙃，無法得知您想瞭解的股票！請您重新輸入！"
            self.prev_action = "serv_top_share"
            success = self.send_message()
        return success

    def serv_api_register(self,msg_received):
        """
        To register other bot API for sharing use.
        """
        print('【serv_api_register】')
        msg_received = msg_received.split(' ')
        api_owner,api_token = msg_received[1:]

        # Check exist list in db
        if api_owner in self.api_db.keys():
            self.api_db[api_owner] = api_token
            text = "您好，菜雞發現您已針對用戶進行注冊，爲了方便，菜雞已爲您更新 API 咯！🤣"
        else:
            self.api_db[api_owner] = api_token
            text = "好了，恭喜注冊成功 ! 🎉🎉🎉"
        self.out_msg = text
        success = self.send_message()
        return success        

    def serv_friend_list(self):
        """
        To list out the friend list.
        """
        print('【serv_friend_list】')

        # Check whether is empty
        if not bool(self.api_db):
            text = "好可憐哦，主人！您目前沒朋友！🤣"
        else:
            text = "👨‍💻 您的好友列別如下： \n"
            for name in self.api_db.keys():
                text = text + "✔ {} \n".format(name)
        self.out_msg = self.temp_msg = text
        success = self.send_message()
        return success

    def serv_forward_msg(self,keyword,msg_received):
        """
        To forward the importand news to other registered bot.
        """
        print('【serv_forward_msg】')
        # Check whether is empty
        if not bool(self.api_db):
            self.out_msg = self.temp_msg  = "好可憐哦，主人！您目前沒朋友！🤣"
            success = self.send_message()
        elif msg_received.split(keyword)[1] not in self.api_db.keys():
            self.out_msg = self.temp_msg = "抱歉查無此人！！！ 重新再來吧 🤣"
            success = self.send_message()
        else:
            to_api_token = self.api_db[msg_received.split(keyword)[1]]
            success = self.send_message(to_api_token)
            self.out_msg = self.temp_msg = "報告主人，菜雞已幫您完成轉達！😎"
            success = self.send_message()
        return success

    def serv_others(self,msg_received):
        """
        To response the word which not in the service list.
        """
        print('【serv_others】')
        self.out_msg = self.temp_msg = "{} <- 😒 是在，哈咯！？！".format(msg_received)
        success = self.send_message()
        return success

    def send_message(self,access_token=ACCESS_TOKEN):
        """
        To send out the message.
        """

        # Create a specific URL
        TELEGRAM_BASE = 'https://api.telegram.org/bot{}/'.format(access_token)
        api_msg_type = ['sendPhoto','sendMessage']
        get_type = str(type(self.out_msg)).split("'")[1]

        # Check the type of response message
        if get_type == 'str':
            res = requests.get(TELEGRAM_BASE + '{}?chat_id={}&text={}'.format(api_msg_type[1],self.chat_id,self.out_msg))
        if get_type == 'list':
            files = {'photo': open('candle_stick.png','rb')}
            data = {'chat_id': self.chat_id}
            res = requests.post(TELEGRAM_BASE + '{}'.format(api_msg_type[0]), files = files, data = data)
            res = requests.get(TELEGRAM_BASE + '{}?chat_id={}&text={}'.format(api_msg_type[1],self.chat_id,self.out_msg[1]))
        return True if res.status_code == 200 else False

    def import_share_no(self):
        """
        To import the industry list.
        """
        df = pd.read_csv('symbol_info.csv', encoding = 'big5')
        for industry,symbol_id in zip(df['industry'],df['symbol_id']):
            self.share_db[symbol_id] = industry

    @staticmethod
    def webhook_init(webhook_link):
        """
        To connect the ngrok service.
        """
        requests.get(webhook_link)
