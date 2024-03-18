---
title: Mybatis
date: 2022-06-07 18:00:00
tags:
 - CS
 - Mybatis
 - JAVA
typora-root-url: ..
typora-copy-images-to: ..\img\java\mybatis
---

**环境：**

+ JDK1.8

+ Mysql 5.7

+ maven 3.6.1

+ IDEA

**回顾：**

+ JDBC

+ Mysql

+ Java基础

+ Maven

+ Junit：单元测试



## 1. 简介

### 1.1 什么是Mybatis

MyBatis 是一款优秀的持久层框架，它支持自定义 SQL、存储过程以及高级映射。MyBatis 免除了几乎所有的 JDBC 代码以及设置参数和获取结果集的工作。MyBatis 可以通过简单的 **XML** 或注解来配置和映射原始类型、接口和 Java POJO（Plain Old Java Objects，普通老式 Java 对象）为数据库中的记录。

框架：配置文件最好直接看官网

MyBatis官方文档：https://mybatis.org/mybatis-3/zh/index.html

GitHub主页：https://github.com/mybatis/mybatis-3

Maven地址：https://mvnrepository.com/artifact/org.mybatis/mybatis

```xml
<!-- https://mvnrepository.com/artifact/org.mybatis/mybatis -->
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.6</version>
</dependency>
```



### 1.2 持久化

数据持久化

+ 持久化就是将程序的数据在持久状态和顺势状态转化的过程
+ 内存：断电即失
+ 数据库(JDBC)，文件IO持久化

为什么需要持久化

+ 有一些对象，不能让他丢掉
+ 内存价格昂贵



### 1.3 持久层

Dao层(data access object)：数据访问层、Service层、Controller层...

+ 完成持久化工作的代码块
+ 界限十分明显



### 1.4 为什么需要Mybatis

+ 帮助程序员将数据存入数据库

+ 传统的JDBC代码太复杂。方便、简化框架、自动化

+ 不用Mybatis也可以，但是Mybatis更容易上手。**技术没有高低之分**

+ 优点：

  + 简单易学：本身就很小且简单。没有任何第三方依赖，最简单安装只要两个jar文件+配置几个sql映射文件易于学习，易于使用，通过文档和源代码，可以比较完全的掌握它的设计思路和实现。
  + 灵活：mybatis不会对应用程序或者数据库的现有设计强加任何影响。 sql写在xml里，便于统一管理和优化。通过sql语句可以满足操作数据库的所有需求。
  + 解除sql与程序代码的耦合：通过提供DAO层，将业务逻辑和数据访问逻辑分离，使系统的设计更清晰，更易维护，更易单元测试。sql和代码的分离，提高了可维护性。
  + 提供映射标签，支持对象与数据库的orm字段关系映射
  + 提供对象关系映射标签，支持对象关系组建维护
  + 提供xml标签，支持编写动态sql

  **最重要的一点：使用的人多**



## 2. 第一个Mybatis程序

思路：搭建环境-》导入Mybatis包-》编写代码-》测试



### 2.1 搭建环境

创建数据库环境

```mysql
create database mybatis;
use mybatis;

create table user (
	id int(20) not null,
    name varchar(30) default null,
    pwd varchar(30) default null
)engine=innodb default charset=utf8;

insert into user(id, name, pwd) values
(1, 'slz', '123456'),
(2, '神火', '123456'),
(3, '狂神', '123456');

delete from  user where id=1;
```

新建一个普通的maven项目

1. 新建一个普通maven项目（父工程）
2. 创建一个子模块

添加依赖：

```xml
   <!-- https://mvnrepository.com/artifact/org.mybatis/mybatis -->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis</artifactId>
      <version>3.5.6</version>
    </dependency>
    <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>8.0.16</version>
    </dependency>
```



### 2.2 创建模块

+ 在main/java/resources/下创建Mybatis配置文件

```
完整的JdbcUrl: 
jdbc:mysql://localhost:3306/mybatis?useSSL=true&amp;useUnicode=true&amp;characterEncoding=UTF-8&amp;serverTimezone=UTC
```



[mybatis-config.xml]

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<!--核心配置文件-->
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/mybatis?serverTimezone=UTC"/>
                <property name="username" value="root"/>
                <property name="password" value="shenhuo"/>
            </dataSource>
        </environment>
    </environments>
    <!--每一个Mpapper.xml都需要在Mybatis核心配置文件中注册！-->
    <mappers>
        <mapper resource="com/ahulearn/dao/UserMapper.xml"/>
    </mappers>
</configuration>
```

+ 编写Mybatisg工具类

```java
public class Mybatis {
    //全局静态变量
    private static SqlSessionFactory sqlSessionFactory;
    static {
        //从配置文件中获取SqlSessionFactory
        String resource = "mybatis-config.xml";
        try {
            InputStream inputStream = Resources.getResourceAsStream(resource);
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        }catch(IOException e){
            e.printStackTrace();
        }
    }
    //使用SqlSessionFactory创建SqlSession实例
    //SqlSesion包含了面向数据库执行SQL命令所需的所有方法
    public static SqlSession getSqlSession(){
        SqlSession sqlSession = sqlSessionFactory.openSession();
        return sqlSsession;
    }
}
```



### 2.3 编写代码

+ 实体类

  ```java
  package com.ahulearn.pojo;
  
  //实体类
  public class User {
      private int id;
      private String name;
      private String pwd;
      public User() {
      }
  
      public User(int id, String name, String pwd) {
          this.id = id;
          this.name = name;
          this.pwd = pwd;
      }
  
      public int getId() {
          return id;
      }
  
      public String getName() {
          return name;
      }
  
      public String getPwd() {
          return pwd;
      }
  
      public void setId(int id) {
          this.id = id;
      }
  
      public void setName(String name) {
          this.name = name;
      }
  
      public void setPwd(String pwd) {
          this.pwd = pwd;
      }
  }
  ```

  

+ Dao接口

  ```java
  public interface UserDao {
      List<User> getUsers();
  }
  ```

  

+ 接口实现类：由原来的UserDaoImpl转变为一个Mapper.xml配置文件

```xml
<?xml version="1.0" encoding="UTF-8" ?>
        <!DOCTYPE mapper
                PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
                "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!--namespace绑定一个对应的Dao/Mapper接口-->
<mapper namespace="com.ahulearn.dao.UserDao">
    <!--select查询语句
        id: 接口中的方法
        返回结果: 完全限定名，resultType，resultMap
    -->
    <select id="getUserList" resultType="com.ahulearn.pojo.User">
        select * from mybatis.user where id = #{id}
    </select>
</mapper>
```



### 2.4 测试

在test目录下创建和待测试文件一样的目录结构进行测试，test/java/com.ahulearn/dao

+ 测试代码

```java
package com.ahulearn.dao;

import com.ahulearn.pojo.User;
import com.ahulearn.utils.Mybatis;
import org.apache.ibatis.session.SqlSession;
import org.junit.Test;

import java.util.List;

public class UserDaoTest {
    @Test
    public void test() {
        //获取SqlSession对象
        SqlSession sqlSession = Mybatis.getSqlSession();
        //执行SQL: 方式一, 面向接口编程，获取UserDao接口对象
        UserDao userDao = sqlSession.getMapper(UserDao.class);
        //调用接口方法
        List<User> userList = userDao.getUserList();
        for (User user : userList) {
            System.out.println(user.toString());
        }
        //关闭SqlSession
        sqlSession.close();
    }
}

```



java.lang.ExceptionInInitializerError

​	at com.ahulearn.dao.UserDaoTest.test(UserDaoTest.java:14)

Mapper.xml文件没用添加到mybatis主配置文件中，或者没有当作资源文件发布。



java.lang.NullPointerException

全局变量问题：

```java
private static SqlSessionFactory sqlSessionFactory;
static {
    //  获取SqlSessionFactory
    String resource = "mybatis-config.xml";
    try {
        InputStream inputStream = Resources.getResourceAsStream(resource);
        //注意此处使用全局变量，不能再用类声明。SqlSessionFactory sqlSessionFactory = ...形式
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
    }catch(IOException e){
        e.printStackTrace();
    }
}
```



错误

```error
org.apache.ibatis.exceptions.PersistenceException: 
### Error querying database.  Cause: java.sql.SQLException: Error setting driver on UnpooledDataSource. Cause: java.lang.ClassNotFoundException: Cannot find class: com.mysql.cj.jdbc.Driver
### The error may exist in com/ahulearn/dao/Mapper.xml
### The error may involve com.ahulearn.dao.UserMapper.selectById
### The error occurred while executing a query
### Cause: java.sql.SQLException: Error setting driver on UnpooledDataSource. 
```

没有添加MySQL依赖，工厂返回NULL



## 3. CRUD

**1. namespace**

namespace中的包名要和Dao/Mapper中的接口的包名相同，绑定接口

**2. select**

选择，查询语句：

+ id：namespace对应的接口中的方法名
+ resultType：Sql语句执行的返回值! 该返回值类型在定义时要和表结构一致，即类属性要和表头一一对应。
+ parameterType: 参数类型

只需要改接口，接口映射、测试类



代码

```xml
<mapper namespace="com.ahulearn.mapper.UserMapper">
    <!--select查询语句
        id: 对应接口中的方法名
        返回结果: 完整路径类名, resultType，resultMap
    -->
    <select id="selectUser" resultType="user">
        select * from mybatis.user;
    </select>
    <insert id="addUser" parameterType="user">
        insert into mybatis.user(id, name, pwd) values (#{id}, #{name}, #{pwd});
    </insert>
    <delete id="deleteUser" parameterType="int">
        delete from mybatis.user where id=#{id};
    </delete>
    <update id="updateUser" parameterType="user">
        update mybatis.user set id=#{id},name=#{name},pwd=#{pwd} where id=#{id};
    </update>
</mapper>
```



