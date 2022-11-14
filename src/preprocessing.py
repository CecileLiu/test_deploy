from bs4 import BeautifulSoup
import preprocessor as p
import re
from typing import Union, List, Dict


label_mapping = {"Y": 1, "N": 0, "N ": 0}


def full_to_half(sentence):  # 输入为一个句子
    change_sentence = ""
    for word in sentence:
        inside_code = ord(word)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        change_sentence += chr(inside_code)
    return change_sentence


def remove_tags(html):

    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(["style", "script"]):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return " ".join(soup.stripped_strings)


def preprocess(text) -> str:
    """Data cleaning

    Args:
        text (str): input text

    Returns:
        text (str): output 

    Notes:
        Option Name	Option Short Code
        URL	p.OPT.URL
        Mention	p.OPT.MENTION
        Hashtag	p.OPT.HASHTAG
        Reserved Words	p.OPT.RESERVED
        Emoji	p.OPT.EMOJI
        Smiley	p.OPT.SMILEY
        Number	p.OPT.NUMBER
    """
    p.set_options(p.OPT.RESERVED, p.OPT.URL, p.OPT.MENTION)

    # clean html
    text = remove_tags(text)

    # clean url, reserved, mentions
    p.clean(text)

    # remove special characters

    text.strip('[":.\n]+')
    clean = lambda s: re.sub(re.compile("// :|...全文"), ",", s)
    text = clean(text)
    # \u4e00-\u9fa5 for all unicode chinese char
    remove_sp_char = lambda s: full_to_half(
        re.sub("[^\s1234567890:：a-zA-Z，。,." + "\u4e00-\u9fa5]+", "", s)
    )
    text = remove_sp_char(text)

    return text
