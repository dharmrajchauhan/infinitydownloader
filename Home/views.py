from django.shortcuts import render, HttpResponse
from Home.models import song
from django.contrib import messages
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# Create your views here.
def index(request):
    messages.success(request, "Hello, user i am happy for surfing my web")
    return render(request, 'index.html')


def about(request):
    return HttpResponse("This is aboutpage")


def songs(request):
    if request.method == "POST":
        songname = request.POST.get('song')
        songs = song(song=songname, )

        def musicdownload(list):
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
            # driver = webdriver.Chrome('F:/drivers/chromedriver.exe', options=chrome_options)
            driver = webdriver.Chrome('F:/drivers/chromedriver.exe')

            # -----------------------------------------------------------------------------------------------------------------------

            def google_link_searcher(new_string):
                global results
                query = new_string.strip() + ' wynk music'
                search_string = query.replace(' ', '+')
                webpage = driver.get("https://www.google.com/search?q=" + query + "&start=")
                try:
                    webpage = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'taw')))
                except TimeoutException:
                    print("googling spped is very low!")
                taw = driver.find_element_by_id("taw")
                if taw.size['width'] != 0:
                    suggestion = taw.text
                    if len(suggestion) > 1:
                        time.sleep(2)
                    try:
                        newlink = driver.find_element_by_xpath("//*[@id='taw']/div[2]/p/a").click()
                    except:
                        pass
                else:
                    time.sleep(2)
                    pass
                results = driver.find_elements_by_css_selector('div.g')
                print("result", len(results))
                return results

                # -----------------------------------------------------------------------------------------------------------------------

            links_bunch = []

            def link_extracter(results):
                # print("start but not get")
                for i in range(len(results)):
                    # print(results[i])
                    link = results[i].find_element_by_tag_name("a")
                    href = link.get_attribute("href")
                    try:
                        if href.startswith("https://wynk.in/"):
                            webresult = href
                            links_bunch.append(webresult + ",result" + str(i))
                    #                     print(webresult + ",result" + str(i))
                    except:
                        print("didn't get link")
                return links_bunch

            # -----------------------------------------------------------------------------------------------------------------------
            name_list = []

            def link_grabber(links_bunch):

                # print(links_bunch)
                wink_list = []
                pattern = r'.*,result0$'
                wink_rlink = (links_bunch[0])
                # print("wink list",wink_rlink.split(",")[0])
                wink_link = (wink_rlink.split(",")[0]).split("/")[5]
                wink_link = wink_link.replace('-', ' ')
                name_list.append(wink_link)
                # print("wink link",wink_link)
                print("name list", name_list)
                return name_list

            # -----------------------------------------------------------------------------------------------------------------------
            final_link_list = []

            def youtube_link(name_list):
                webpage = driver.get(f'https://www.youtube.com/results?search_query={name_list[0]}')
                try:
                    webpage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'contents')))
                except TimeoutException:
                    print("Youtube take tooo much time to load")
                wink_link = driver.find_element_by_id("video-title")
                # print(wink_link.text)
                wink_div = driver.find_element_by_xpath(
                    '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]//a[@href]')
                new_list = (wink_div.get_attribute("href"))
                final_link_list.append(new_list)
                # print("new_list11", new_list)
                print("final_link_list", final_link_list)
                return final_link_list

            def chrome_download(final_link_list):
                try:
                    driver.get('https://yt1s.com/youtube-to-mp3/en2')
                    try:
                        webpage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 's_input')))
                    except TimeoutException:
                        print("converter take too much time!")
                    search_input = driver.find_element_by_id("s_input").send_keys(final_link_list)
                    search_button = driver.find_element_by_class_name("btn-red").click()
                    time.sleep(10)
                    download = driver.find_element_by_id("asuccess").click()
                    print("download successful")
                except:
                    print("its not working")
                return

            google_link_searcher(list)
            time.sleep(2)
            link_extracter(results)
            time.sleep(2)
            link_grabber(links_bunch)
            time.sleep(2)
            youtube_link(name_list)
            time.sleep(2)
            chrome_download(final_link_list)
            time.sleep(5)
            driver.close()

        musicdownload(songname)
        songs.save()
        messages.success(request, "your download has been done vro")


    return render(request, 'songs.html')
