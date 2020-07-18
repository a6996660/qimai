from xiaomi import xiaomi
from huawei import huawei
from vivo import vivo
from oppo import oppo
from meizu import meizu
from yingyongbao import yingyongbao
from sanliuling import sanliuling
from wandoujia import wandoujia
from baidu import baidu
from pingguo import apple
if __name__ == '__main__':

   date='2020-07-12'  #设置日期

   xiaomi=xiaomi()
   xiaomi.shuchu(date)

   huawei=huawei()
   huawei.shuchu(date)

   vivo=vivo()
   vivo.shuchu(date)

   oppo=oppo()
   oppo.shuchu(date)

   meizu=meizu()
   meizu.shuchu(date)

   yingyongbao=yingyongbao()
   yingyongbao.shuchu(date)

   sanliuling=sanliuling()
   sanliuling.shuchu(date)

   wandoujia=wandoujia()
   wandoujia.shuchu(date)

   baidu=baidu()
   baidu.shuchu(date)

   apple=apple()
   apple.shuchu(date)