from pandas import DataFrame
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import sys
import re
import os

def crawl(keyword, maxPage):
    # 크롬 웹브라우저 실행
    path = "./샘플"
    driver_path = "./chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    url_list = []
    count = 0
    if(not os.path.exists(path+"/"+keyword)):
        os.mkdir(path+"/"+keyword)

    for i in range(1, int(maxPage) + 1):  # 1~2페이지까지의 블로그 내용을 읽어옴
        url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo='+ str(i) + '&rangeType=ALL&orderBy=sim&keyword=' + keyword
        driver.get(url)
        time.sleep(0.5)
    
        for j in range(1, 8): # 각 블로그 주소 저장
            titles = driver.find_element_by_xpath('/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]')
            
            title = titles.get_attribute('href')
            url_list.append(title)
            #print(title)
    
    #print("url 수집 끝, 해당 url 데이터 크롤링")
    
    for url in tqdm(url_list, desc='샘플 수집중'): # 수집한 url 만큼 반복
        content_list = ""
        count = count + 1
        driver.get(url) 
        driver.switch_to.frame('mainFrame')
        #overlays_type = ".se-component.se-text.se-l-default" 
        overlays_type = "#post-view" + url.split('/')[4]
        contents = driver.find_elements_by_css_selector(overlays_type)
        title_overlays_type1 = ".se-fs-"
        title_overlays_type2 = ".pcol1"

        try:
            title = driver.find_element_by_css_selector(title_overlays_type1)
        except NoSuchElementException:
            title = driver.find_element_by_css_selector(title_overlays_type2)

        for content in contents:
            content_list = content_list + content.text # content_list 라는 값에 + 하면서 점점 누적
        title_str = path + "/" + keyword + "/" + "샘플 " + re.sub('[\/:*?"<>|]','',title.text) + '.txt'
        f = open(title_str, 'w', encoding='utf-8')
        f.write(content_list)
        f.close()

    print('크롤링 완료')
    
    driver.close()

def compare(keyword):
    okt = Okt()
    stop_words_list = set_stopwords() # 불용어 사전
    tokens_list = []
    test_files = load_files(keyword)
        
    for i in tqdm(range(0, len(test_files['inspect_files_list'])), desc='문서 토큰화'):
        stream_tokens = tokenizer(okt, test_files['inspect_files'][i], stop_words_list)
        tokens_list.append(stream_tokens)

    for i in tqdm(range(0, len(test_files['sample_files_list'])), desc='           '):
        stream_tokens = tokenizer(okt, test_files['sample_files'][i], stop_words_list)
        tokens_list.append(stream_tokens)
    
    tfidf_vectorizer = TfidfVectorizer(min_df=1)

    tfidf_matrix = tfidf_vectorizer.fit_transform(tokens_list)

    #similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
    similarities = tfidf_matrix * tfidf_matrix.T
    similarities_array = similarities.toarray()

    file_list = []
    for i in range(0,len(test_files['inspect_files_list'])):
        file_list.append(test_files['inspect_files_list'][i])
    for i in range(0,len(test_files['sample_files_list'])):
        file_list.append(test_files['sample_files_list'][i])
        
    for i in tqdm(range(0, len(similarities_array)), desc='분석 진행중'):
        for j in range(0, len(similarities_array[i])):
            similarities_array[i][j] = round(similarities_array[i][j], 3) * 100

    raw_data = {'파일/유사도': file_list}
    for i in tqdm(range(0, len(file_list)), desc='파일 생성중'):
        raw_data[file_list[i]] = similarities_array[i]
    df_data = DataFrame(raw_data)
    df_data.to_csv('./결과/'+keyword+'.csv', sep=',', na_rep='NaN', encoding='utf-8-sig')


def tokenizer(okt, stream, stop_words_list):
    stream_pos = okt.pos(stream)
    
    stream_tokens = ''
    for i in range(0, len(stream_pos)):
        if (stream_pos[i][1] == 'Noun' or stream_pos[i][1] == 'Verb' or stream_pos[i][1] == 'Adjective') and stream_pos[i][0] not in stop_words_list and len(stream_pos[i][0]) > 1:
            stream_tokens += stream_pos[i][0] + ' '
    
    #stream_tokens = [ i[0] for i in stream_pos if (i[1] == 'Noun' or i[1] == 'Verb' or i[1] == 'Adjective') and i[0] not in stop_words_list and len(i[0]) > 1]
    return stream_tokens

def set_stopwords():
    stop_words_list = []
    stopwords = open('stopwords.txt', 'r', encoding = 'utf-8')
    for line in stopwords.readlines():
       stop_words_list.append(line.rstrip())
    stopwords.close()
    return stop_words_list

def load_files(keyword):
    inspect_files_list = os.listdir('./검수/' + keyword)
    sample_files_list = os.listdir('./샘플/' + keyword)
    test_files = { 'sample_files': [], 'inspect_files': [], 'sample_files_list': sample_files_list, 'inspect_files_list': inspect_files_list }

    for i in range(0, len(inspect_files_list)): 
        fd = open('./검수/' + keyword + '/' + inspect_files_list[i], 'r', encoding = 'utf-8')
        stream = fd.read().replace('\n', ' ')
        test_files['inspect_files'].append(stream)
        fd.close()

    for i in range(0, len(sample_files_list)): 
        fd = open('./샘플/' + keyword + '/' + sample_files_list[i], 'r', encoding = 'utf-8')
        stream = fd.read().replace('\n', ' ')
        test_files['sample_files'].append(stream)
        fd.close()

    return test_files

def main():
    keyword = sys.argv[1]
    pages = sys.argv[2]
    crawl(keyword, pages)
    compare(keyword)
    input("종료하시려면 아무 키를 눌러주세요.")

if __name__ == '__main__' :
    main()