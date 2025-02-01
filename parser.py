from http.client import HTTPException, HTTPResponse
from urllib.error import URLError
from urllib.request import urlopen, Request
from html.parser import HTMLParser
import json, mimetypes, time


def get_http(url: str) -> str:
    url = url.encode('ascii', errors='ignore').decode('ascii')
    try:
        response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
        
    except HTTPException as e:
        print(e)
        return None
    
    data=response.read().decode('utf-8')
    
    return data

class SinonimOrgParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.dopush = None
        self.out = {}
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'a' and ('class', 'wordsL') in attrs:
            self.dopush = attrs[0][1]
        return super().handle_starttag(tag, attrs)
    def handle_endtag(self, tag: str) -> None:
        return super().handle_endtag(tag)
    def handle_data(self, data: str) -> None:
        if isinstance(self.dopush, str):
            self.out[data] = self.dopush
            self.dopush = None
        return super().handle_data(data)


start = time.perf_counter()
print(f'start')
data = get_http('https://sinonim.org/l/%D0%B0')
parse = SinonimOrgParser()
parse.feed(data)
with open('words.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(parse.out, indent=4, ensure_ascii=False))

print(f'end, {time.perf_counter() - start}, on 1 words: {(time.perf_counter() - start)/len(parse.out)}')
#with open('out.html', 'w', encoding='utf-8') as f:
#    f.write(data)

