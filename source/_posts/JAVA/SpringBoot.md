---
title: SpringBoot
date: 2023-08-23 13:00:00
tags:
 - CS
 - SpringBoot
 - JAVA
typora-root-url: ..
typora-copy-images-to: ..\img\springboot
---



官方文档：https://spring.io/projects/spring-boot#learn

其他笔记：

**主要参考**：[ Spring Boot 2 学习笔记（1 / 2）_KISS-CSDN博客](https://blog.csdn.net/u011863024/article/details/113667634)

[SpringBootWeb模块的默认规则研究_大恐龙的小弟的博客-CSDN博客](https://blog.csdn.net/qq_43240702/article/details/111032361)

## 01、基础入门-Spring生态圈

[Spring官网](https://spring.io/)

### Spring能做什么



![image-20210623135328829](../img/springboot/image-20210623135328829.png)

#### Spring的生态

覆盖了：

- web开发
- 数据访问
- 安全控制
- 分布式
- 消息服务
- 移动开发
- 批处理
- …



<!--more-->



#### Spring5重大升级

- 响应式编程

![在这里插入图片描述](../img/springboot/20210205004250581.png)

+ 内部源码设计

基于Java8的一些新特性，如：接口默认实现。重新设计源码架构。

接口的默认实现：即适配器模式（adapter）

+ 由于接口的抽象方法太多，而一般情况下我们只需要使用接口的某几个方法，此时继承了接口必须实现所有方法，即便不用，也要加上空方法。
+ 此时我们使用适配器实现接口的所有方法，通过继承适配器来重新部分方法即可，避免大量无用的方法实现



### 为什么用SpringBoot

> Spring Boot makes it easy to create stand-alone, production-grade Spring based Applications that you can “just run”.link



### SpringBoot优点
+ Create stand-alone Spring applications

  + 创建独立Spring应用

+ Embed Tomcat, Jetty or Undertow directly (no need to deploy WAR files)

  + 内嵌web服务器

+ Provide opinionated ‘starter’ dependencies to simplify your build configuration

  + 自动starter依赖，简化构建配置

+ Automatically configure Spring and 3rd party libraries whenever possible

  + 自动配置Spring以及第三方功能

+ Provide production-ready features such as metrics, health checks, and externalized configuration
  
+ 提供生产级别的监控、健康检查及外部化配置
  
+ Absolutely no code generation and no requirement for XML configuration

  + 无代码生成、无需编写XML

  

> SpringBoot是整合Spring技术栈的一站式框架
>
> SpringBoot是简化Spring技术栈的快速开发脚手架





#### SpringBoot缺点

- 人称版本帝，迭代快，需要时刻关注变化
- 封装太深，内部原理复杂，不容易精通

## 02、基础入门-SpringBoot的大时代背景

### 微服务

[James Lewis and Martin Fowler (2014)](https://martinfowler.com/articles/microservices.html) 提升微服务完整概念：https://martinfowler.com/microservices/

> In short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery. There is a bare minimum of centralized management of these services, which may be written in different programming languages and use different data storage technologies.——James Lewis and Martin Fowler (2014)



+ 微服务是一种架构风格
+ 一个应用拆分为一组小型服务
+ 每个服务运行在自己的进程内，也就是可独立部署和升级
+ 服务之间使用轻量级HTTP交互
+ 服务围绕业务功能拆分
+ 可以由全自动部署机制独立部署
+ 去中心化，服务自治。服务可以使用不同的语言、不同的存储技术



### 分布式

![在这里插入图片描述](/img/springboot/2021020500434620.png)



### 分布式的困难

- 远程调用
- 服务发现
- 负载均衡
- 服务容错
- 配置管理
- 服务监控
- 链路追踪
- 日志管理
- 任务调度
- …



#### 分布式的解决

- SpringBoot + SpringCloud

![在这里插入图片描述](/img/springboot/20210205004523307.png)

### 云原生

原生应用如何上云。 Cloud Native

#### 上云的困难

- 服务自愈：出问题自动复制另一台服务自愈
- 弹性伸缩：自动扩展下线服务
- 服务隔离：一台出问题，不影响其他
- 自动化部署：自动化部署
- 灰度发布：新老版本共存并逐步取代所有老版
- 流量治理：负载均衡
- …



## 03、基础入门-SpringBoot官方文档架构

- [Spring Boot官网](https://spring.io/projects/spring-boot)
- Spring Boot官方文档：https://docs.spring.io/spring-boot/docs/current/reference/html/
- 官方PDF：https://docs.spring.io/spring-boot/docs/2.5.1/reference/pdf/spring-boot-reference.pdf

### 官网文档架构

![image-20210623150038557](/img/springboot/image-20210623150038557.png)

权限信息

概览：可以点进去下载pdf

入门

入门进阶

高级特性

监控

部署

命令行应用

插件

小技巧

资源信息：

所有可以配置的属性

配置源信息

自动配置



## 04、基础入门-SpringBoot-HelloWorld

### 系统要求

- Java 8
- Maven 3.3+
- IntelliJ IDEA 2019.1.2

### Maven配置文件

Maven安装目录下**conf/settings.xml**新添内容：

```xml
<!--设置仓库源-->
<mirrors>
	<mirror>
		<id>nexus-aliyun</id>
		<mirrorOf>central</mirrorOf>
		<name>Nexus aliyun</name>
		<url>http://maven.aliyun.com/nexus/content/groups/public</url>
	</mirror>
	<mirror>
      <id>nexus-aliyun2</id>
      <mirrorOf>*,!jeecy,!jeecg-snapshots</mirrorOf>
      <name>aliyun maven2</name>
      <url>http://maven.aliyun.com/nexus/content/repositories/central/</url>
    </mirror>
</mirrors>

<!--设置jDK编译版本，可以不修改，在项目pom.xml中修改-->
<profiles>
	<profile>
		<id>jdk-1.8</id>

		<activation>
			<activeByDefault>true</activeByDefault>
			<jdk>1.8</jdk>
		</activation>

		<properties>
			<maven.compiler.source>1.8</maven.compiler.source>
			<maven.compiler.target>1.8</maven.compiler.target>
			<maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>
		</properties>
	</profile>
</profiles>
```



#### 创建maven工程

#### 创建pom.xml文件，引入父项目

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>myproject</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    
    <!--引入父项目-->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.1</version>
    </parent>

    <!-- Additional lines to be added here... -->

</project>

```



#### 添加依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

创建主程序

Maven默认编译src/main/java路径下的资源

创建src/main/java/com/example/MyApplication.java，写入以下代码

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@EnableAutoConfiguration
public class MyApplication {

    @RequestMapping("/")
    String home() {
        return "Hello World!";
    }

    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }

}
```

一般写法是只声明主类，不在主类中进行业务处理：

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MainApplication {

    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }

}
```

编写Controller

```java
package com.example.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

//@RestController
@Controller
@RequestMapping("/hello")
public class HelloController {
    @GetMapping("/h1")
    //声明直接返回字符串
    @ResponseBody
    public String hello() {
        return "hello";
    }
}
```



#### SpringBoot配置

在maven工程的resource文件夹中创建application.properties文件。

springboot 所有配置均有默认值，不配置可直接启动

```properties
# 设置端口号
server.port=8888
```

[所有其他配置](https://docs.spring.io/spring-boot/docs/2.3.7.RELEASE/reference/html/appendix-application-properties.html#common-application-properties-server)



#### 打包部署

在pom.xml添加部署插件

```xml
<build>
	<plugins>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
		</plugin>
	</plugins>
</build>
```



+ mvn clean：清空目录

+ mvn package：打包程序

+ 运行：java -jar boot-01-helloworld-1.0-SNAPSHOT.jar

取消cmd的快速编辑模式，否则命令行方式启动SpringBoot时如果点击命令行，可能终止启动



## 05、基础入门-SpringBoot-依赖管理特性

- 父项目：做依赖管理

```xml
<!--依赖管理-->
<parent>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-parent</artifactId>
	<version>2.3.4.RELEASE</version>
</parent>

<!--上面项目的父项目如下：-->
<parent>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-dependencies</artifactId>
	<version>2.3.4.RELEASE</version>
</parent>

<!--它几乎声明了所有开发中常用的依赖的版本号，自动版本仲裁机制-->
```



starter的含义及支持的所有场景：https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.build-systems.starters

>Starters are a set of convenient dependency descriptors that you can include in your application. You get a one-stop shop for all the Spring and related technologies that you need without having to hunt through sample code and copy-paste loads of dependency descriptors. For example, if you want to get started using Spring and JPA for database access, include the `spring-boot-starter-data-jpa` dependency in your project.



+ 开发导入starter场景启动器
  1、见到很多 spring-boot-starter-* ： *就某种场景
  2、只要引入starter，这个场景的所有常规需要的依赖我们都自动引入
  3、更多SpringBoot所有支持的场景
  4、见到的 *-spring-boot-starter： 第三方为我们提供的简化开发的场景启动器。

  5、所有场景的启动器最底层的依赖

```xml
<!--所有场景启动器最底层的依赖-->
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter</artifactId>
	<version>2.3.4.RELEASE</version>
	<scope>compile</scope>
</dependency>
```



- 无需关注版本号，自动版本仲裁
  1. 引入依赖默认都可以不写版本
  2. 引入非版本仲裁的jar，要写版本号。



- 可以修改默认版本号
  1. 查看spring-boot-dependencies里面规定当前依赖的版本 用的 key。
  2. 在当前项目的pom.xml配置文件，添加如下面的代码。

```xml
<properties>
    <!--查看底层父项目的标签-->
	<mysql.version>5.1.43</mysql.version>
</properties>
```



IDEA快捷键：

- `ctrl + shift + alt + U`：以图的方式显示项目中依赖之间的关系。
- `alt + ins`：相当于Eclipse的 Ctrl + N，创建新类，新包等。



## 06、基础入门-SpringBoot-自动配置特性

- 自动配好Tomcat
  - 引入Tomcat依赖。
  - 配置Tomcat

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-tomcat</artifactId>
	<version>2.3.4.RELEASE</version>
	<scope>compile</scope>
</dependency>
```

- 自动配好SpringMVC
  - 引入SpringMVC全套组件
  - 自动配好SpringMVC常用组件（功能）
- 自动配好Web常见功能，如：字符编码问题
  - SpringBoot帮我们配置好了所有web开发的常见场景

```java
public static void main(String[] args) {
    //1、返回我们IOC容器
    ConfigurableApplicationContext run = SpringApplication.run(MainApplication.class, args);

    //2、查看容器里面的组件
    String[] names = run.getBeanDefinitionNames();
    for (String name : names) {
        System.out.println(name);
    }
}
```

- 默认的包结构
  - 主程序所在包及其下面的所有子包里面的组件都会被默认扫描进来
  - 无需以前的包扫描配置
  - 想要改变扫描路径
    - @SpringBootApplication(scanBasePackages=“com.lun”)
    - @ComponentScan 指定扫描路径

```java
@SpringBootApplication
//等同于以下三个注解
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan("com.lun")
```



- SpringBoot各种配置拥有默认值
  - 默认配置最终都是映射到某个类上，如：`MultipartProperties`
  - 配置文件的值最终会绑定每个类上，这个类会在容器中创建对象



- 所有自动配置项是按需加载
  - 非常多的starter，引入了哪些场景这个场景的自动配置才会开启
  - SpringBoot所有的自动配置功能都在 spring-boot-autoconfigure 包里面



## 07、底层注解-@Configuration配置类注解

- 实验环境

基本的bean

+ User

```java
package com.example.helloworld.bean;

public class User {
    private String name;
    private Integer age;
    private Pet pet;

    public Pet getPet() {
        return pet;
    }

    public void setPet(Pet pet) {
        this.pet = pet;
    }

    public User() {
    }

    public User(String name, Integer age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "User{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", pet=" + pet +
                '}';
    }
}
```

+ Pet

```java
package com.example.helloworld.bean;

public class Pet {
    private String name;

    public Pet() {
    }

    public Pet(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Pet{" +
                "name='" + name + '\'' +
                '}';
    }
}
```



- 基本使用
  - Full模式与Lite模式
  - 示例

```java
package com.example.helloworld.config;

import com.example.helloworld.bean.Pet;
import com.example.helloworld.bean.User;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @Configuration 声明这是一个配置类
 * 1、配置类里面使用@Bean标注在方法上给容器注册组件，默认也是单实例的
 * 2、配置类本身也是组件
 * 3、proxyBeanMethods：代理bean的方法
 *      Full(proxyBeanMethods = true)（保证每个@Bean方法被调用多少次返回的组件都是单实例的）（默认）
 *      Lite(proxyBeanMethods = false)（每个@Bean方法被调用多少次返回的组件都是新创建的）
 */
@Configuration(proxyBeanMethods = false) //告诉SpringBoot这是一个配置类 == 配置文件
public class MyConfig {

    /**
     * Full:外部无论对配置类中的这个组件注册方法调用多少次获取的都是之前注册容器中的单实例对象
     * @return
     */
    @Bean //给容器中添加组件。默认 方法名为组件id。返回类型就是组件类型。返回的值，就是组件在容器中的实例
    public User user01(){
        User user = new User("张三", 18);
        //user组件依赖Pet组件.
        //但由于此时proxyBeanMethods = false，user中获取的并不是容器中的Pet, 而是创建了一个新的Pet
        user.setPet(tomcatPet());
        return user;
    }

    @Bean(name="tom01") //指定组件id名为tom
    public Pet tomcatPet(){
        return new Pet("tomcat");
    }
}
```



@Configuration测试代码如下:

```java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan("com.atguigu.boot")
public class MainApplication {

    public static void main(String[] args) {
    //1、返回我们IOC容器
        ConfigurableApplicationContext run = SpringApplication.run(MainApplication.class, args);

    //2、查看容器里面的组件
        String[] names = run.getBeanDefinitionNames();
        for (String name : names) {
            System.out.println(name);
        }

    //3、从容器中获取组件
        Pet tom01 = run.getBean("tom", Pet.class);
        Pet tom02 = run.getBean("tom", Pet.class);
        System.out.println("组件："+(tom01 == tom02));

    //4、com.atguigu.boot.config.MyConfig$$EnhancerBySpringCGLIB$$51f1e1ca@1654a892
        MyConfig bean = run.getBean(MyConfig.class);
        System.out.println(bean);

    //如果@Configuration(proxyBeanMethods = true)代理对象调用方法。SpringBoot总会检查这个组件是否在容器中有。
        //保持组件单实例
        User user = bean.user01();
        User user1 = bean.user01();
        System.out.println(user == user1);

        User user01 = run.getBean("user01", User.class);
        Pet tom = run.getBean("tom", Pet.class);

        System.out.println("用户的宠物："+(user01.getPet() == tom));
    }
}
```

- 最佳实战
  - 配置 类组件之间**无依赖关系**用Lite模式加速容器启动过程，减少判断
  - 配置 类组件之间**有依赖关系**，方法会被调用得到之前单实例组件，用Full模式（默认）

>lite 英 [laɪt] 美 [laɪt]
>adj. 低热量的，清淡的(light的一种拼写方法);类似…的劣质品



IDEA快捷键：

- `Alt + Ins`:生成getter，setter、构造器等代码。
- `Ctrl + Alt + B`:查看类的具体实现代码。





## 08、底层注解-@Import导入组件

+ 使用@import导入类，自动调用类的无参构造创建组件，可以放在任何被Springboot管理的组件中，不一定放入config配置类上

@Bean、@Component、@Controller、@Service、@Repository，它们是Spring的基本注解，在Spring Boot中也可以导入容器。

@ComponentScan 在**06、基础入门-SpringBoot-自动配置特性**有用例。

@Import({User.class, DBHelper.class})给容器中**自动创建出这两个类型的组件**、默认组件的名字就是全类名

```java
//使用无参构造创建两个组件, 默认组件id为全类名
@Import({User.class, DBHelper.class}) 
@Configuration(proxyBeanMethods = false)
public class MyConfig {
}
```

测试类：

```java

//1、返回我们IOC容器
ConfigurableApplicationContext run = SpringApplication.run(MainApplication.class, args);

//...

//5、获取组件
String[] beanNamesForType = run.getBeanNamesForType(User.class);

for (String s : beanNamesForType) {
    System.out.println(s);
}

DBHelper bean1 = run.getBean(DBHelper.class);
System.out.println(bean1);
```



## 9、底层注解-@Conditional条件装配

**条件装配：满足Conditional指定的条件，则进行组件注入** 有很多派生注解

![image-20210628123240922](/assets/springboot/image-20210628123240922.png)

ctrl+h：打开继承树

用@ConditionalOnMissingBean举例说明

+ 配置类

```java
 /**
  * 放在配置类上，如果某个组件存在，该配置才生效
  */
@Configuration(proxyBeanMethods = false)
@ConditionalOnMissingBean(name = "tom")//容器中没有tom的Bean时，MyConfig类的Bean才能生效。
public class MyConfig {

    @Bean
    public User user01(){
        User zhangsan = new User("zhangsan", 18);
        zhangsan.setPet(tomcatPet());
        return zhangsan;
    }

    @Bean("tom22")
    public Pet tomcatPet(){
        return new Pet("tomcat");
    }
    /**
     * 如果容器中存在tom组件则注册user02组件
     */
    @ConditionalOnBean(name = "tom02")//容器中有tom02的Bean时，才注册user02
    @Bean
    public User user02(){
        User user = new User("张三", 18);
        user.setPet(tomcatPet());
        return user;
    }
}
```

+ 主程序类

```java
public static void main(String[] args) {
    //1、返回我们IOC容器
    ConfigurableApplicationContext run = SpringApplication.run(MainApplication.class, args);

    //2、查看容器里面的组件
    String[] names = run.getBeanDefinitionNames();
    for (String name : names) {
        System.out.println(name);
    }

    /**
		 * @Import
		 */
		//5、获取所有User类型的组件
		String[] beanNamesForType = run.getBeanNamesForType(User.class);

		for (String s : beanNamesForType) {
			System.out.println(s);
		}

		DBHelper bean1 = run.getBean(DBHelper.class);
		System.out.println(bean1);

		/**
		 *  @Conditional
		 *  containsBean判断容器中是否存在指定组件
		 */
		boolean tom03 = run.containsBean("tom");
		System.out.println("容器中Tom03组件："+tom03);//false

		boolean tom22 = run.containsBean("tom01");
		System.out.println("容器中tom22组件："+tom22);//true

		boolean user02 = run.containsBean("user02");
		System.out.println("容器中user02组件："+user02);//false

		boolean user03 = run.containsBean("user01");
		System.out.println("容器中user02组件："+user03);//true

}
```





## 10、底层注解-@ImportResource 导入Spring配置文件

比如，公司使用bean.xml文件生成配置bean，然而你为了省事，想继续复用bean.xml，可以使用@ImportResource注解。

bean.xml：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!-- Spring方式注册bean，springboot是使用config配置类-->
    <bean id="haha" class="com.example.helloworld.bean.User">
        <property name="name" value="张三"/>
        <property name="age" value="18"/>
        <property name="pet" ref="hehe"/>
    </bean>

    <bean id="hehe" class="com.example.helloworld.bean.Pet">
        <property name="name" value="tomcat"/>
    </bean>

</beans>
```



使用方法：

```java
@ImportResource("classpath:beans.xml")
public class MyConfig {
...
}
```

测试类：

```java
public static void main(String[] args) {
    //1、返回我们IOC容器
    ConfigurableApplicationContext run = SpringApplication.run(MainApplication.class, args);

	boolean haha = run.containsBean("haha");
	boolean hehe = run.containsBean("hehe");
	System.out.println("haha："+haha);//true
	System.out.println("hehe："+hehe);//true
}
```



## 11、底层注解-@ConfigurationProperties配置绑定

如何使用Java读取到properties文件中的内容，并且把它封装到JavaBean中，以供随时使用

传统方法，十分复杂：

```java
public class getProperties {
	public static void main(String[] args) throws FileNotFoundException, IOException {
		Properties pps = new Properties();
		pps.load(new FileInputStream("a.properties"));
		Enumeration enum1 = pps.propertyNames();//得到配置文件的名字
		while(enum1.hasMoreElements()) {
			String strKey = (String) enum1.nextElement();
			String strValue = pps.getProperty(strKey);
			System.out.println(strKey + "=" + strValue);
			//封装到JavaBean。
		}
	}
}
```



**Spring Boot一种配置配置绑定**：

@ConfigurationProperties + @Component

+ 基本的bean, Car

```java
package com.example.helloworld.bean;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * 只有容器中的组件，才有springboot提供的强大功能
 * @Component 加入Spring容器中
 * @ConfigurationProperties 绑定配置文件
 */
@Component
@ConfigurationProperties(prefix = "mycar")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Car {
    private String brand;
    private Integer price;

    @Override
    public String toString() {
        return "Car{" +
                "brand='" + brand + '\'' +
                ", price=" + price +
                '}';
    }
}
```

+ 配置文件application.properties

```yml
mycar.brand=BYD
mycar.price=100000
```

+ Controller

```java
package com.example.helloworld.controller;

import com.example.helloworld.bean.Car;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    
    //自动装配
    @Autowired
    Car car;
    @RequestMapping("/car")
    public Car car() {
        return car;
    }
}
```



**Spring Boot另一种配置配置绑定**：

@EnableConfigurationProperties + @ConfigurationProperties

@EnableConfigurationProperties(Car.class)的作用

1. 开启Car配置绑定功能
2. 把Car这个组件自动注册到容器中

```java
@EnableConfigurationProperties(Car.class)
public class MyConfig {
...
}

```

```java
@ConfigurationProperties(prefix = "mycar")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Car {
    private String brand;
    private Integer price;

    @Override
    public String toString() {
        return "Car{" +
                "brand='" + brand + '\'' +
                ", price=" + price +
                '}';
    }
}
```



## 12、自动配置-自动包规则原理

Spring Boot应用的启动类：

```java
/**
 * @SpringBootApplication相当与下面三个注解：
 * @SpringBootConfiguration
 * @EnableAutoConfiguration
 * @ComponentScan()
 */
@SpringBootApplication
public class MainApplication {

    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }

}
```



分析下`@SpringBootApplication`

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(
    excludeFilters = {@Filter(
    type = FilterType.CUSTOM,
    classes = {TypeExcludeFilter.class}
), @Filter(
    type = FilterType.CUSTOM,
    classes = {AutoConfigurationExcludeFilter.class}
)}
)
public @interface SpringBootApplication {
    ...
}

```



重点分析`@SpringBootConfiguration`，`@EnableAutoConfiguration`，`@ComponentScan`



### @SpringBootConfiguration

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Configuration
public @interface SpringBootConfiguration {
    @AliasFor(
        annotation = Configuration.class
    )
    boolean proxyBeanMethods() default true;
}

```

除了元注解之外，就是一个`@Configuration`，表示主启动类也是一个配置类。

### @ComponentScan

指定扫描哪些路径，Spring注解。

@ComponentScan 在 **07、基础入门-SpringBoot-自动配置特性** 有用例。

### @EnableAutoConfiguration

最重要的注解就是 @EnableAutoConfiguration

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(AutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {
    String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";

    Class<?>[] exclude() default {};

    String[] excludeName() default {};
}
```

重点包含两个注解`@AutoConfigurationPackage`，`@Import(AutoConfigurationImportSelector.class)`。

#### @AutoConfigurationPackage

标签名直译为：自动配置包，指定了默认的包规则。

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@Import(AutoConfigurationPackages.Registrar.class)//给容器中导入Registrar组件
public @interface AutoConfigurationPackage {
    String[] basePackages() default {};

    Class<?>[] basePackageClasses() default {};
}

```

1. @Import给容器中导入一个组件Registrar，利用Registrar给容器批量导入一系列组件
2. 将指定注解标注的包下的所有组件导入spring IOC容器中。



#### @Import(AutoConfigurationImportSelector.class) 初始加载自动配置类

1. 利用`getAutoConfigurationEntry(annotationMetadata);`给容器中批量导入一些组件
2. 调用`List<String> configurations = getCandidateConfigurations(annotationMetadata, attributes)`获取到所有需要导入到容器中的配置类
3. 利用工厂加载 `Map<String, List<String>> loadSpringFactories(@Nullable ClassLoader classLoader);`得到所有的组件
4. 从`META-INF/spring.factories`位置来加载一个文件。
   1. 默认扫描我们当前引入的所有包中的`META-INF/spring.factories`路径的文件
   2. `spring-boot-autoconfigure-2.3.4.RELEASE.jar`包里面也有`META-INF/spring.factories`

```xml
# 文件里面写死了spring-boot一启动就要给容器中加载的所有配置类 共127个
# spring-boot-autoconfigure-2.3.4.RELEASE.jar/META-INF/spring.factories
# Auto Configure
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.springframework.boot.autoconfigure.admin.SpringApplicationAdminJmxAutoConfiguration,\
org.springframework.boot.autoconfigure.aop.AopAutoConfiguration,\
...
```

127个默认组件

![image-20210628142105606](../img/springboot/image-20210628142105606.png)

虽然127个场景的所有自动配置启动的时候默认全部加载，但是`xxxxAutoConfiguration`按照条件装配规则（`@Conditional`），最终会按需配置。



如`AopAutoConfiguration`类：

```java
@Configuration(
    proxyBeanMethods = false
)
@ConditionalOnProperty(
    prefix = "spring.aop",
    name = "auto",
    havingValue = "true",
    matchIfMissing = true
)
public class AopAutoConfiguration {
    public AopAutoConfiguration() {
    }
	...
}

```

## 13、自动配置-自动配置流程

SpringBoot自动配置相关，在 **spring-boot-autoconfigure-xxx.jar** 中

以`DispatcherServletAutoConfiguration`的内部类`DispatcherServletConfiguration`为例子:

+ 整段代码相当于alis，如果MultipartResolver.class类型的组件id不是标准名称multipartResolver，则设置别名为multipartResolver
+ 放在用户设置的下载解析器名称不规范

```java
@Bean
@ConditionalOnBean(MultipartResolver.class)  //容器中有这个类型组件
@ConditionalOnMissingBean(name = DispatcherServlet.MULTIPART_RESOLVER_BEAN_NAME) //容器中没有名字 为multipartResolver 的组件
public MultipartResolver multipartResolver(MultipartResolver resolver) {
	//给@Bean标注的方法传入了对象参数，这个参数的值会从容器中找。
	//SpringMVC multipartResolver。防止有些用户配置的文件上传解析器不符合规范
	// Detect if the user has created a MultipartResolver but named it incorrectly
	return resolver;//给容器中加入了文件上传解析器；
}
```



SpringBoot默认会在底层配好所有的组件，但是**如果用户自己配置了以用户的优先**。



**总结**：

+ SpringBoot先加载所有的自动配置类 xxxxxAutoConfiguration
+ 每个自动配置类按照条件生效，一旦生效默认都会绑定配置文件指定的值。（xxxxProperties类中读取，xxxProperties类和配置文件进行了绑定）
+ 生效的配置类就会给容器中装配很多组件
+ 只要容器中有这些组件，相当于这些功能就有了
+ 定制化配置
  + 用户直接自己@Bean替换底层的组件
  + 用户去看这个组件是获取的配置文件什么值就去修改

**xxxxxAutoConfiguration —> 组件 —> xxxxProperties类中拿值 ----> application.properties**



## 14、最佳实践-SpringBoot应用如何编写

+ 引入场景依赖
  + 官方文档：https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.build-systems.starters
+ 查看自动配置了哪些（选做）
  + 自己分析，引入场景对应的自动配置一般都生效了
  + 配置文件中 debug=true 开启自动配置报告。
    + Negative（不生效）
    + Positive（生效）
+ 是否需要修改
  + 参照文档修改配置项
    + 官方文档
    + 自己分析。xxxxProperties绑定了配置文件的哪些。
  + 自定义加入或者替换组件
    + @Bean、@Component…
  + 自定义器 XXXXXCustomizer；
  + …

## 15、最佳实践-Lombok简化开发


Lombok用标签方式代替构造器、getter/setter、toString()等鸡肋代码。

spring boot已经管理Lombok。引入依赖：

```xml
 <dependency>
     <groupId>org.projectlombok</groupId>
     <artifactId>lombok</artifactId>
</dependency>
```

IDEA中File->Settings->Plugins，搜索安装Lombok插件。

```java
@NoArgsConstructor
//@AllArgsConstructor
@Data
@ToString
@EqualsAndHashCode
public class User {

    private String name;
    private Integer age;

    private Pet pet;

    public User(String name,Integer age){
        this.name = name;
        this.age = age;
    }
}
```

简化日志开发

```java
@Slf4j
@RestController
public class HelloController {
    @RequestMapping("/hello")
    public String handle01(@RequestParam("name") String name){
        log.info("请求进来了....");
        return "Hello, Spring Boot 2!"+"你好："+name;
    }
}
```





## 17、配置文件-yaml的用法

同以前的properties用法

YAML 是 “YAML Ain’t Markup Language”（YAML 不是一种标记语言）的递归缩写。在开发的这种语言时，YAML 的意思其实是：“Yet Another Markup Language”（仍是一种标记语言）。

**非常适合用来做以数据为中心的配置文件**。



### 基本语法

- key: value；kv之间的冒号后有空格
- 大小写敏感
- 使用空格缩进表示层级关系(同一层级左对齐即可)
- 缩进不允许使用tab，只允许空格
- 缩进的空格数不重要，只要相同层级的元素左对齐即可
- '#'表示注释
- 字符串无需加引号，如果要加单引号’’表示插入转义符、双引号""表示字符串原样输出不转义



### 数据类型

- 字面量：单个的、不可再分的值。date、boolean、string、number、null

```yaml
k: v
```

- 对象：键值对的集合。map、hash、set、object

```yaml
#行内写法：  
k: {k1:v1,k2:v2,k3:v3}

#或
k: 
  k1: v1
  k2: v2
  k3: v3
```



- 数组：一组按次序排列的值。array、list、queue

```yaml
#行内写法：  
k: [v1,v2,v3]

#或者
k:
 - v1
 - v2
 - v3

```



### 示例

```java
//绑定配置文件前缀
@ConfigurationProperties(prefix = "person")
@Data
public class Person {
    private String userName;
    private Boolean boss;
    private Date birth;
    private Integer age;
    private Pet pet;
    private String[] interests;
    private List<String> animal;
    private Map<String, Object> score;
    private Set<Double> salarys;
    private Map<String, List<Pet>> allPets;
}

@Data
public class Pet {
    private String name;
    private Double weight;
}
```

用yaml表示以上对象

写在 `application.yml` 中，优先级是`application.properties`优先

```yaml
person:
  userName: zhangsan
  boss: false
  birth: 2019/12/12 20:12:33
  age: 18
  pet: 
    name: tomcat
    weight: 23.4
  interests: [篮球,游泳]
  animal: 
    - jerry
    - mario
  score:
    english: 
      first: 30
      second: 40
      third: 50
    math: [131,140,148]
    chinese: {first: 128,second: 136}
  salarys: [3999,4999.98,5999.99]
  allPets:
    sick:
      - {name: tom}
      - {name: jerry,weight: 47}
    health: [{name: mario,weight: 47}]
```



## 18、配置文件-自定义类绑定的配置提示

    You can easily generate your own configuration metadata file from items annotated with @ConfigurationProperties by using the spring-boot-configuration-processor jar. The jar includes a Java annotation processor which is invoked as your project is compiled.——link
需要在pom.xml中添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-configuration-processor</artifactId>
    <optional>true</optional>
</dependency>

<!-- 2.4之前最好添加下面插件，作用是工程打包时，不将spring-boot-configuration-processor打进包内，让其只在编码的时候有用 -->
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <excludes>
                    <exclude>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-configuration-processor</artifactId>
                    </exclude>
                </excludes>
            </configuration>
        </plugin>
    </plugins>
</build>
```



## 19、web场景-web开发简介

Spring Boot provides auto-configuration for Spring MVC that **works well with most applications.(大多场景我们都无需自定义配置)**

The auto-configuration adds the following features on top of Spring’s defaults:



- Inclusion of `ContentNegotiatingViewResolver` and `BeanNameViewResolver` beans.

  - 内容协商视图解析器和BeanName视图解析器
- Support for serving static resources, including support for WebJars (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-static-content))).
  - 静态资源（包括webjars）

- Automatic registration of `Converter`, `GenericConverter`, and `Formatter` beans.
  - 自动注册 `Converter，GenericConverter，Formatter`
- Support for `HttpMessageConverters` (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-message-converters)).
  - 支持 `HttpMessageConverters` （后来我们配合内容协商理解原理）
- Automatic registration of `MessageCodesResolver` (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-message-codes)).
  - 自动注册 `MessageCodesResolver` （国际化用）
- Static `index.html` support.
  - 静态index.html 页支持
- Custom `Favicon` support (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-favicon)).
  - 自定义 `Favicon`
- Automatic use of a `ConfigurableWebBindingInitializer` bean (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-web-binding-initializer)).
  - 自动使用 `ConfigurableWebBindingInitializer` ，（DataBinder负责将请求数据绑定到JavaBean上）

> If you want to keep those Spring Boot MVC customizations and make more MVC customizations (interceptors, formatters, view controllers, and other features), you can add your own @Configuration class of type WebMvcConfigurer but without @EnableWebMvc.
> 不用@EnableWebMvc注解。使用 @Configuration + WebMvcConfigurer 自定义规则



> If you want to provide custom instances of RequestMappingHandlerMapping, RequestMappingHandlerAdapter, or ExceptionHandlerExceptionResolver, and still keep the Spring Boot MVC customizations, you can declare a bean of type WebMvcRegistrations and use it to provide custom instances of those components.
>
> 声明 WebMvcRegistrations 改变默认底层组件



> If you want to take complete control of Spring MVC, you can add your own @Configuration annotated with @EnableWebMvc, or alternatively add your own @Configuration-annotated DelegatingWebMvcConfiguration as described in the Javadoc of @EnableWebMvc.
>
> 使用 @EnableWebMvc+@Configuration+DelegatingWebMvcConfiguration 全面接管SpringMVC



## 20、web场景-静态资源规则与定制化

### 静态资源目录

只要静态资源放在类路径下： called `/static` (or `/public` or `/resources` or `/META-INF/resources`

访问 ： 当前项目根路径/ + 静态资源名

原理： 静态映射/**。

请求进来，先去找Controller看能不能处理。不能处理的所有请求又都交给静态资源处理器。静态资源也找不到则响应404页面。

也可以改变默认的静态资源路径，`/static`，`/public`,`/resources`, `/META-INF/resources`失效

```yml
resources:
  static-locations: [classpath:/haha/]
```

### 静态资源访问前缀

```yml
spring:
  mvc:
    static-path-pattern: /res/**
```

当前项目 + static-path-pattern + 静态资源名 = 静态资源文件夹下找

### webjar

可用jar方式添加css，js等资源文件，

https://www.webjars.org/

例如，添加jquery

```xml
<dependency>
    <groupId>org.webjars</groupId>
    <artifactId>jquery</artifactId>
    <version>3.5.1</version>
</dependency>
```

访问地址：http://localhost:8080/webjars/jquery/3.5.1/jquery.js 后面地址要按照依赖里面的包路径。



## 21、web场景-welcome与favicon功能

官方文档: https://docs.spring.io/spring-boot/docs/2.3.8.RELEASE/reference/htmlsingle/#boot-features-spring-mvc-welcome-page

### 欢迎页支持

- 静态资源路径下 index.html
  - 可以配置静态资源路径
  - 但是不可以配置静态资源的访问前缀。否则导致 index.html不能被默认访问

```yml
spring:
#  mvc:
#    static-path-pattern: /res/**   指定静态资源前缀，会导致welcome page功能失效
  resources:
    static-locations: [classpath:/haha/]
```

- controller能处理/index

### 自定义Favicon

指网页标签上的小图标。

favicon.ico 放在静态资源目录下即可。

```yml
spring:
#  mvc:
#    static-path-pattern: /res/**   指定静态资源前缀，会导致 Favicon 功能失效
```



## 22、web场景-【源码分析】-静态资源原理

- SpringBoot启动默认加载 xxxAutoConfiguration 类（自动配置类）
- SpringMVC功能的自动配置类`WebMvcAutoConfiguration`，生效



```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnWebApplication(type = Type.SERVLET)
@ConditionalOnClass({ Servlet.class, DispatcherServlet.class, WebMvcConfigurer.class })
@ConditionalOnMissingBean(WebMvcConfigurationSupport.class)
@AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE + 10)
@AutoConfigureAfter({ DispatcherServletAutoConfiguration.class, TaskExecutionAutoConfiguration.class,
		ValidationAutoConfiguration.class })
public class WebMvcAutoConfiguration {
    ...
}
```

给容器中配置的内容：

- 配置文件的相关属性的绑定：WebMvcProperties==**spring.mvc**、ResourceProperties==**spring.resources**

```java
@Configuration(proxyBeanMethods = false)
@Import(EnableWebMvcConfiguration.class)
@EnableConfigurationProperties({ WebMvcProperties.class, ResourceProperties.class })
@Order(0)
public static class WebMvcAutoConfigurationAdapter implements WebMvcConfigurer {
    ...
}
```



### WEB场景需要主要分析的包

+ org.sspringframework.boot.autoconfigure: 路径org.springframework.boot:spring-boot-autoconfigure

  自动配置原理

+ org.springframework.web.servlet: 路径org.springframework:spring-webmvc

  web应用原理





### 配置类只有一个有参构造器

```java
有参构造器所有参数的值都会从容器中确定
public WebMvcAutoConfigurationAdapter(WebProperties webProperties, WebMvcProperties mvcProperties,
		ListableBeanFactory beanFactory, ObjectProvider<HttpMessageConverters> messageConvertersProvider,
		ObjectProvider<ResourceHandlerRegistrationCustomizer> resourceHandlerRegistrationCustomizerProvider,
		ObjectProvider<DispatcherServletPath> dispatcherServletPath,
		ObjectProvider<ServletRegistrationBean<?>> servletRegistrations) {
	this.mvcProperties = mvcProperties;
	this.beanFactory = beanFactory;
	this.messageConvertersProvider = messageConvertersProvider;
	this.resourceHandlerRegistrationCustomizer = resourceHandlerRegistrationCustomizerProvider.getIfAvailable();
	this.dispatcherServletPath = dispatcherServletPath;
	this.servletRegistrations = servletRegistrations;
	this.mvcProperties.checkConfiguration();
}
```

- ResourceProperties resourceProperties；获取和spring.resources绑定的所有的值的对象
- WebMvcProperties mvcProperties 获取和spring.mvc绑定的所有的值的对象
- ListableBeanFactory beanFactory Spring的beanFactory
- HttpMessageConverters 找到所有的HttpMessageConverters
- ResourceHandlerRegistrationCustomizer 找到 资源处理器的自定义器。
- DispatcherServletPath
- ServletRegistrationBean 给应用注册Servlet、Filter…



### 资源处理的默认规则

```java
...
public class WebMvcAutoConfiguration {
    ...
	public static class EnableWebMvcConfiguration extends DelegatingWebMvcConfiguration implements ResourceLoaderAware {
        ...
		@Override
		protected void addResourceHandlers(ResourceHandlerRegistry registry) {
			super.addResourceHandlers(registry);
			if (!this.resourceProperties.isAddMappings()) {
				logger.debug("Default resource handling disabled");
				return;
			}
			ServletContext servletContext = getServletContext();
			addResourceHandler(registry, "/webjars/**", "classpath:/META-INF/resources/webjars/");
			addResourceHandler(registry, this.mvcProperties.getStaticPathPattern(), (registration) -> {
				registration.addResourceLocations(this.resourceProperties.getStaticLocations());
				if (servletContext != null) {
					registration.addResourceLocations(new ServletContextResource(servletContext, SERVLET_LOCATION));
				}
			});
		}
        ...
        
    }
    ...
}
```



根据上述代码，我们可以同过配置禁止所有静态资源规则。

```yml
spring:
  resources:
    add-mappings: false   #禁用所有静态资源规则
```

静态资源规则：

```yml
@ConfigurationProperties(prefix = "spring.resources", ignoreUnknownFields = false)
public class ResourceProperties {

    private static final String[] CLASSPATH_RESOURCE_LOCATIONS = { "classpath:/META-INF/resources/",
            "classpath:/resources/", "classpath:/static/", "classpath:/public/" };

    /**
     * Locations of static resources. Defaults to classpath:[/META-INF/resources/,
     * /resources/, /static/, /public/].
     */
    private String[] staticLocations = CLASSPATH_RESOURCE_LOCATIONS;
    ...
}
```

### 欢迎页的处理规则

```java
...
public class WebMvcAutoConfiguration {
    ...
	public static class EnableWebMvcConfiguration extends DelegatingWebMvcConfiguration implements ResourceLoaderAware {
        ...
		@Bean
		public WelcomePageHandlerMapping welcomePageHandlerMapping(ApplicationContext applicationContext,
				FormattingConversionService mvcConversionService, ResourceUrlProvider mvcResourceUrlProvider) {
			WelcomePageHandlerMapping welcomePageHandlerMapping = new WelcomePageHandlerMapping(
					new TemplateAvailabilityProviders(applicationContext), applicationContext, getWelcomePage(),
					this.mvcProperties.getStaticPathPattern());
			welcomePageHandlerMapping.setInterceptors(getInterceptors(mvcConversionService, mvcResourceUrlProvider));
			welcomePageHandlerMapping.setCorsConfigurations(getCorsConfigurations());
			return welcomePageHandlerMapping;
		}
```

`WelcomePageHandlerMapping`的构造方法如下：

```java
WelcomePageHandlerMapping(TemplateAvailabilityProviders templateAvailabilityProviders,
                          ApplicationContext applicationContext, Resource welcomePage, String staticPathPattern) {
    if (welcomePage != null && "/**".equals(staticPathPattern)) {
        //要用欢迎页功能，必须是/**
        logger.info("Adding welcome page: " + welcomePage);
        setRootViewName("forward:index.html");
    }
    else if (welcomeTemplateExists(templateAvailabilityProviders, applicationContext)) {
        //调用Controller /index
        logger.info("Adding welcome page template: index");
        setRootViewName("index");
    }
}
```

这构造方法内的代码也解释了**web场景-welcome与favicon功能**中配置`static-path-pattern`了，welcome页面和小图标失效的问题。







### 参数映射

+ @PathVariable("路径变量")
+ @RequestHeader("请求头参数")
+ @RequestParam("?请求参数")
+ @CookieValue("cookie值")
+ @RequestBody("请求体，post请求中的表单")
+ @RequestAttribute("获取request域属性")
  + 即获取前一个请求request.setAttribute("", "")放入的参数
+ @MatrixVariable(value = "矩阵变量", pathVar = "path")
  + 需要和路径变量合用
  + /users/{tom;age=34;name=byd}
  + 分号前是访问路径，分号后是矩阵变量，即controller中只需要GetMapping("/users/{path}")
  + 路径重写，解决cookie被禁用的问题
  + SpringBoot默认关闭矩阵变量 



### 定制SpringMVC

在config类中添加一个 WebMvcConfigurer bean

```java
@Bean
public WebMvcConfigurer webMvcConfigurer() {
    //接口
    return new WebMvcConfigurer() {
        @Override
        public void extendMessageConverters(List<HttpMessageConverter<?>> converters) {
            
        }
    }
}
```

 



## 23、模板引擎

springboot默认打jar包，是一种压缩格式，而jsp不支持在jar包中编译，因此springboot默认不支持jsp，引入了第三方模板引擎

Thymeleaf：简单，自然语言的模板，但不高效。




## 24、数据库

查看版本：

```xml
父项目spring boot
    <parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.5.0</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>
spring boot 版本仲裁依赖
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-dependencies</artifactId>
    <version>2.5.0</version>
  </parent>
```



```yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/my_test?serverTimezone=UTC&useSSL=false
    username: root
    password: shenhuo
    driver-class-name: com.mysql.jdbc.Driver
    # 如果导入数据源但是不配置属性项目会启动失败
```





##  25、整合第三方技术到spring boot 中

第三方是否提供starter，提供可以直接使用，不提供则需要手动导入自定义使用



导入依赖

```xml
        <dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid</artifactId>
			<version>1.1.17</version>
		</dependency>
```

配置文件

```xml
<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource" destroy-method="close">
    <property name="url" value="${jdbc.url}" />
    <property name="username" value="${jdbc.username}" />
    <property name="password" value="${jdbc.password}" />
    <property name="maxActive" value="20" />
    <property name="initialSize" value="1" />
    <property name="maxWait" value="60000" />
    <property name="minIdle" value="1" />
    <property name="timeBetweenEvictionRunsMillis" value="60000" />
    <property name="minEvictableIdleTimeMillis" value="300000" />
    <property name="testWhileIdle" value="true" />
    <property name="testOnBorrow" value="false" />
    <property name="testOnReturn" value="false" />
    <property name="poolPreparedStatements" value="true" />
    <property name="maxOpenPreparedStatements" value="20" />
</bean>
```

