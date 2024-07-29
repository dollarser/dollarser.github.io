---
title: JAVA学习路线
date: 2022-06-27 18:00:00
tags:
 - CS
 - JAVA
typora-root-url: ..
typora-copy-images-to: ..\img\javapath
---


# CodeSheep
参考视频：https://www.bilibili.com/video/BV1GQ4y1N7HD

相关思维导图：https://www.processon.com/view/link/5eb6a1b0e401fd16f4283225

## 编程基础（掌握）
### JAVA语法
#### Java基础

####  JVM
- 类加载机制
- 字节码执行机制
- JVM内存模型
- GC垃圾回收
- JVM性能监控与故障定位
- JVM调优

#### 多线程
- 并发编程的基础
- 线程池
- 锁
- 并发容器
- 原子类
- JUC并发工具类

<!--more-->


### 数据结构和算法

#### 数据结构
- 字符串
- 数组
- 链表
- 堆、栈、队列
- 二叉树
- 哈希
- 图

#### 算法
- 排序
- 查找
- 贪心
- 分治
- 动态规划
- 回溯

### 计算机网络

- ARP协议
- IP、ICMP协议
- TCP、UDP协议
- DNS、HTTP/HTTPS协议
- Session/Cookie

### MySQL数据库

- SQL语句的书写
- SQL语句的优化
- 事务、隔离级别
- 索引
- 锁

### 操作系统

- 进程、线程
- 并发、锁
- 内存管理和调度
- I/O原理

### 设计模式

- 单例
- 工厂
- 代理
- 策略
- 模板方法
- 观察者
- 适配器
- 责任链
- 建造者



## 研发工具
### 集成开发环境
- Eclipse
- Intellij IDEA
- VSCode

### Linux系统（了解）
- 常用命令
- Shell脚本### 项目管理/构建工具（掌握）
- Maven
- Gradle### 代码管理工具（了解）
- SVN
- Git


### 前端（了解）
- 基础套餐（大致了解，2-3天）
	- 三大件
		- HTML
		- JavaScript
		- CSS
	- 基础库
		- jQuery
		- Ajax
- 模板框架
	- JSP/JSTL（已过时）
	- Thymeleaf
	- FreeMarker
- 组件化框架
	- Vue
	- React
	- Angular
-----------------------------------------------

## 运维知识（配置）
- Web服务器
	- Nginx
- 应用服务器
	- Tomcat
	- Jetty
	- Undertow
- CDN加速
- 持续集成/持续部署
	- Jenkins
- 代码质量检查
	- sonar
- 日志收集和分析
	- ELK


-----------------------------------



## 成神之路

- 徒手撕源码
- 光脚造轮子
- 闭着眼睛深度调优
- 吊打面试官

-----------------------------------------------



## 平稳降落

调整心态、注意健康，飞的多高不重要，重要的是如何平望降落。





# 韩顺平版

参考视频：https://www.bilibili.com/video/BV14K4y177Qk

东西很多，慢慢学，学完前5个阶段就可以找工作

## 1、JAVA基础

+ 数据类型
+ 流程控制
  + 顺序结构
  + 分支结构
  + 循环结构
+ OOP
  + 封装
  + 继承
  + 多态
+ 数组
+ JavaAPI：学会查看文档
+ 异常和处理
+ 集合
+ 泛型
+ IO
+ 反射
+ 网络通信

## 2、Java高级

+ **Java多线程/高并发**
+ 并发基础
    + 互斥同步
    + 非阻塞同步
    + 指令墨棑
    + synchronized
    + volatile
  + 线程
  + 锁
    + 自旋锁
    + 偏向锁
    + 可重入锁
  + 线程锁
  + 并发容器
  + JUC
    + executor
    + collections
    + locks
    + atomic(原子类)
    + tools(CountDownLatch、Exchanger、ThreadLocal、CyclicBarrier)
+ **数据结构和算法**
+ 数据结构
  
  + 数组(稀疏数组)
    + 队列
    + 栈
    + 链表
    + 树
    + 散列表
    + 堆
    + 图
  
+ 算法
  
  + **排序(8种)**
+ 查找
    + 分治
+ **动态规划(背包问题)**
    + **回溯(骑士周游问题)**
+ **贪心算法**
    + KMP
+ Prim-普里姆最小生成树算法
    + Kruskal-克鲁斯卡尔最小生成树算法
+ Floyd-弗洛伊德最短路径算法
    + Dijkstra-迪杰斯特拉最短路径算法
+ 设计模式(23种)
    + 单例模式
    + 观察者模式
    + 工厂模式
    + 适配器模式
    + 装饰器模式
    + 代理模式
    + 模板模式
    + 职责链模式
    + 其他(组合模式，桥接模式，原型模式，...)
+ **JVM**
    + JVM体系
    + 类加载过程/机制
    + 双亲委派机制/沙箱安全机制
    + JMM(java内存模式)
    + 字节码执行过程/机制
    + GC(垃圾回收算法)
    + JVM性能监控和故障定位
    + JVM调优



## 3、JavaWEB

+ 前端基础
  + HTML
  + CSS
  + JavaScript
  + Ajax
  + Jquery
+ 前端框架（了解）
  + VUE
  + React
  + Angular
  + bootstrap
  + Node.js
+ Java web后端
  + Tomcat
  + Servlet
  + JSP



## 4、主流框架和项目管理

+ Linux(操作系统的使用，必学)

+ Nginx(做反向代理的WEB服务器)

+ **SSM**

  + Spring(轻量级的容器框架)
  + SpringMVC(分层的web开发框架)
  + MyBatis(持久层的框架)

+ 项目管理

  + Maven
  + Git、Github
  + *SVN*

+ **数据库**
  + MySQL
  + Redis
  + Oracle
+ 其他框架
  + WebService(即SOA)
  + Activiti(工作流框架。引擎)
  + Shiro(安全框架)
  + Spring Security(安全框架)
  + JPA(持久化)
  + SpringData(持久层的通用解决解决方案)



## 5、分布式 微服务 并行框架

+ **Netty**

  ​	初始了解：https://www.jianshu.com/p/b9f3f6a16911

+ Dubbo(RPC框架)

+ FastDFS(分布式文件系统)

+ Docker(应用容器引擎)

+ **Spring家族**
  + SpringBoot
  + SpringCloud(组件很多)
    + Nacos(阿里巴巴 服务发现、配置、管理)
    + Seata(阿里巴巴 分布式事务中间件)
    + Sentinel(阿里巴巴 流量控制 熔断 负载保护)
    + GateWay(网关、限流、日志、监控、鉴权)
    + OpenFeign(服务间调用)
  
+ 搜索引擎
  + ElasticSearch
  + Solr
  
+ **中间件**
  + MyCat(数据库，分库分表)

    了解参考：https://www.cnblogs.com/kingsonfu/p/10627802.html

  + 消息中间件
    + ActiveMQ
    + RabbitMQ
    + Kafka

+ 日志分析与监控(ELK)
  + ElasticSearch(搜索，存储数据)
  + LogStash(分析日志)
  + Kibana(可视化)
  
+ Zookeeper(一致性服务：配置维护、域名维护、分布式同步)



## 6、DevOps(开发运维一体化，自动化项目部署管理，CI/CD)

+ k8s(让部署容器化应用简单高效)
+ Prometheus(普罗米修斯：系统监控和报警)
+ Jenkins(监控持续的工作：部署、集成、交付)
+ Harbor(容器的镜像仓库)
+ GitLab
+ 项目工程代码质量检测(sonarqube)



## 7、大数据技术(了解)

+ Hadoop
+ Hive
+ Impals
+ spark
+ flink



## 8、项目：应用之前学的技术，做三个以上

+ 电商：https://github.com/macrozheng/mall
+ 金融：
+ 教育
+ 直播
+ CRM, ERP



## 9、大厂高频面试题

+ 上面加黑部分：主要包括JAVA高级、主流框架、项目



## 10、底层源码、内核研究



## 11、编程基础扩展

+ 计算机网络
+ 操作系统
+ 计算机组成原理
+ 编译原理
+ 离散数学
+ 数值分析
+ 汇编语言



