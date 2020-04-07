# SCU_FinTech_Telegram_Chatbot

- ### 作業目標
將 Fugle API 以及 Telegram Chatbot API 結合，建立輕量級之聊天機器人，人性化的與用戶進行金融市場資訊之交換，最終作爲投資用戶的資訊參考媒介。

- 作業工具
    - 程式語言：Python
    - 套件應用：Flask / Telegram / Request / JSON
    - API 應用：Fugle API / Telegram_bot API 

- Fugle API 資訊
    - GET/intraday/chart
    - GET/intraday/quote
    - GET/intraday/meta

- Turing API 資訊

- 功能構思（Fugle菜雞專家）

    聊天機器人説明：小傑是位投資新手，對於投資策略，看盤資訊一概不知。同時，在沒有額外金錢去訂閲財報之下，決定試試Fugle菜雞專家，期許在菜雞的帶領下能夠家財萬貫。

    - 輸入
    - 輸出
        - 【菜雞，菜雞】
            - 您好，菜雞非常高興能夠爲您服務。請輸入關鍵字以下關鍵字：
                - 【股票代碼】
                - 【適合買嗎？/ 適合賣嗎？】
                - 【給我圖表 / 給我蠟燭】
                - 【發給某某（全部）】
        - 【股票代碼】
            - 股票代碼
            - 股票名字
            - 日期
            - 時間
            - 開盤價
            - 收盤價
            - 最高價
            - 最低價
            - 交易張數
            - 交易量
        - 【適合買嗎？/ 適合賣嗎？】
            - 在用發出時判斷是否之前收到【股票代碼】之請求，若沒有則先進行股票代碼詢問。
            - 提取 meta API，若變數 canDayBuySell 為 True，則建議買入，反之。
            - 等待詢問：菜雞太笨，沒拿到股票代碼，請再輸入！！！
            - 成功輸出：菜雞調查後，建議【股票代碼】【股票名稱】可進行（結果），最終決定在您手中！
            - 失敗輸出：抱歉，菜雞設備不好，當機了。請您重新再操作！
        - 【給我圖表 / 給我蠟燭】
            - 利用 selenium 的自動化功能進行截圖，再進行推播。
            - 等待輸出：請稍後，菜雞在幫您取圖中，請不要怪我 ！
            - 成功輸出：截圖 GET！這是【股票代碼】【股票名稱】之K綫圖。
            - 失敗輸出：OOPS ！！！菜雞伺服器爛，請重新再來 ！
        - 【最佳五（5）檔】
            - 成功輸出：您好，菜雞偷了Fugle的最佳5檔機密，請參考！
            - 失敗輸出：看來菜雞是太嫩了，竟然無法獲取資訊，請重新嘗試！
        - 【注冊某某 API】
            - 在接受字串后進行切割，切割以空格及注冊為依據，將名字為設定為 key，API 為 value，以便好友清單的推播及共享。
            - Example：{ '偉傑' ：‘jdbasjnfobwrbf23orf9d02h3nq2idbni’}
            - 成功輸出：好了，恭喜注冊成功 !
            - 失敗輸出：抱歉，注冊失敗，在嘗試看看！
        - 【好友清單】
            - 好的，菜雞找到了你的好友列表：

                → A

                → B

                享受分享功能，找到你的生活樂趣 ^_^

        - 【發給某某（全部）】
            - 將最新一筆之互動資訊（不包括注冊 / 非關鍵字）進行共享。
            - 成功輸出：好的，菜雞已爲您將資訊分享給某某喲！
            - 失敗輸出：非常抱歉，您可能輸入錯誤好友資訊或好友不在列表中，請重新檢查！
        - 【非關鍵字】
            - 靠北！！！【非關鍵字】<<< 這火星文噢 ！
            - 【非關鍵字】<<<是在，哈咯！？！

- 函式架構
    - app.py
    - config.py
    - telegram_process.py

- 其他構思
    - Fugle菜鳥投資人

- 參考資料
    - [How To Create A Telegram Bot With Python](https://www.youtube.com/watch?v=GWH1XDXfAXQ)
    - [Python Telegram Bot 教學 (by 陳達仁)](https://hackmd.io/@BpUgvpG2TZy_PvDRF1bwvw/HkgaMUc24?type=view)
    - [實戰篇－打造人性化 Telegram Bot](https://medium.com/@zaoldyeck/%E5%AF%A6%E6%88%B0%E7%AF%87-%E6%89%93%E9%80%A0%E4%BA%BA%E6%80%A7%E5%8C%96-telegram-bot-ed9bb5b8a6d9)
    - [峰哥Telegram机器人系列教程](https://www.youtube.com/playlist?list=PL3dZh-p-vVofZ0BOQ4LnPlhJV3sVAQX8h)
    - [圖靈機器人](http://www.turingapi.com/)
    - [Telegram API](https://core.telegram.org/bots/api#sendphoto)
