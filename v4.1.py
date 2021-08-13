#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/8/9 17:02
# @Author: Bolvar Fordragon
# @File  : v4.1.py
import time, os, json
from v0 import preparation, loadDataFromJson, equal_distribution_list
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing.dummy import Pool


def scrapy_pages_amazon(asin_list):
    # 初始化浏览器
    DRIVERNAME = 'Chrome'
    print('浏览器选用：%s' % DRIVERNAME)
    if DRIVERNAME.lower() == 'chrome':
        # 打开ChromeDriver
        driver = webdriver.Chrome('D:/WebDriver/bin/chromedriver.exe')
        # Chrome打开会有设置标签，影响后续操作，拿伊组忒
        windows = driver.window_handles  # 获取所有标签页
        driver.switch_to.window(windows[0])  # 跳转到第0个标签页即设置标签
        driver.close()  # 把设置标签关掉
        driver.switch_to.window(windows[-1])  # 回到需要操作的标签
    else:
        # 设置别的浏览器
        driver = webdriver.Chrome('D:/WebDriver/bin/chromedriver.exe')
        driver.quit()
        pass
    driver.maximize_window()
    driver.get('https://www.amazon.com/?currency=USD&language=en_US')
    time.sleep(2)
    driver.refresh()  # 刷新规避cookies
    time.sleep(15)  # 空等规避登录提示

    for asin_code in asin_list:
        repeat_count = 0
        item_url = 'https://www.amazon.com/dp/{}?currency=USD&language=en_US'.format(asin_code)
        item_dict = {"Product ID": asin_code,
                     "Product Principal Screenshot": {"Link": '%s_PS.png' % asin_code,
                                                      "Timestamp": ''},
                     "Category": '',
                     "details": [],
                     # "Product details": {"Link": '%s_PD.png' % asin_code,"Timestamp": '',"Details": '', },
                     # "Product Description": {"Link": '%s_PP.png' % asin_code,"Timestamp": '',"Description": '', },
                     "Historical QAs": [],
                     "Reviews": []}
        driver.get(item_url)  # 访问商品链接
        time.sleep(2)
        # driver.refresh()     # 刷新规避cookies
        # time.sleep(5)
        if driver.title == 'Page Not Found':
            fno.write('%s\n' % asin_code)
            fno.flush()
        else:
            fok.write('%s\n' % asin_code)
            fok.flush()
            while True:
                if repeat_count >= 2:
                    print(asin_code)
                    break
                try:
                    driver.find_element_by_xpath('//*[@id="ppd"]')
                    break
                except:
                    time.sleep(30)
                    driver.get(item_url)  # 访问商品链接
                    time.sleep(5)
                    repeat_count += 1
            driver.execute_script("document.body.style.zoom='0.75'")
            pic_name = '主体信息'
            try:
                pic_shot = driver.find_element_by_xpath('//*[@id="ppd"]').screenshot(
                    File_Path_product_principal_screenshot + item_dict["Product Principal Screenshot"]["Link"])
                item_dict["Product Principal Screenshot"][
                    "Timestamp"] = time.time()  # time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：')
                # print("%s：截图成功！" % pic_name)
            except Exception as e:
                efp.write('%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, e))
                efp.flush()
                # print("%s-%s截图失败：%s" % (asin_code, pic_name, pic_msg))
                continue

            try:
                item_dict['Category'] = driver.find_element_by_xpath(
                    '//*[@id="wayfinding-breadcrumbs_feature_div"]/ul').text.strip()
            except Exception as e:
                item_dict['Category'] = ''
                efc.write('%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, e))
                efc.flush()

            details_pics = driver.find_elements_by_xpath('//*[@id="dp-container"]/div')
            for details_pics_i in range(len(details_pics)):
                try:
                    details_pics[details_pics_i].screenshot(File_Path_product_details + '%s_%s.png' % (asin_code, details_pics_i))
                    item_dict["details"].append(details_pics[details_pics_i].get_property('attributes')[0])
                except Exception as e:
                    efd.write('%s\t%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, details_pics_i, e))
                    efd.flush()
                    # print('详情截图 Error%s,%s,%s' % (asin_code, details_pics_i, e))
            '''
            pic_name = '产品描述1'
            try:
                pic_shot = driver.find_element_by_xpath('//*[@id="descriptionAndDetails"]').screenshot(File_Path_product_details + item_dict["Product details"]['Link'])
                item_dict["Product details"]["Timestamp"] = time.time()#time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：')
                #print("%s：截图成功！" % pic_name)
            except Exception as pic_msg:
                print("%s-%s截图失败：%s" % (asin_code, pic_name, pic_msg))
    
            pic_name = '产品描述2'
            try:
                pic_shot = driver.find_element_by_xpath('//*[@id="prodDetails"]').screenshot(File_Path_product_details + item_dict["Product Description"]['Link'])
                item_dict["Product Description"]["Timestamp"] = time.time()#time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：')
                #print("%s：截图成功！" % pic_name)
            except Exception as pic_msg:
                print("%s-%s截图失败：%s" % (asin_code, pic_name, pic_msg))
    
            try:
                item_dict["Product Description"]["Description"] = driver.find_element_by_xpath('//*[@id="productDescription"]').text
                #productDetails_feature_div
            except:
                pass
            try:
                item_dict["Product details"]["Details"] = driver.find_element_by_xpath('//*[@id="detailBullets_feature_div"]').text
            except:
                pass
            '''
            '''
            {"Question": "Does this work on Kindle fire hd?",
            "Post time": "May 1, 2020",
            "Vote": 1,
            "Answers": [{"Text": "No unfortunately it does not work on Kindle Fire.",
                         "Helpful": (0, 0),
                         "Post time": "July 20, 2020"}]}
            '''
            q_href_list = []  # 本来想用dict但是怕重复问题
            qa_url = 'https://www.amazon.com/ask/questions/asin/{}/1?currency=USD&language=en_US'.format(asin_code)
            driver.get(qa_url)
            time.sleep(2)
            # 获取当页所有Q和Q的href
            qas = driver.find_elements_by_xpath('//*[@id="a-page"]/div[1]/div[6]/div/div/div')
            for qa in qas:
                q = qa.find_element_by_xpath('div/div[2]/div[1]/div/div[2]/a/span').text.strip()
                v = qa.find_element_by_xpath('div/div[1]/ul/li[2]/span[1]').text.strip()
                a_url = qa.find_element_by_xpath('div/div[2]/div[1]/div/div[2]/a').get_attribute('href')
                q_href_list.append([q, v, a_url])
            while True:
                try:
                    driver.find_element_by_xpath('//*[@id="askPaginationBar"]/ul/li[last()]/a').click()  # 翻页
                    time.sleep(2)
                    qas = driver.find_elements_by_xpath('//*[@id="a-page"]/div[1]/div[6]/div/div/div')
                    for qa in qas:
                        q = qa.find_element_by_xpath('div/div[2]/div[1]/div/div[2]/a/span').text
                        v = qa.find_element_by_xpath('div/div[1]/ul/li[2]/span[1]').text.strip()
                        a_url = qa.find_element_by_xpath('div/div[2]/div[1]/div/div[2]/a').get_attribute('href')
                        q_href_list.append([q, v, a_url])
                        # print('Q:%s' % q)
                        # print('HREF:%s' % a_url)
                    break
                except Exception as e:
                    # print(driver.current_url, len(qas), len(q_href_list), e)
                    efq.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, driver.current_url, len(qas), len(q_href_list), e))
                    efq.flush()
                    break

            for question, v, a_url in q_href_list:
                driver.get(a_url)
                time.sleep(2)
                try:
                    q_p_d = driver.find_element_by_xpath('//*[@id="a-page"]/div[1]/div[1]/div[2]/p[2]').text.strip()
                except:
                    while True:
                        driver.get(a_url)
                        time.sleep(2)
                        try:
                            q_p_d = driver.find_element_by_xpath('//*[@id="a-page"]/div[1]/div[1]/div[2]/p[2]').text.strip()
                            break
                        except:
                            pass
                answer_list = []
                answers = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/div')
                for answer in answers:
                    # 需要A、A的信息、A的helpful
                    ans_text = answer.find_element_by_xpath('span').text.strip()
                    ans_date = answer.find_element_by_xpath('div[1]/span').text.strip().strip('· ')
                    ans_help = answer.find_element_by_xpath(
                        'div[2]/span[1]').text.strip()  # 1 of 1 found this helpful. Do you?   #Do you find this helpful?
                    if 'found' in ans_help:
                        ans_help = ans_help.split(' found this helpful')[0]
                    else:
                        ans_help = '0 of 0'
                    ans_dict = {"Text": ans_text, "Helpful": ans_help, "Post time": ans_date}
                    # print(ans_dict)
                    answer_list.append(ans_dict)
                    # qa_list.append([question, ans_text, ans_date, ans_help])
                # print(answer_list)

                item_dict["Historical QAs"].append({"Question": question,
                                                    'Post time': q_p_d,
                                                    'Vote': v,
                                                    'Answers': answer_list
                                                    }
                                                   )
                # item_dict["Historical QAs"]['Answers'] = answer_list

            '''
            {"RID": '',
             "Link": ASIN_RID.png,
             "Timestamp": '',
             "Title": "Worked Perfectly",
             "Rating": (5, 5),
             "Post time": "May 5, 2020",
             "ISVerifiedPurchase": 1,
             "Content": "",
             "Helpful": 15,
             "Product related": {"Platform": "PC/Mac Online Code",
                                 "Edition": "18 Months, 2 Devices"}}
            '''
            review_url = 'https://www.amazon.com/product-reviews/{}?currency=USD&language=en_US'.format(asin_code)
            driver.get(review_url)
            review_id = 0
            time.sleep(2)
            driver.refresh()
            time.sleep(7)
            reviews_driver = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div')
            if len(reviews_driver) > 10:
                reviews_driver = reviews_driver[:-1]
            soup = BeautifulSoup(driver.page_source, 'lxml')
            reviews_soup = soup.find('div', id='cm_cr-review_list').find_all('div', class_='a-section review aok-relative')
            if len(reviews_driver) > len(reviews_soup):
                reviews_driver = reviews_driver[1:]
                if len(reviews_driver) != len(reviews_soup):
                    print('%s Review Error:【%s：%s：%s】' % (asin_code, review_id, len(reviews_driver), len(reviews_soup)))
                    print(driver.current_url)
                    continue
            for i in range(min(len(reviews_driver), len(reviews_soup))):
                item_dict["Reviews"].append({"RID": review_id,
                                             # "Link": '%s_%s.png' % (asin_code, review_id),
                                             # links :[]
                                             "Timestamp": time.time(),
                                             "Title": "",
                                             "Rating": '',
                                             "Post time": "",
                                             "ISVerifiedPurchase": '',
                                             "Content": "",
                                             "Helpful": '',
                                             "Product related": ''})
                '''
                pic_name = '评论信息'
                try:
                    pic_shot = reviews_driver[i].screenshot(File_Path_reviews + item_dict["Reviews"][review_id]["Link"])
                    item_dict["Reviews"][review_id]["Timestamp"] = time.time()#time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：')
                    # print("%s：截图成功！" % pic_name)
                except Exception as pic_msg:
                    print("%s%s截图失败：%s" % (asin_code, pic_name, pic_msg))
                '''
                item_dict["Reviews"][review_id]['Title'] = reviews_driver[i].find_element_by_xpath(
                    'div/div/div[2]/a[2]/span').text.strip()
                item_dict["Reviews"][review_id]['Rating'] = reviews_soup[i].find('a', class_='a-link-normal').text.strip()
                # comment_rating = comments_driver[i].find_element_by_xpath('div/div/div[2]/a[1]').text.strip()
                item_dict["Reviews"][review_id]["Post time"] = reviews_driver[i].find_element_by_xpath(
                    'div/div/span').text.strip()
                try:
                    comment_Veri = reviews_driver[i].find_element_by_xpath('div/div/div[3]/span/a/span').text.strip()
                    if 'Verified' in comment_Veri:
                        item_dict["Reviews"][review_id]["ISVerifiedPurchase"] = 1
                    else:
                        item_dict["Reviews"][review_id]["ISVerifiedPurchase"] = 0
                except:
                    item_dict["Reviews"][review_id]["ISVerifiedPurchase"] = 0

                item_dict["Reviews"][review_id]["Content"] = reviews_driver[i].find_element_by_xpath(
                    'div/div/div[4]/span/span').text.strip()
                try:
                    item_dict["Reviews"][review_id]["Helpful"] = reviews_driver[i].find_element_by_xpath(
                        'div/div/div[5]/div/span[1]/div[1]/span').text.strip()
                except:
                    item_dict["Reviews"][review_id]["Helpful"] = 0

                try:
                    item_dict["Reviews"][review_id]["Link"] = [p.find_element_by_xpath('a/img').get_attribute('src') for p
                                                               in reviews_driver[i].find_elements_by_xpath(
                            'div/div/div[6]/div/span')]
                except:
                    item_dict["Reviews"][review_id]["Link"] = ''

                review_id += 1
            while True:
                try:
                    next_ = driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
                    time.sleep(2)
                    driver.refresh()
                    time.sleep(7)
                    reviews_driver = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div')
                    if len(reviews_driver) > 10:
                        reviews_driver = reviews_driver[:-1]
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    reviews_soup = soup.find('div', id='cm_cr-review_list').find_all('div', class_='a-section review aok-relative')
                    if len(reviews_driver) > len(reviews_soup):
                        reviews_driver = reviews_driver[1:]
                        if len(reviews_driver) != len(reviews_soup):
                            print('%s Review Error:【%s：%s：%s】' % (
                            asin_code, review_id, len(reviews_driver), len(reviews_soup)))
                            print(driver.current_url)
                            continue
                    for i in range(min(len(reviews_driver), len(reviews_soup))):
                        item_dict["Reviews"].append({"RID": review_id,
                                                     # "Link": '%s_%s.png' % (asin_code, review_id),
                                                     "Timestamp": time.time(),
                                                     "Title": "",
                                                     "Rating": '',
                                                     "Post time": "",
                                                     "ISVerifiedPurchase": '',
                                                     "Content": "",
                                                     "Helpful": '',
                                                     "Product related": ''})

                        '''
                        pic_name = '评论信息'
                        try:
                            pic_shot = reviews_driver[i].screenshot(File_Path_reviews + item_dict["Reviews"][review_id]["Link"])
                            item_dict["Reviews"][review_id]["Timestamp"] = time.time()#time.strftime('%Y-%m-%d %H{}%M{}%S',time.localtime(time.time())).format('：', '：')
                            # print("%s：截图成功！" % pic_name)
                        except Exception as pic_msg:
                            print("%s%s截图失败：%s" % (asin_code, pic_name, pic_msg))
                        '''
                        item_dict["Reviews"][review_id]['Title'] = reviews_driver[i].find_element_by_xpath(
                            'div/div/div[2]/a[2]/span').text.strip()
                        item_dict["Reviews"][review_id]['Rating'] = reviews_soup[i].find('a',
                                                                                         class_='a-link-normal').text.strip()
                        # comment_rating = comments_driver[i].find_element_by_xpath('div/div/div[2]/a[1]').text.strip()
                        item_dict["Reviews"][review_id]["Post time"] = reviews_driver[i].find_element_by_xpath(
                            'div/div/span').text.strip()
                        try:
                            comment_Veri = reviews_driver[i].find_element_by_xpath(
                                'div/div/div[3]/span/a/span').text.strip()
                            if 'Verified' in comment_Veri:
                                item_dict["Reviews"][review_id]["ISVerifiedPurchase"] = 1
                            else:
                                item_dict["Reviews"][review_id]["ISVerifiedPurchase"] = 0
                        except:
                            item_dict["Reviews"]["ISVerifiedPurchase"] = 0

                        item_dict["Reviews"][review_id]["Content"] = reviews_driver[i].find_element_by_xpath(
                            'div/div/div[4]/span/span').text.strip()
                        try:
                            item_dict["Reviews"][review_id]["Helpful"] = reviews_driver[i].find_element_by_xpath(
                                'div/div/div[5]/div/span[1]/div[1]/span').text.strip()
                        except:
                            item_dict["Reviews"][review_id]["Helpful"] = 0

                        try:
                            item_dict["Reviews"][review_id]["Link"] = [p.find_element_by_xpath('a/img').get_attribute('src')
                                                                       for p in reviews_driver[i].find_elements_by_xpath(
                                    'div/div/div[6]/div/span')]
                        except:
                            item_dict["Reviews"][review_id]["Link"] = ''

                        review_id += 1
                except:
                    break
                if review_id >= 20:
                    break
            # results.append(item_dict)
            # for result in results:
            # f.write(json.dumps(result) + '\n')
            ofj.write(json.dumps(item_dict) + '\n')
            ofj.flush()
            ofd.write('%s:%s' % (asin_code, str(item_dict)))
            ofd.flush()
            # break
    driver.quit()


if __name__ == '__main__':
    start_time, File_Path, File_Path_product_principal_screenshot, File_Path_product_details, File_Path_reviews = preparation()
    asin_list = loadDataFromJson()[:60]
    pcn = 3
    list_list = equal_distribution_list(asin_list, pcn)
    efp = open('%serrorlog_principal_screenshot%s.txt' % (File_Path, start_time), 'w')
    #efp.write('%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, e))
    efc = open('%serrorlog_Category%s.txt' % (File_Path, start_time), 'w')
    #efc.write('%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, e))
    efd = open('%serrorlog_detail%s.txt' % (File_Path, start_time), 'w')
    #efd.write('%s\t%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, details_pics_i, e))
    efq = open('%serrorlog_qa%s.txt' % (File_Path, start_time), 'w')
    #efq.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：'), asin_code, driver.current_url, len(qas), len(q_href_list), e))
    ofj = open('%samazonMultiqa%s.jsonl' % (File_Path, start_time), 'w')
    ofd = open('%samazonMultiqa%s.txt' % (File_Path, start_time), 'w')
    ofd.write('{')
    fok = open('asin.txt', 'w')
    fno = open('asin_stop.txt', 'w')
    #ofj.write(json.dumps(item_dict) + '\n')
    #ofj.flush()
    pool = Pool(pcn)
    result = pool.map(scrapy_pages_amazon, list_list)
    efp.close()
    efc.close()
    efd.close()
    efq.close()
    ofj.close()
    ofd.close()

