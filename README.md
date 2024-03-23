# 俄羅斯拼圖russian_puzzle程式語言破解說明

 - 可以先執行[觀賞每3秒變一次每0.5秒變一種擺法的.py程式](show.py)或是[在終端機輸入來顯示其中一種解法的其中一種擺放的.py程式](choose_num_show.py)
 - 然後可以看[example_video也就是看機器自己try跑的畫面](example_video.py)
 - 然後還有可以跑出solutions.txt的[C++的main](main.exe)還有[python的main](main.py)
 - 至於跑C++和Python的速度意外的是C++比較慢Python比較快，原因是因為我只有一個[main.cpp檔](main.cpp)然後C++又是編譯型語言，所以會有很大的負荷。
 - 跑出"find one solution"69415次就結束
 - 會出現各種類似"1 2/13"的東西(進度)，在最上面一層也就是0 38/38結束後就全部跑完了。
 - 至於[.json這個檔案就是information也就是所有來源](.json)來源於roger的影片
 - 使用C++17
 - 使用python3.12.1
 - 必須使用pygame(我使用pygame2.5.2)
 - [.py](.py)和[test.cpp](test.cpp)是拿來測試用的所以沒有東西

## 演算法說明

 - 先把1~13的積木的形狀輸入到程式碼裡。
 - 然後把目前的盤面掃描一遍
 - 檢查每個空格有沒有0，(也就是放不進去的)
 - 就到上一步，嘗試下一個拼法
 - 會先檢查每個空格的數字，找最小的也就是n
 - 然後把所有可以覆蓋這格空格的n種方法一一嘗試
 - 註: 其他通通不用嘗試，因為如果試了最小的格子一一搜索的話，就可以讓盤面全部被搜索
 - 如果此座標有n種覆蓋方法，以後也不會大於n
 - 所以只試最少的n種一路往下就可以了
 - 這種方法稱為**回溯法(Backtracking)**
 - 然後它是搜索到最深(13層)，然後到底了走回來也稱為**DFS(depth-first-search)**

## 使用須知
 - 要先在終端機輸入此命令
 - ```
   pip install -r requirements.txt
   ```

## 感言
 - 以上拼圖程式是受到roger啟發[roger影片](https://www.youtube.com/watch?v=jvPMyMe39fc)
 - 以上演算法和[資訊json也就是RGB和shape](.json)都從他那裡來
 - 以上程式碼除了語法支持，沒有任何問Chatgpt的部分
