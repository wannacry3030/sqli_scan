# UNION BASED / esse aplicação funciona da seguinte forma, ela vai tentar escrever uma aspa simples depois de um parametro de sql no url, (?id=1'), e vai nos dizer caso o url retorne um erro, geralmente (99%) quando o site retorna um erro de syntax, o sql é possivelmente injetavel...
import copy
from urllib import parse
import requests
import sys
#importando o modulo parse, para manipular url..

def request(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0","Cookie": "cf_clearance=a5.gOvCebw6NzWX3dNXqeLyBmWNZ7Yf18UlTM9gyTQ0-1674569703-0-150; PHPSESSID=t378jdas44hsgi2dt2mb8v8jf0; preferred_color_mode=dark; tz=America%2FSao_Paulo"}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        pass

def is_vulnerable(html):
    errors = ["mysql_fetch_array()","You have an error in your SQL syntax"]
    for error in errors:
        if error in html:
            return True

if __name__ == "__main__":
    url = sys.argv[1]
    url_parsed = parse.urlsplit(url)
    params = parse.parse_qs(url_parsed.query)
    for param in params.keys():
        query = copy.deepcopy(params)
        for c in "'\"":
            query[param][0] = c
            new_params = parse.urlencode(query, doseq=True)
            url_final = url_parsed._replace(query=new_params)
            url_final = url_final.geturl()
            response = requests.get(url_final)
            html = request(url_final)
            if html:
                if is_vulnerable(html):
                    print("vulneravel = {}".format(param))
                    quit()
                
print("nao vulneravel")