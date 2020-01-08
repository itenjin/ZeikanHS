import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('http://www.customs.go.jp/searchsv/jitsv001.jsp')


#driver.find_element_by_css_selector("#itmdt").send_keys('20190415')
#日付以降

driver.find_element_by_css_selector("#itmnm").send_keys('いか')


Select(driver.find_element_by_css_selector("#itmct")).select_by_index(3)
#100件表示

driver.find_element_by_css_selector("#jit001btnarea > input:nth-child(1)").click()
#検索ボタンを押す


wait = WebDriverWait(driver, 10)
#指定したdriverに対して最大で10秒間待つように設定する


element = wait.until(EC.presence_of_element_located((By.ID, "jit001resarea")))
#指定された要素()がDOM上に現れるまで待機する

#件数出力
#print(driver.find_element_by_css_selector("#jit001resarea").text)
SchRslt = driver.find_element_by_css_selector("#jit001resarea").text

kenS = SchRslt.find("：")
kenE = SchRslt.find("件")

HitNum = int(SchRslt[kenS+1:kenE].strip())
print(HitNum)

WriteNum = 0
bigloop = HitNum // 100
modloop = HitNum % 100

#print (bigloop)

#bigloopが100で割り切れないならば＋1回
if modloop!=0:
    bigloop= bigloop +1

    
    
for j in range(bigloop):

    #最終(J = BIGLOOP)であれば
    if j == bigloop:
    
        smallloop = modloop
    else:
        smallloop = 102
        #100件
        
    for i in range(2,smallloop):

        #検索結果からリンクをたどる　最初は2
        driver.find_element_by_css_selector("#jit001restbl > tbody > tr:nth-child("+str(i)+") > td.col1 > a").click()

        #指定された要素()がDOM上に現れるまで待機する
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > table > caption")))
        # ソースをパースする
        url = driver.page_source
        soup=   BeautifulSoup(url, "html.parser")
        #print(soup.prettify())

        # セレクタ(タグ：table、id：jit001restbl)
        table = soup.findAll("table")[0]

        tds = table.findAll("td")
        # ファイルオープン
        csv_file = open('test2.csv', 'at', newline = '', encoding = 'utf-8')
        csv_write = csv.writer(csv_file)
        csv_data = []

        for td in tds:
        
        # 1行ごとにtd, tr要素のデータを取得してCSVに書き込み
            csv_data.append(td.get_text().strip())

        csv_write.writerow(csv_data)
        WriteNum = WriteNum + 1
        #jit001resarea
        
        # ファイルクローズ
        csv_file.close()

        driver.back()
    #下にスクロールさせる
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    if  j != bigloop:
    #次の100件をクリックする
        driver.find_element_by_css_selector("#contents > table > tbody > tr > td > div > form > div:nth-child(34) > table > tbody > tr > td.col4 > input[type=image]").click()
    else:
    
        pass

print (str(HitNum)+"件中"+str(WriteNum)+"件処理しました")
driver.quit()
    
                                    
