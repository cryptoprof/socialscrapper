from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import json
import click
import os
selfProfile = "https://mbasic.facebook.com/profile.php?fref=pb"


def mfacebookToBasic(url):
    """Reformat a url to load mbasic facebook instead of regular facebook, return the same string if
    the url don't contains facebook"""

    if "m.facebook.com" in url:
        return url.replace("m.facebook.com", "mbasic.facebook.com")
    elif "www.facebook.com" in url:
        return url.replace("www.facebook.com", "mbasic.facebook.com")
    else:
        return url


class Person():
    """Basic class for people's profiles"""

    def __init__(self):
        self.name = ""
        self.profileLink = ""
        self.addLink = ""

    def __str__(self):
        s = ""
        s += self.name + ":\n"
        s += "Profile Link: " + self.profileLink
        if self.addLink != "":
            s += "Addlink ->: " + self.addLink
        return s

    def __repr__(self):
        self.__str__()


class Post():
    """Class to contain information about a post"""

    def __init__(self):
        self.posterName = ""
        self.text = ""
        self.numLikes = 0
        self.time = ""
        self.privacy = ""
        self.posterLink = ""
        self.linkToComment = ""
        self.linkToLike = ""
        self.linkToLikers = ""
        self.linkToReport = ""
        self.groupLink = ""
        self.linkToShare = ""
        self.linkToMore = ""
        self.numComents = 0

    def toDict(self):
        return self.__dict__.copy()

    def fromDict(self, d):
        self.__dict__ = d.copy()

    def from_json(self, j):
        self.fromDict(json.loads(j))

    def from_json_file(self, f):
        self.fromDict(json.loads(open(f, "rt").read()))

    def to_json(self):
        return json.dumps(self.toDict())

    def __str__(self):
        s = "\nPost by " + self.posterName + ": "
        s += self.text + "\n"
        s += "Likes: " + str(self.numLikes) + " - "
        s += "Comments: " + str(self.numComents) + " - "
        s += self.time + " "
        s += " - Privacy: " + self.privacy + "\n-"
        s += "\n Comment -> " + self.linkToComment + "\n"
        return s

    def __repr__(self):
        return self.__str__()


class FacebookBot(webdriver.Chrome):
    """Main class for browsing facebook"""

    def __init__(self, pathToWebdriver = os.getcwd()+'\\facebook_selenium_scrapper\\lib\\chromedriver.exe'):
        self.pathToWebdriver = pathToWebdriver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        webdriver.Chrome.__init__(self, executable_path=pathToWebdriver, chrome_options=options)

    def get(self, url):
        """The make the driver go to the url but reformat the url if is for facebook page"""
        super().get(mfacebookToBasic(url))

    def login(self, email, password):
        """Log to facebook using email (str) and password (str)"""

        url = "https://mbasic.facebook.com"
        self.get(url)
        email_element = self.find_element_by_name("email")
        email_element.send_keys(email)
        pass_element = self.find_element_by_name("pass")
        pass_element.send_keys(password)
        pass_element.send_keys(Keys.ENTER)
        if self.find_element_by_class_name("bi"):
            self.find_element_by_class_name("bp").click();
        try:
            self.find_element_by_name("xc_message")
            print("Logged in")
            return True
        except NoSuchElementException as e:
            print("Fail to login")
            return False

    def logout(self):
        """Log out from Facebook"""

        url = "https://mbasic.facebook.com/logout.php?h=AffSEUYT5RsM6bkY&t=1446949608&ref_component=mbasic_footer&ref_page=%2Fwap%2Fhome.php&refid=7"
        try:
            self.get(url)
            return True
        except Exception as e:
            print("Failed to log out ->\n", e)
            return False

    def postTextToURL(self, text, url):
        """Post text(str) to url (str), url can be a group, fan page or profile"""

        try:
            self.get(url)
            textbox = self.find_element_by_name("xc_message")
            textbox.send_keys(text)
            submit = self.find_element_by_name("view_post")
            submit.click()
            return True
        except Exception as e:
            print("Failed to post in ", url, "->\n", e)
            return False

    def postTextToTimeline(self, text):
        """Shortcut to post in your own timeline"""

        url = "https://mbasic.facebook.com/"
        return self.postTextToURL(text, url)

    def newMessageToFriend(
            self,
            friendname,
            message,
            image1=None,
            image2=None,
            image3=None):
        """Send message(str) to friend name (str), images doesn work in phantomjs"""

        url = "https://mbasic.facebook.com/friends/selector/?return_uri=%2Fmessages%2Fcompose%2F&cancel_uri=https%3A%2F%2Fm.facebook.com%2Fmessages%2F&friends_key=ids&context=select_friend_timeline&refid=11"
        self.get(url)
        q = self.find_element_by_name("query")
        q.send_keys(friendname)
        q.send_keys(Keys.ENTER)
        id = self.page_source.split(
            "/messages/compose/?ids=")[1].split('"><span>')[0].split('"><span>')[0]
        url = "https://mbasic.facebook.com/messages/compose/?ids=" + id
        self.get(url)
        t = self.find_element_by_name("body")
        t.send_keys(message)
        t.send_keys(Keys.ENTER)
        f1 = self.find_element_by_name("file1")
        f2 = self.find_element_by_name("file2")
        f3 = self.find_element_by_name("file3")
        if image1 is not None:
            f1.send_keys(image1)
        if image2 is not None:
            f2.send_keys(image2)
        if image3 is not None:
            f3.send_keys(image3)
        send = self.find_element_by_name("Send")
        send.send_keys(Keys.ENTER)
        return True

    def getPostInGroup(self, url, deep=2, moreText="Ver más publicaciones"):
        """Get a list of posts (list:Post) in group url(str) iterating deep(int) times in the group
        pass moreText depending of your language, i couldn't find a elegant solution for this"""

        self.get(url)
        ids = [4, 5, 6, 7, 9]
        posts = []
        for n in range(deep):
            #print("Searching, deep ",n)
            for i in ids:
                # print(i)
                post = Post()
                try:
                    p = self.find_element_by_id("u_0_" + str(i))
                    # print(p.text)
                    a = p.find_elements_by_tag_name("a")
                    post.posterName = a[1].text
                    try:
                        post.numLikes = int(a[3].text.split(" ")[0])
                    except ValueError:
                        post.numLikes = 0
                    post.text = p.find_element_by_tag_name("p").text
                    post.time = p.find_element_by_tag_name("abbr").text
                    # p.text.split("· ")[1].split("\n")[0]
                    post.privacy = self.title
                    post.posterLink = a[0].get_attribute('href')
                    # p.find_element_by_class_name("du").get_attribute('href')
                    post.linkToComment = a[2].get_attribute('href')
                    post.linkToLike = a[4].get_attribute('href')
                    try:
                        post.numComents = int(a[5].text.split(" ")[0])
                    except ValueError:
                        post.numComents = 0
                    # post.linkToShare = a[5].get_attribute('href')
                    post.linkToLikers = a[1].get_attribute('href')
                    post.linkToMore = a[6].get_attribute('href')
                    if post not in posts:
                        posts.append(post)
                except Exception:
                    continue
            try:
                more = self.find_element_by_partial_link_text(
                    moreText).get_attribute('href')
                self.get(more)
            # self.find_element_by_partial_link_text(moreText)
            except Exception as e:
                print(e)
                print(" Can't get more posts")
        return posts

    def postInGroup(self, groupURL, text):
        """Post text(str) in a group"""

        self.get(groupURL)
        try:
            tf = self.find_element_by_name("xc_message")
        except NoSuchElementException:
            print(" Group url doesn't exist or you don't have permissions to see it")
            return False
        tf.send_keys(text)
        self.find_element_by_name("view_post").send_keys(Keys.ENTER)
        return True

    def postImageInGroup(self, url, text, image1, image2="", image3=""):
        """Post image(str) in a group(url:str) with the text(str), doesn't work in phantomJS"""
        self.get(url)
        v = self.find_element_by_name("view_photo")
        v.send_keys(Keys.ENTER)
        self.save_screenshot("debug.jpg")
        i1 = self.find_element_by_name("file1")
        i2 = self.find_element_by_name("file2")
        i3 = self.find_element_by_name("file3")
        i1.send_keys(image1)
        i2.send_keys(image2)
        i3.send_keys(image3)
        filter = self.find_element_by_name("filter_type")
        filter.value_of_css_property(0)
        pre = self.find_element_by_name("add_photo_done")
        pre.click()
        m = self.find_element_by_name("xc_message")
        m.send_keys(text)
        vp = self.find_element_by_name("view_post")
        vp.click()
        return True

    def commentInPost(self, postUrl, text):
        """Comment a text(str) in a post(str)"""
        try:
            self.get(postUrl)
            tb = self.find_element_by_name("comment_text")
            tb.send_keys(text)
            tb.send_keys(Keys.ENTER)
            return self.getScrenshotName(
                "CommentingIn_" + self.title, screenshot, screenshotPath)
        except Exception as e:
            print("Can't comment in ", postUrl, "\n->", e)

    def getGroupMembers(self, url, deep=3, start=0):
        """Return a list of members of a group(url) as a list:Person iterat deep(int) times"""

        seeMembersUrl = url + "?view=members&amp;refid=18"
        groupId = url.split("groups/")[1]
        step = 28
        r = "https://mbasic.facebook.com/browse/group/members/?id=$GROUPID$&start=$n$"
        rg = r.replace("$GROUPID$", groupId)
        members = []
        for d in range(start, start + deep):
            url = rg.replace("$n$", str(d * 30))
            self.get(url)
            # print(self.current_url)
            p = self.find_elements_by_class_name("p")  # BK cada profile
            for b in p:
                person = Person()
                h3 = b.find_elements_by_tag_name("h3")
                person.name = h3[0].text
                person.profileLink = h3[0].find_element_by_tag_name(
                    "a").get_attribute('href')
                try:
                    person.addLink = b.find_elements_by_tag_name(
                        "a")[1].get_attribute('href')  # puede haber error
                except Exception:
                    # print("No Addlink")
                    pass
                members.append(person)
                # more = self.find_element_by_id("m_more_item").find_element_by_tag_name("a").get_attribute('href')
                # self.get(more)
                # print(more)
        # print(len(members))
        return members

    def sendFriendRequest(self, url):
        """Send a friend request to a profile(str)"""
        self.get(url)
        try:
            bz = self.find_element_by_class_name("bz")
            l = bz.get_attribute('href')
            self.get(l)
            return True
        except Exception:
            # print("Can't add friend")
            return False

    def messageToUrl(self, url, text):
        """Message a profile/fanpage (str) with text(str)"""

        self.get(url)
        name = self.title
        try:
            mb = self.find_elements_by_class_name("bx")
        except NoSuchElementException:
            print("Can't message to ", name)
            return False
        mm = None
        for m in mb:
            if "messages" in m.get_attribute('href'):
                mm = m.get_attribute('href')
                break
        self.get(mm)
        b = self.find_element_by_name("body")
        b.send_keys(text)
        self.find_element_by_name("Send").click()
        return True

    def getGroups(self):
        """
        Return a list of url of the groups your account belong to"""
        url = "https://m.facebook.com/groups/?seemore"
        # g = {"name": ("url", 0)}
        g = dict()
        self.get(url)
        br = self.find_elements_by_class_name("br")
        for b in br:
            try:
                notis = int(b.text[-2:])
                group_name = b.text[:-2]
            except ValueError:
                group_name = b.text
                notis = 0
            try:
                link = b.find_element_by_tag_name("a").get_attribute('href')
                g[group_name] = (mfacebookToBasic(link), notis)
            except Exception as e:
                print("Can't get group link")
        return g

    def getSuggestedGroups(self, sendrequest=False):
        """
        Return a list of suggested groups and optionally send a request to join"""

        url = "https://m.facebook.com/groups/"
        g = dict()
        self.get(url)
        bq = self.find_elements_by_class_name("bq")[-1]
        li = bq.find_elements_by_tag_name("li")
        for l in li:
            nombre = l.find_elements_by_tag_name(
                "td")[0].find_elements_by_tag_name("a")[0].text
            description = l.find_elements_by_tag_name(
                "td")[0].find_elements_by_class_name("bx")[0].text
            linkToGroup = l.find_elements_by_tag_name(
                "td")[0].find_element_by_tag_name("a").get_attribute('href')
            linkToRequest = l.find_elements_by_tag_name(
                "td")[-1].find_element_by_tag_name("a").get_attribute('href')
            g[nombre] = (description, linkToGroup, linkToRequest)
        if sendrequest:
            for r in g:
                try:
                    self.get(g[r][2])
                    print("Request to group: ", r)
                except Exception:
                    print("Fail to send request to: ", r)
        return g

    def getPostInProfile(self, profileURL, moreText="Mostrar",deep=2):
        """Return a list of Posts in a profile/fanpage , setup the "moreText" using your language, theres not elegant way to handle that"""
        posts_list = list()
        url = '{}?v=timeline'.format(profileURL)
        self.get(url)

        years_elements = self.find_elements_by_xpath("//div[@class='h']/a[contains(., '20')]")
        years = [y.text for y in years_elements]
        years.append('9999')  # append one dummy year for the extraction of the last year in the list
        i=0
        with click.progressbar(years, label='Scraping {} years'.format(len(years)), show_eta=False) as bar:
            for year in bar:

                more_button_exists = True
                while more_button_exists:
                    try:
                        articles = self.find_elements_by_xpath("//div[@role='article']")
                        for article in articles:
                            try:
                                #html вместо текста. грязные данные для последующей обработки
                                posts_list.append(str(article.get_attribute('outerHTML')))
                                print(str(article.get_attribute('outerHTML')))
                                #if iterator is equal deep, exit function return result
                                if (i == deep):
                                    return posts_list
                                i += 1
                                print(str(i) + '--' + str(deep))
                            except Exception as e:
                                print("ERROR: " + str(e))

                        # press more if more button exists
                        try:
                            show_more_link_element = self.find_element_by_partial_link_text(moreText)
                            show_more_link = show_more_link_element.get_attribute('href')
                            self.get(show_more_link)
                        except NoSuchElementException:
                            # if more button does not exist go to the next year
                            more_button_exists = False
                            if year is not '9999':
                                year_link_element = self.find_element_by_xpath("//div[@class='h']/a[text()='{}']".format(year))
                                year_link = year_link_element.get_attribute('href')
                                self.get(year_link)

                    except TimeoutError as e:
                        print("Timeout:", str(e))
                        time.sleep(1)
                    except BaseException as e:
                        print("ERROR:", str(e))

        return posts_list