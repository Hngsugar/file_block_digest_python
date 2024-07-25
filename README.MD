# 企业微信微盘文件分块上传Python版本

## 说在前面

![image-20240725101314797](https://raw.githubusercontent.com/Hngsugar/Typora_Images/main/images/image-20240725101314797.png)

代码思路是源于https://github.com/knockkk/file_block_digest_nodejs.git里提供的将官方C++代码编译为wasm代码，并在node.js中正常运行的思路和代码。此python版本代码再写js文件和python文件实现通过python代码即可上传大文件，在实现的过程中还发现上传除了sha_cal_demo.txt以外的文件时最后一块上传不了，会报错640050，最后通过获取最后一块的实际字节大小，转换为base64编码，再进行分块上传请求，成功上传最后一块分块内容。此版本不仅是分块上传，通过下面的使用教程可以直接实现大文件上传。



部分代码技术参考链接：

[knockkk/file_block_digest_nodejs: 企业微信微盘文件分块上传Node.js版本 (github.com)](https://github.com/knockkk/file_block_digest_nodejs)

[wecomopen/file_block_digest (github.com)](https://github.com/wecomopen/file_block_digest)





## 如何使用

1.将项目拷贝；

2.根据代码文件注释，修改main.py文件中的变量：

+ access_token
+ space_id
+ father_id
+ filePath：这里设定的是upload_api_js/upload_file文件夹

3.运行main.py文件即可完成将upload_file下的文件上传到指定文件夹id为father_id的目录下。





## 运行效果

![image-20240725101031773](https://raw.githubusercontent.com/Hngsugar/Typora_Images/main/images/image-20240725101031773.png)





