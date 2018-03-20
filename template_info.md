# 源码自动生成模板 empty

### 概述

* 模板: empty
* 模板使用时间: 2018-03-18 18:59:01

### Docker
* Image: registry.cn-beijing.aliyuncs.com/rdc-template/repo
* Tag: 0817
* SHA256: 5556cb0b0d1605f84cca2b4118fe3d65e50314e905b66b8d926f4b1de90c432d

### 用户输入参数
* repoUrl: "git@code.aliyun.com:20891-lf/sfpt.git" 
* appName: "sfpt" 
* operator: "aliyun_605447" 
* appReleaseContent: "# 
* 请参考: 请参考 
* https://help.aliyun.com/document_detail/59293.html: https://help.aliyun.com/document_detail/59293.html 
* 了解更多关于release文件的编写方式: 了解更多关于release文件的编写方式 
* [NEWLINE][NEWLINE]#: [NEWLINE][NEWLINE]# 
* 构建源码语言类型[NEWLINE]code.language: scripts" 

### 上下文参数
* appName: sfpt
* operator: aliyun_605447
* gitUrl: git@code.aliyun.com:20891-lf/sfpt.git
* branch: master


### 命令行
	sudo docker run --rm -v `pwd`:/workspace -e repoUrl="git@code.aliyun.com:20891-lf/sfpt.git" -e appName="sfpt" -e operator="aliyun_605447" -e appReleaseContent="# 请参考 https://help.aliyun.com/document_detail/59293.html 了解更多关于release文件的编写方式 [NEWLINE][NEWLINE]# 构建源码语言类型[NEWLINE]code.language=scripts"  registry.cn-beijing.aliyuncs.com/rdc-template/repo:0817

