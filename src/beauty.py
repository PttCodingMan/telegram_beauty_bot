import sys
import json
import traceback
import re
import random
import threading
from datetime import date, timedelta
import datetime
import time

from PyPtt import PTT

Woman = []
in_update = False

def get_pw():
    try:
        with open('account.txt') as AccountFile:
            account = json.load(AccountFile)
            id = account['ID']
            password = account['Password']
    except FileNotFoundError:
        print('Please note PTT ID and Password in account.txt')
        print('{"ID":"YourID", "Password":"YourPassword"}')
        sys.exit()

    return id, password


def update():
    global Woman
    global in_update

    in_update = True

    woman_temp = []

    ptt_id, ptt_pw = get_pw()

    ptt_bot = PTT.API(
        # LogLevel=PTT.LogLevel.TRACE,
        # LogLevel=PTT.LogLevel.DEBUG,
    )
    try:
        ptt_bot.login(
            ptt_id,
            ptt_pw,
            kick_other_login=True
        )
    except PTT.Exceptions.LoginError:
        ptt_bot.log('登入失敗')
        return

    crawl_list = [
        ('Beauty', PTT.data_type.post_search_type.PUSH, '50'),
    ]

    max_piture = 2000

    for (board, search_type, condition) in crawl_list:

        try:
            index = ptt_bot.get_newest_index(
                PTT.data_type.index_type.BBS,
                board,
                search_type=search_type,
                search_condition=condition,
            )
            # print(f'{board} 最新文章編號 {Index}')

            random_post_index = [i for i in range(index - 2000, index + 1)]

            random.shuffle(random_post_index)

            catch_pic = 0
            for index in random_post_index:

                # print(f'準備解析第 {IndexList.index(index) + 1} 篇 編號 {index} 已經蒐集 {Piture} 張圖片')

                post = ptt_bot.get_post(
                    board,
                    post_index=index,
                    search_type=search_type,
                    search_condition=condition
                )

                if post.delete_status != PTT.data_type.post_delete_status.NOT_DELETED:
                    continue

                # print(Post.getContent())

                content = post.content

                all_pic_id = re.findall(
                    r'https://(.+).jpg',
                    content
                )

                for album in all_pic_id:
                    pic_url = f'https://{album}.jpg'

                    if pic_url.startswith('https://imgur'):
                        pic_url = pic_url.replace('https://imgur', 'https://i.imgur')

                    if '[正妹]' in post.title or '[廣告]' in post.title:
                        if pic_url not in woman_temp:
                            woman_temp.append(pic_url)
                            catch_pic += 1
                            print(f'已抓取 {catch_pic} 張圖')

                    if catch_pic >= max_piture:
                        break
                if catch_pic >= max_piture:
                    break

                # https://imgur.com/ZAthTSl
                all_pic_id = re.findall(
                    r'https://imgur.com/(.+)',
                    content
                )

                for album in all_pic_id:
                    if '.' in album:
                        album = album[:album.find('.')]
                    if len(album) != 7:
                        continue

                    pic_url = f'https://i.imgur.com/{album}.jpg'

                    if '[正妹]' in post.title or '[廣告]' in post.title:
                        if pic_url not in woman_temp:
                            woman_temp.append(pic_url)
                            catch_pic += 1
                            # print(f'已抓取 {Piture} 張圖')

                    if catch_pic >= max_piture:
                        break

                if catch_pic >= max_piture:
                    break

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            break
        # print('=' * 50)

    ptt_bot.logout()

    Woman = woman_temp
    in_update = False
    print('更新完畢')
    # print(f'Woman length {len(Woman)}')


def timer():
    while True:
        update()

        now = datetime.datetime.now()
        tomorrow = date.today() - timedelta(-1)

        refresh_time = datetime.datetime(
            tomorrow.year,
            tomorrow.month,
            tomorrow.day,
            2,
            0,
            0)

        interval = refresh_time - now
        sec = interval.days * 24 * 3600 + interval.seconds

        print(interval)
        print(f'{sec} 秒後更新表特資料')
        time.sleep(sec)


def start(test_mode=False):
    t = threading.Thread(target=timer)
    t.daemon = True
    t.start()

    if test_mode:
        t.join()


temp_list = []


def pickup(n=1):
    global temp_list
    if len(temp_list) < n:
        global Woman
        temp_list = Woman.copy()

    result = random.sample(temp_list, n)
    # print(f'正妹剩下 {len(WomanTemplist)} 張還沒抽')

    return result


if __name__ == "__main__":
    # update()
    # print(pickup())

    start(test_mode=True)