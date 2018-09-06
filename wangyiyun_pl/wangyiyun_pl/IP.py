import random
'''从自己创建的免费ip池取出ip，生成代理'''
def get_IP():
    with open(r'D:\gerapy\projects\wangyiyun_pl\wangyiyun_pl\ip.txt', 'r') as f:
        ip_list = f.readlines()
        ip = random.choice(ip_list)
        ip_text = ip.split(':')
        if ip_text[0] == 'http':
            proxie = 'http://{0}:{1}'.format(ip_text[1].strip(), ip_text[2].strip())
        elif ip_text[0] == 'https':
            proxie = 'https://{0}:{1}'.format(ip_text[1].strip(), ip_text[2].strip())
        else:
            proxie = 'http://{0}:{1}'.format(ip_text[1].strip(), ip_text[2].strip())
    return proxie