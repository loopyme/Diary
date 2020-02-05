# Diary-Flask

自用的极简加密日志网站,基于`flask`和`loopyCryptor`,我用它来在手机上(或者其他有浏览器的设备上)便捷的记一些私人信息.

### 使用

用户在网页上输入密码登录,然后记下加密日志,就搞定了.

### 实现

大概是:
1. **登录**: 用户输入密码,密码不加验证,md5一次存到session里.后续每一步操作都需要验证,验证时取出md5一次的token,再md5一次,与保存的两重md5值(`Diary.views.TOKEN_2MD5`)比较并验证.
2. **写日志**:用户在网页上输入日志,服务器用预设的RSA公钥(`Diary/static/diary_key.pub`)加密,保存为`.diary`文件
3. **读日志**:服务器上可以不保存RSA私钥(`Diary/static/diary_key.pri`),用户要读日志的时候可以下载所有`.diary`文件,手动使用`read_diary.py`进行解密.

### Feature & Bug

1. 服务器只管存,不管读,加密存完以后就读不了了,需要下载后用私钥解密.
2. 服务器上可以不放RSA私钥,公钥就够了.
3. 凌晨4点以前的日志都算前一天的日志.
4. 浏览器的历史表单可能会记录下日志的原文,http传输也可能导致泄漏.

### Usage
去填上RSA公钥`Diary/static/diary_key.pub`,RSA私钥`Diary/static/diary_key.pri`,登录密码的两重md5值`Diary.views.TOKEN_2MD5`,就能跑起来了.

### DEMO

我自用的网站架在[这里](http://diary.loopy.tech),欢迎进行**除DDos以外的**任何测试和玩耍
