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


class CrawlBot:
    def __init__(
            self,
            account_file_name,
            board):
        self.account_file_name = account_file_name
        self.board = board

        self.ptt_id = None
        self.ptt_password = None

        self.Woman = None
        self.temp_list = []

    def get_pw(self):
        try:
            with open(self.account_file_name) as AccountFile:
                account = json.load(AccountFile)
                self.ptt_id = account['ID']
                self.ptt_password = account['Password']
        except FileNotFoundError:
            print(f'Please note PTT ID and Password in {self.account_file_name}')
            print('{"ID":"YourID", "Password":"YourPassword"}')
            sys.exit()

    def update(self):
        global Woman
        global in_update

        in_update = True

        woman_temp = []

        self.get_pw()

        ptt_bot = PTT.API(
            # LogLevel=PTT.LogLevel.TRACE,
            # LogLevel=PTT.LogLevel.DEBUG,
        )
        try:
            ptt_bot.login(
                self.ptt_id,
                self.ptt_password,
                kick_other_login=True
            )
        except PTT.exceptions.LoginError:
            ptt_bot.log('登入失敗')
            sys.exit()
        except PTT.exceptions.WrongIDorPassword:
            ptt_bot.log('帳號密碼錯誤')
            sys.exit()
        except PTT.exceptions.LoginTooOften:
            ptt_bot.log('請稍等一下再登入')
            sys.exit()

        crawl_list = [
            ('Beauty', PTT.data_type.post_search_type.PUSH, '50'),
        ]

        max_picture = 2000

        for (board, search_type, condition) in crawl_list:

            try:
                index = ptt_bot.get_newest_index(
                    PTT.data_type.index_type.BBS,
                    board,
                    search_type=search_type,
                    search_condition=condition,
                )
                # print(f'{board} 最新文章編號 {Index}')

                random_post_index = [i for i in range(index - max_picture, index + 1)]

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

                    if '[正妹]' not in post.title and '[廣告]' not in post.title:
                        continue

                    # print(Post.getContent())

                    content = post.content
                    content = content[:content.find('--')]
                    # print(content)

                    all_pic_id = re.findall(
                        r'https://(.+).jpg',
                        content
                    )

                    for album in all_pic_id:
                        pic_url = f'https://{album}.jpg'

                        if pic_url not in woman_temp:
                            woman_temp.append(pic_url)
                            catch_pic += 1

                        if catch_pic >= max_picture:
                            break
                    if catch_pic >= max_picture:
                        break

                    # print(f'已抓取 {catch_pic} 張圖')

            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print(e)
                break
            # print('=' * 50)

        ptt_bot.logout()

        self.Woman = woman_temp
        in_update = False

        print('更新完畢')
        # print(f'Woman length {len(Woman)}')

    def timer(self):
        while True:
            self.update()

            now = datetime.datetime.now()
            tomorrow = date.today() - timedelta(-1)

            refresh_time = datetime.datetime(
                tomorrow.year,
                tomorrow.month,
                tomorrow.day,
                6,
                0,
                0)

            interval = refresh_time - now
            sec = interval.days * 24 * 3600 + interval.seconds

            sec = int(sec + 1)

            print(interval)
            print(f'{sec} 秒後更新表特資料')
            time.sleep(sec)

    def start(self, test_mode=False):
        t = threading.Thread(target=self.timer)
        t.daemon = True
        t.start()

        if test_mode:
            t.join()

    def pickup(self, n=1):
        if len(self.temp_list) < n:
            self.temp_list = Woman.copy()

        result = random.sample(self.temp_list, n)
        # print(f'正妹剩下 {len(WomanTemplist)} 張還沒抽')

        return result


if __name__ == "__main__":
    pass
    # update()
    # print(pickup())

    # start(test_mode=True)
