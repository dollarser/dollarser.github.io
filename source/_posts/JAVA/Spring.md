---
title: Spring
date: 2023-05-27 18:00:00
tags:
 - CS
 - Spring
 - Java
categories:
 - Java
typora-root-url: ..
typora-copy-images-to: ..\img\spring
---



## 1. Spring

官网：https://spring.io/projects/spring-framework/

文档：https://docs.spring.io/spring-framework/docs/current/reference/html/index.html

**三大核心**：

​	控制反转（ioc）-----> Inversion of Control

​	依赖注入（di）---- >Dependency Injection

​	面向切面编程（AOP）---->Aspect Oriented Programming



<!--more-->



+ 测试依赖

```xml
   <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.11</version>
      <scope>test</scope>
    </dependency>
```

+ 测试代码写在/src/test/java目录下，最好包结构也和待测试代码一致。
+ 测试代码中main函数可加但是**不需要**加测试注解，如果要测试其他函数则mian函数**不能**加测试注解

```java
import com.ahulearn.pojo.People;
import com.ahulearn.pojo.ResourceTest;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MyTest {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("beans3.xml");
        People people = context.getBean("people", People.class);
        people.getCat().shout();
        people.getDog().shout();
    }
    @Test
    public void testResource() {
        ApplicationContext context = new ClassPathXmlApplicationContext("beans3.xml");
        ResourceTest resource = context.getBean("resource", ResourceTest.class);
        resource.getCat().shout();
        resource.getDog().shout();
    }
}
```



## 2. IOC思想

文档：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html

1. UserDao接口：面向接口编程
2. UserDaoImpl实现类
3. UserService业务接口：业务层，就是用来调用Dao层
4. UserService也算实现类
5. 用户测试类

+ 工厂模式



### 2.1 为什么需要IOC

下方案例，如果用户获取用户的需求发生改变，则需要做

+ 添加一个新的UserDao实现类
+ 修改UserServiceI实现类的方法，调用新的的UserDao类

这只是一个需求需要更改的情况，且项目本身很小。对于大项目需要修改的内容十分繁杂。如果项目代码需要每一次根据用户需求的改变或增加而大量修改代码显然是不合理的。





+ UserDao接口

```java
package com.ahulearn.dao;

public interface UserDao {
    void getUsers();
}
```

+ UserDaoImpl实现类

```java
package com.ahulearn.dao;

public class UserDaoImpl implements UserDao {
    @Override
    public void getUsers() {
        System.out.println("获取用户数据");
    }
}
```

+ UserService业务接口

```java
package com.ahulearn.service;

public interface UserService {
    void getUsers();
}
```

+ UserServiceImpl实现类

```java
package com.ahulearn.service;

import com.ahulearn.dao.UserDao;
import com.ahulearn.dao.UserDaoImpl;

public class UserServiceImpl implements UserService {
    //业务层调用dao层
    private UserDao userDao = new UserDaoImpl();

    @Override
    public void getUsers() {
        userDao.getUsers();
    }
}
```

+ 用户测试类

```java
package com.ahulearn;

import com.ahulearn.service.UserService;
import com.ahulearn.service.UserServiceImpl;

public class MyTest {
    public static void main(String[] args) {
        //用户实际调用业务层, 不需要接触Dao层
        UserService userService = new UserServiceImpl();
        userService.getUsers();
    }
}
```



解决方法：利用set方法，实现动态的创建值的注入

方法很简单，但思想很深刻

+ UserServiceImpl实现类

```java
package com.ahulearn.service;

import com.ahulearn.dao.UserDao;

public class UserServiceImpl implements UserService {
    //业务层调用dao层
    private UserDao userDao;

    public void setUserDao(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public void getUsers() {
        userDao.getUsers();
    }
}
```

+ 用户测试类: 利用泛型的思想，根据用户需求将不同的实现类传给service层，不需要对service层进行修改，只需要在业务层增加相应的实现即可。
+ 存在一个问题就是，用户层需要接触dao层的具体实现类

```java
package com.ahulearn;

import com.ahulearn.dao.UserDaoImpl;
import com.ahulearn.dao.UserDaoMysqlImpl;
import com.ahulearn.service.UserService;
import com.ahulearn.service.UserServiceImpl;


public class MyTest {
    public static void main(String[] args) {
        //用户实际调用业务层, 不需要接触Dao层
        UserService userService = new UserServiceImpl();
        ((UserServiceImpl)userService).setUserDao(new UserDaoImpl());
        userService.getUsers();
    }
}
```

+ 之前，对象是程序主动创建的，控制权在程序员的手上。
+ 使用set注入后，程序不再具有主动性，而是变成被动的接受对象！

这种思想，从本质上解决问题，程序员不需要再去管理对象的创建。系统的耦合性降低，可以更加专注业务的实现上。

这是IOC的原型，并不是真正的IOC。



**IOC的本质**

**控制反转**（Inversion of Control，缩写为**IoC**），是面向对象编中的一种设计原则，可以用来减低计算机代码之间的耦合度。其中最常见的方式叫做**依赖注入**（Dependency Injection，简称**DI**），还有一种方式叫“依赖查找”（Dependency Lookup）。通过控制反转，对象在被创建的时候，由一个调控系统内所有对象的外界实体将其所依赖的对象的引用传递给它。也可以说，依赖被注入到对象中。



## 3. HelloSpring

控制反转中初始化对象属性是依赖对象中的set方法实现的。

+ 对象

```java
package com.ahulearn.pojo;

public class Hello {
    private String str;

    @Override
    public String toString() {
        return "Hello{" +
                "str='" + str + '\'' +
                '}';
    }

    public String getStr() {
        return str;
    }

    public void setStr(String str) {
        this.str = str;
    }
}
```



+ beans.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <!--使用Spring来创建对象，在Spring这些称为Bean
    类型 变量名 = new 类型();
    Hello hello = new Hello();
    id = 变量名
    class = new 的对象
    property 相当于给对象中的属性设置一个值
    -->
    <bean id="hello" class="com.ahulearn.pojo.Hello">
        <property name="str" value="Spring"/>
    </bean>
</beans>
```



+ 测试类

```java
package com.ahulearn.pojo;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MyTest {
    public static void main(String[] args) {
        //获取Spring的上下文对象
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        //我们的对象现在都在Spring中管理，我们要使用，直接去里面取出来就可以！
        Hello hello = (Hello) context.getBean("hello");
        System.out.println(hello);
    }
}

```



+ 重写IOC思想案例测试类

```java
package com.ahulearn.pojo;

import com.ahulearn.service.UserServiceImpl;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class TestIoc {
    public static void main(String[] args) {
        //获取ApplicationContext：拿到Spring的容器
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        UserServiceImpl userServiceImpl = (UserServiceImpl) context.getBean("userServiceImpl");
        userServiceImpl.getUsers();
    }
}
```

beans.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--使用spring重写模块1中的内容-->
    <bean id="userDaoImpl" class="com.ahulearn.dao.UserDaoImpl"/>
    <bean id="mysqlImpl" class="com.ahulearn.dao.UserDaoMysqlImpl"/>
    <bean id="sqlImpl" class="com.ahulearn.dao.UserDaoSqlImpl"/>
    <bean id="userServiceImpl" class="com.ahulearn.service.UserServiceImpl">
        <!--
        ref: 引用Spring容器中创建好的对象
        value: 具体的值，基本数据类型
        -->
        <property name="userDao" ref="userDaoImpl"/>
    </bean>
</beans>
```

注意：运行出错可能是代码没有重新编译

此时修改实现只需要修改xml配置文件，配置文件可以通过配置选修修改。或者手动修改配置文件。但不需要修改代码了。用户和服务都不需要修改。



## 4. IOC创建对象

+ 依赖包

```xml
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>5.2.10.RELEASE</version>
      <scope>test</scope>
    </dependency>
```



Spring在创建容器后，容器中注册管理的所有对象都被初始化了。

1. 默认使用无参构造对象！

2. 要使用有参构造创建对象

   + 下标赋值

   ```xml
       <!--通过参数索引，有参构造-->
       <bean id="user1" class="com.ahulearn.pojo.User">
           <constructor-arg index="0" value="sl"/>
       </bean>
   ```

   + 参数类型

   ```xml
       <!--通过参数类型，有参构造-->
       <bean id="user2" class="com.ahulearn.pojo.User">
           <constructor-arg type="java.lang.String" value="lz"/>
       </bean>
   ```

   + 引用方式

   ```xml
       <!--主流方法，通过形参名，有参构造-->
       <bean id="user3" class="com.ahulearn.pojo.User">
           <constructor-arg name="name" value="令章"/>
       </bean>
   ```

## 5. Spring配置

### 5.1 别名

```xml
    <bean id="user3" class="com.ahulearn.pojo.User">
        <constructor-arg name="name" value="令章"/>
    </bean>
    <!--别名-->
    <alias name="user3" alias="user"/>
```

### 5.2 bean

id: bean的唯一标识符，相当于对象名

class: bean对象对应的全限定命名：包名+类型

name: 别名，相当于用alias去定义别名, 且可以同时取多个别名

```xml
    <!--name创建别名，可以创建多个别名，别名间通过逗号，分号或空格分隔-->
    <bean id="user4" class="com.ahulearn.pojo.User" name="userName,u">
        <constructor-arg name="name" value="令章"/>
    </bean>
```



### 5.3 import

import一般用于团队开发使用，他可以将多个配置文件，导入合并为一个：applicationContext.xml

假设，现在项目中有多个人开发，两个人负责不同的类开发，不同的类需要注册在不同的bean中，可以利用import将所有人的beans.xml合并为一个总的配置文件，使用的时候只需要使用总的配置文件即可。

如果两个文件中，存在相同的id, 则后导入的会覆盖之前导入的bean.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">
    <import resource="beans.xml"/>
    <import resource="beans2.xml"/>
</beans>
```



## 6. 依赖注入

文档：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-collaborators

### 6.1构造器注入

上方第5节已经使用并介绍

### 6.2 set注入【重点】

+ 依赖注入
  + 依赖：bean对象的创建依赖于容器！
  + 注入：bean对象的所有属性，由容器来注入！

【环境搭建】

1. 复杂类型

```java
package com.ahulearn.pojo;

public class Address {
    private String address;

    public void setAddress(String address) {
        this.address = address;
    }

    @Override
    public String toString() {
        return "Address{" +
                "address='" + address + '\'' +
                '}';
    }
}
```

```java
public class Student {
    private String name;
    private Address address;
    private String[] books;
    private List<String> hobbies;
    private Map<String, String> card;
    private Set<String> games;
    private String wife; //空指针Null
    private Properties info; //配置类
}
```



2. 真实测试对象

```java
package com.ahulearn.pojo;

import java.util.*;

public class Student {
    private String name;
    private Address address;
    private String[] books;
    private List<String> hobbies;
    private Map<String, String> card;
    private Set<String> games;
    private String wife; //空指针Null
    private Properties info; //配置类

    public Student() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public String[] getBooks() {
        return books;
    }

    public void setBooks(String[] books) {
        this.books = books;
    }

    public List<String> getHobbies() {
        return hobbies;
    }

    public void setHobbies(List<String> hobbies) {
        this.hobbies = hobbies;
    }

    public Map<String, String> getCard() {
        return card;
    }

    public void setCard(Map<String, String> card) {
        this.card = card;
    }

    public Set<String> getGames() {
        return games;
    }

    public void setGames(Set<String> games) {
        this.games = games;
    }

    public String getWife() {
        return wife;
    }

    public void setWife(String wife) {
        this.wife = wife;
    }

    public Properties getInfo() {
        return info;
    }

    public void setInfo(Properties info) {
        this.info = info;
    }

    @Override
    public String toString() {
        return "Student{" +
                "name='" + name + '\'' +
                ", address=" + address.toString() +
                ", books=" + Arrays.toString(books) +
                ", hobbies=" + hobbies +
                ", card=" + card +
                ", games=" + games +
                ", wife='" + wife + '\'' +
                ", info=" + info +
                '}';
    }
}
```



3. beans.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="address" class="com.ahulearn.pojo.Address">
        <property name="address" value="复旦大学"/>
    </bean>
    <!--set方法注入-->
    <bean id="student" class="com.ahulearn.pojo.Student">
        <!--普通注入，直接赋值-->
        <property name="name" value="slz"/>
        <!--Bean id引用注入-->
        <property name="address" ref="address"/>
        <!--数组注入， ref-->
        <property name="books">
            <array>
                <value>红楼梦</value>
                <value>西游记</value>
                <value>三国演绎</value>
                <value>水浒传</value>
            </array>
        </property>
        <!--List注入， ref-->
        <property name="hobbies">
            <list>
                <value>听歌</value>
                <value>看电影</value>
                <value>敲代码</value>
            </list>
        </property>
        <!--Map注入-->
        <property name="card">
            <map>
                <entry key="身份证" value="341623343886816642"/>
                <entry key="银行卡" value="1233423412314321342"/>
            </map>
        </property>
        <!--Set注入-->
        <property name="games">
            <set>
                <value>LOL</value>
                <value>COC</value>
                <value>FGO</value>
            </set>
        </property>
        <!--Null和空字符串-->
        <property name="wife">
            <null/>
        </property>
        <!--Property key=>value形式-->
        <property name="info">
            <props>
                <prop key="driver">com.mysql.jdbc.Driver</prop>
                <prop key="url">jdbc:mysql://localhost:3306/mydb</prop>
                <prop key="username">root</prop>
                <prop key="password">1234</prop>
            </props>
        </property>

    </bean>

</beans>
```

4. 测试类

```java
import com.ahulearn.pojo.Student;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MyTest {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        Student student = (Student)context.getBean("student");
        //System.out.println(student.getName());
        System.out.println(student);
    }
}
```



### 6.3 拓展方式注入

p命名空间注入，对应set方式注入

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:p="http://www.springframework.org/schema/p"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">
    <!--p命名空间注入，等同于通过set方法注入，必须要有无参构造方法，不然对象都构造不出，就不能设置属性-->
    <bean id="user1" class="com.ahulearn.pojo.User" p:name="slz" p:age="18"/>
</beans>
```



c命名空间注入，对应构造器注入

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:p="http://www.springframework.org/schema/p"
       xmlns:c="http://www.springframework.org/schema/c"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">
    <!--p命名空间注入，等同于通过set方法注入，必须要有无参构造方法，不然对象都构造不出，就不能设置属性-->
    <bean id="user1" class="com.ahulearn.pojo.User" p:name="slz" p:age="18"/>
    <!--c命名空间注入，等同于通过构造方法注入,要求必须定义有参构造：construct-args-->
    <bean id="user2" class="com.ahulearn.pojo.User" c:name="slz" c:age="18"/>
</beans>
```

注意点：p命名和c命名不能直接使用，需要导入相应的xml约束

```xml
xmlns:p="http://www.springframework.org/schema/p"
xmlns:c="http://www.springframework.org/schema/c"
```



### 6.4 Bean Scopes 作用域

文档：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes

6种作用域，后两种类似



| Scope                                                        |                         Description                          |
| :----------------------------------------------------------- | :----------------------------------------------------------: |
| [singleton](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes-singleton) | (Default) Scopes a single bean definition to a single object instance for each Spring IoC container. |
| [prototype](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes-prototype) | Scopes a single bean definition to any number of object instances. |
| [request](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes-request) | Scopes a single bean definition to the lifecycle of a single HTTP request. That is, each HTTP request has its own instance of a bean created off the back of a single bean definition. Only valid in the context of a web-aware Spring `ApplicationContext`. |
| [session](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes-session) | Scopes a single bean definition to the lifecycle of an HTTP `Session`. Only valid in the context of a web-aware Spring `ApplicationContext`. |
| [application](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes-application) | Scopes a single bean definition to the lifecycle of a `ServletContext`. Only valid in the context of a web-aware Spring `ApplicationContext`. |
| [websocket](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#websocket-stomp-websocket-scope) | Scopes a single bean definition to the lifecycle of a `WebSocket`. Only valid in the context of a web-aware Spring `ApplicationContext`. |

1. 单例模式singleton (Spring默认机制)

   每次从容器中get, 同一个id取出的是同一个对象

```xml
<!--单例模式-->
<bean id="user3" class="com.ahulearn.pojo.User" c:name="lz" c:age="19" scope="singleton"/>
```

2. 原型模式prototype (多线程可能有用)

   每次从容器中get, 同一个id都会产生一个新对象！

```xml
<!--原型模式-->
<bean id="user4" class="com.ahulearn.pojo.User" c:name="lz" c:age="19" scope="prototype"/>
```

3. 其余的request、session、application，这些只能在web开发中使用到！

   request: 在一次请求中存活，session: 在一个会话中存活，application：全局有效





## 7. Bean的自动装配

+ 自动装配是Spring满足bean依赖的一种方式！
+ Spring会在上下文中自动寻找，并自动给bean装配属性！

在Spring中由三种装配方式

1. 在xml中显示的配置
2. 在java中显示的配置
3. 隐式的自动装配bean【重点】

### 7.1 测试

环境搭建：一个人有两个宠物，看到一句话要立马反应出有几个对象

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="dog" class="com.ahulearn.pojo.Dog"/>
    <bean id="cat" class="com.ahulearn.pojo.Cat"/>
    <bean id="people" class="com.ahulearn.pojo.People">
        <property name="name" value="kl"/>
        <property name="cat" ref="cat"/>
        <property name="dog" ref="dog"/>
    </bean>
</beans>
```



### 7.2 byName自动装配

要求bean ID要和set方法名一致，比如setCat方法装配则找id为cat的bean

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="dog" class="com.ahulearn.pojo.Dog"/>
    <bean id="cat" class="com.ahulearn.pojo.Cat"/>
    <!--
    byName：自动在容器上下文中和自己对象set方法后面的值对应的bean_id, 比如setCat则找id为cat的bean
    -->
    <bean id="people1" class="com.ahulearn.pojo.People" autowire="byName">
        <property name="name" value="kl"/>
    </bean>
</beans>
```



### 7.3 byType自动装配

要求beans中的类型必须全局唯一，用于装配的bean甚至可以需要拥有bean-id

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean class="com.ahulearn.pojo.Dog"/>
    <bean class="com.ahulearn.pojo.Cat"/>

    <!--
    byName：自动在容器上下文中和自己对象set方法后面的值对应的bean_id, 比如setCat则找id为cat的bean
    -->
    <bean id="people" class="com.ahulearn.pojo.People" autowire="byType">
        <property name="name" value="kl"/>
    </bean>
</beans>
```



### 7.4 使用注解自动装配

JDK1.5支持注解，Spring2.5开始支持注解

文档：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-annotation-config

要使用注解须知：

1. 导入约束： `xmlns:context="http://www.springframework.org/schema/context"`
2. 配置注解的支持: ` <context:annotation-config/>`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        https://www.springframework.org/schema/context/spring-context.xsd">

    <context:annotation-config/>

</beans>
```



+ 注解依赖：

```xml
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-beans</artifactId>
      <version>5.2.10.RELEASE</version>
      <scope>compile</scope>
    </dependency>
```

+ 导入包：`import org.springframework.beans.factory.annotation.Autowired;`




#### 7.4.1 **@Autowired**

注解可以在属性上用，或者set方法上用，一般写在属性上。需要在IOC容器中注册相应的id.

如果写在属性上，set方法都不用再写，因为注解是通过反射实现的，但get方法不能省略。

注解优先按类型查找，没有类型匹配则报错；找到多个则按name匹配，如果没有name匹配的则报错。

```java
package com.ahulearn.pojo;

import org.springframework.beans.factory.annotation.Autowired;

public class People {
    private String name;
    @Autowired
    private Cat cat;
    private Dog dog;

    public void setName(String name) {
        this.name = name;
    }

    public void setCat(Cat cat) {
        this.cat = cat;
    }

    @Autowired
    public void setDog(Dog dog) {
        this.dog = dog;
    }
}

```



+ **@Autowired(required=false)** : 默认是true，如果设置成false则允许字段为空，即在beans可以不注册该对象。跳过装配。

```java
public class People {
    private String name;
    //如果显示的定义了Autowired的required属性为false,说明这个对象可以为null,否则不能为空
    @Autowired(required=false)
    private Cat cat;
    @Autowired
    private Dog dog;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Cat getCat() {
        return cat;
    }

    public Dog getDog() {
        return dog;
    }
}
```

可以在xml不添加cat的bean，但必须添加dog的bean

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/context
       https://www.springframework.org/schema/context/spring-context.xsd">
    <!--开启注解支持-->
    <context:annotation-config/>
    <!--不需要注入任何东西-->
    <bean id="dog" class="com.ahulearn.pojo.Dog"/>
    <bean id="people" class="com.ahulearn.pojo.People"/>

</beans>
```

@Nullable: 允许标记的字段为空

```java
import org.springframework.lang.Nullable;

public class People {
    private String name;
    @Autowired
    private Cat cat;
    private Dog dog;

    //允许name为空
    public People(@Nullable String name) {
        this.name = name;
    }

}

```

#### 7.4.2 @Qualifier

+ 如果自动装配环境比较复杂，在beans注册对象中，通过类型可以匹配超过一个对象，但name都不匹配，可以配合@Qualifier(value="cat2")注解指定要装配的id

```java
package com.ahulearn.pojo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;

public class People {
    private String name;
    //如果显示的定义了Autowired的required属性为false,说明这个对象可以为null,否则不能为空
    @Autowired(required=false)
    @Qualifier(value="cat2")
    private Cat cat;
    @Autowired
    private Dog dog;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Cat getCat() {
        return cat;
    }

    public Dog getDog() {
        return dog;
    }
}
```



#### 7.4.3 **@Resource**

javax包下的注解，功能类似spring中的@Autowired注解，首先通过类型匹配，之后通过name匹配，可以手动指定name

+ @Resource(name="cat2")
+ 依赖：javax下的包属于java拓展包，没有包含在java核心包中，需要自己添加依赖

```xml
    <dependency>
      <groupId>javax.annotation</groupId>
      <artifactId>javax.annotation-api</artifactId>
      <version>1.3.2</version>
    </dependency>
```

```java
package com.ahulearn.pojo;
import javax.annotation.Resource;
public class ResourceTest {
    private String name;
    @Resource(name="cat2")
    private Cat cat;
    @Resource
    private Dog dog;

    public String getName() {
        return name;
    }
    public Cat getCat() {
        return cat;
    }

    public Dog getDog() {
        return dog;
    }
}
```



## 8. 使用自动装配注解Component开发

在Spring4之后，要使用注解开发，必须导入aop包

```xml
<!-- https://mvnrepository.com/artifact/org.springframework/spring-aop -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aop</artifactId>
    <version>5.3.5</version>
</dependency>
```



### 8.1 bean

+ 导入约束applicationContext.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/context
       https://www.springframework.org/schema/context/spring-context.xsd">
    <!--指定要扫描的包，只有指定的包下的Component注解才会生效-->
    <context:component-scan base-package="com.ahulearn.pojo"/>
    <!--注解驱动-->
    <context:annotation-config/>
    <import resource="beans.xml"/>

</beans>
```



```java
package com.ahulearn.pojo;

import org.springframework.stereotype.Component;

//等价于<bean id="user" class="com.ahulearn.pojo.User"/>
//Component组间，一般放在类上，让spring容器管理该类
@Component
public class User {
    public String name;
}
```



### 8.2 属性如何注入



```java
package com.ahulearn.pojo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

//等价于<bean id="user" class="com.ahulearn.pojo.User"/>
//Component组间，一般放在类上，让spring容器管理该类
@Component
public class User {
    /**Value相当于
     *<bean id="user" class="com.ahulearn.pojo.User">
     *   <property name="name" value="kk"/>
     *</bean>
     * 用于简单的注入，复杂配置用xml
     */
    @Value("slz")
    public String name;
}

```

+ 测试类

```java
import com.ahulearn.pojo.User;
import com.ahulearn.service.UserService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MyTest {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
        //因为注解扫描装配没有配置bean,因此不存在bean id,通过getBean取对象时必须使用类名小写首字母的形式
        User user = context.getBean("user", User.class);
        System.out.println(user.name);
    }
}
```



### 8.3 衍生注解



@Component有几个衍生注解，作用相同，只是名称不同，用在不同的模块中。我们在web开发中，会按照mvc架构分层

+ dao 【@Repository】

```java
package com.ahulearn.dao;
import org.springframework.stereotype.Repository;

/**
 *在dao层Component写作Repository
 * */
@Repository
public class UserDao {
    public String name;
}
```



+ service【@Service】

```java
package com.ahulearn.service;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    public String name;
}
```



+ controller【@Controller】

```java
package com.ahulearn.controller;
import org.springframework.stereotype.Controller;

@Controller
public class UserController {
    public String name;
}
```

这四个注解功能一样，都是代表将某个类注册到Spring中，装配Bean



+ benas.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       https://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/context
       https://www.springframework.org/schema/context/spring-context.xsd">
    <!--指定要扫描的包，只有指定的包下的Component注解才会生效-->
    <context:component-scan base-package="com.ahulearn.pojo"/>
    <context:component-scan base-package="com.ahulearn.dao"/>
    <context:component-scan base-package="com.ahulearn.controller"/>
    <context:component-scan base-package="com.ahulearn.service"/>
    <!--注解驱动-->
    <context:annotation-config/>

</beans>
```



### 8.4 自动装配

```
@Autowired
@Qualifier
@Resource
```



### 8.5 作用域

+ 导入依赖

  ```java
  import org.springframework.context.annotation.Scope;
  ```

+ @Scope
  + 单例模式@Scope("singleton") 等同于beans配置中的属性scope = "singleton"
  + 多例模式@Scope("prototype") 等同于beans配置中的属性scope = "prototype"

```java
package com.ahulearn.pojo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
/*设置作用域*/
@Scope("prototype")
public class User {
    /**Value相当于
     *<bean id="user" class="com.ahulearn.pojo.User">
     *   <property name="name" value="kk"/>
     *</bean>
     * 用于简单的注入，复杂配置用xml
     */
    @Value("slz")
    public String name;
}
```



### 8.6 小结

xml与注解

+ xml功能更强，适合任何场合！维护简单方便，配置都在同一个文件中
+ 注解不是自己的类使用不了，维护相对复杂

xml与注解最佳实践

+ xml用来管理bean
+ 注解只负责完成属性的注入
+ 我们在使用的过程中，只需要注意一个问题：必须让注解生效，就需要开启注解支持

```xml
    <!--指定要扫描的包，只有指定的包下的Component注解才会生效-->
    <context:component-scan base-package="com.ahulearn.pojo"/>
    <!--注解驱动-->
    <context:annotation-config/>
```



## 9. 使用java的方式配置Spring

JavaConfig原是Spring的子项目，在Spring4之后成为核心功能

完全不使用Spring的xml配置，全权交给java来做

文档：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-java

在一个类上加@Configuration类似于写一个配置文件：beans

+ 配置类：AppConfig.java

```java
package com.ahulearn.config;

import com.ahulearn.pojo.User;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

/**表示这是一个配置类，该注解本身也被@Component注解，即也被添加到Spring容器中
 * 和beans.xml作用相同
 * */
@Configuration
/**
 * 配置自动装配，如果自动装配，可以不用写下方的@Bean方法，取对象直接使用类名小写首字母
 * */
@ComponentScan("com.ahulearn.pojo")
/** 导入其他配置类 */
@Import(MyConfig.class)
public class AppConfig {
    /**注册一个bean, 相当于写一个bean标签
     * 方法名相当于bean标签的id属性
     * 返回值，相当于bean标签的class属性*/
    @Bean
    public User myUser() {
        return new User();
    }
}
```

等价于

```xml
<beans>
    <bean id="myUser" class="com.ahulearn.pojo.User"/>
</beans>
```

+ 实体类：User

```java
package com.ahulearn.pojo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/*让Spring容器接管该类，注册到容器中*/
@Component
public class User {
    /*注入初始值*/
    @Value("slz")
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "User{" +
                "name='" + name + '\'' +
                '}';
    }
}
```

+ 测试类

```java
import com.ahulearn.config.AppConfig;
import com.ahulearn.pojo.User;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class MyTest {
    public static void main(String[] args) {
        //从AppConfig中获取容器
        ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
        //从容器中获取对象
        User myUser = (User) context.getBean("myUser");
        System.out.println(myUser.getName());
    }
}
```

纯java的配置方式，在Springboot中随处可见



## 10. AOP-代理模式

为什么学习代码模式？【因为这就是SpringAOP的底层】

代理模式分类：

+ 静态代理
+ 动态代理

使用代理避免修改原有的业务代码（被代理角色），可以方便的添加公用的业务操作。

### 10.1 静态代理

角色分析：

+ 抽象角色：一般会使用接口或抽象类

```java
package com.ahulearn.demo01;

public interface Rent {
    public void rent();
}
```



+ 真实角色：被代理的角色

```java
package com.ahulearn.demo01;

public class Host implements Rent{
    //租房
    public void rent(){
        System.out.println("房东出租房子");
    }
}
```



+ 代理角色：代理真实角色，代理真实角色后，一般还会做附属操作

```java
package com.ahulearn.demo01;

public class Proxy {
    //多用组合，少用继承
    private Host host;

    public Proxy() {
    }

    public Proxy(Host host) {
        this.host = host;
    }

    public void setHost(Host host) {
        this.host = host;
    }
    public void rent(){
        host.rent();
    }
    public void seeHouse(){
        System.out.println("看房");
    }
    public void fare(){
        System.out.println("收中介费");
    }
    public void contract(){
        System.out.println("签租赁合同");
    }
}
```



+ 客户角色：访问代理对象的人

```java
package com.ahulearn.demo01;

public class Client {
    public static void main(String[] args) {
        //房东
        Host host = new Host();
        //代理
        Proxy proxy = new Proxy(host);
        //看房
        proxy.seeHouse();
        //签合同
        proxy.contract();
        //租房
        proxy.rent();
        //收中介费
        proxy.fare();
    }
}
```

代理模式的好处：

+ 可以使真实角色的操作更加纯粹！不用去关注一些公共的业务
+ 公共业务交给代理角色，实现业务分工
+ 公共业务发生扩展的时候，方便集中管理！

缺点：

+ 一个真实角色就会产生一个代理角色；代码量会翻倍*开发效率变低*



### 10.2 静态代理例子-加深理解

代码对应 spring-08-proxy-demo02

![静态代理](../img/spring/10.2_0.png)

+ 抽象角色

```java
package com.ahulearn.demo02;

public interface UserService {
    public void add();
    public void delete();
    public void update();
    public void query();
}
```



+ 真实角色

```java
package com.ahulearn.demo02;

public class UserServiceImpl implements UserService {
    @Override
    public void add() {
        System.out.println("增加了一个用户");
    }

    @Override
    public void delete() {
        System.out.println("删除了一个用户");
    }

    @Override
    public void update() {
        System.out.println("修改了一个用户");
    }

    @Override
    public void query() {
        System.out.println("查询用户");
    }
}

```



+ 代理角色

```java
package com.ahulearn.demo02;

public class UserServiceProxy implements UserService{
    private UserServiceImpl userService;

    public void setUserService(UserServiceImpl userService) {
        this.userService = userService;
    }

    @Override
    public void add() {
        userService.add();
        log("add");
    }

    @Override
    public void delete() {
        userService.delete();
        log("delete");
    }

    @Override
    public void update() {
        userService.update();
        log("update");
    }

    @Override
    public void query() {
        userService.query();
        log("query");
    }
    //日志方法
    public void log(String msg) {
        System.out.println("log: 使用了"+msg+"方法");
    }
}
```



+ 客户角色：访问代理对象的人

```java
package com.ahulearn.demo02;

public class Client {
    public static void main(String[] args) {
        UserServiceImpl userService = new UserServiceImpl();
        UserServiceProxy proxy = new UserServiceProxy();
        proxy.setUserService(userService);

        proxy.add();
        proxy.delete();
    }
}
```



### 10.3 动态代理

底层：反射

+ 动态代理和静态代理角色一样
+ 动态代理的类是动态生成的，不是直接写好的！
+ 动态代理分为两大类：基于接口的动态代理，基于类的动态代理
  + 基于接口--JDK的动态接口【本节使用的方法】
  + 基于来：cglib
  + 基于字节码：JAVAssist 目前用于JBoss 应用服务器项目

需要了解两个类：

+ Proxy: 代理

提供了创建动态代理类和示例的静态方法

```java
//方法调用句柄
InvocationHandler handler = new MyInvocationHandler();
//动态代理类
Class<?> proxyClass = Proxy.getProxyClass(Foo.getClass().getClassLoader(), Foo.getClass());
//动态创建动态代理实例
Foo f = (Foo) proxyClass.getConstructor(InvocationHandler.getClass()).
    newInstance(handler);

//或者更简单地：
Foo proxy = (Foo) Proxy.newProxyInstance(Foo.getClass().getClassLoader(), 
                               new Class<?> [] {Foo.getClass()}, 
                               handler);
```



+ InvocationHandler: 调用处理程序接口

  代理实例的 *调用处理程序* 的接口

  只有一个invoke接口方法，该方法使用反射的方式调用另一个方法。

  ```java
  Object invoke(Object proxy, Method method, Object[] args)
  ```

  

实验环境：

+ 抽象角色：接口

```java
package com.ahulearn.demo03;

public interface Rent {
    public void rent();
}
```



+ 真实角色：实体类

```java
package com.ahulearn.demo03;

public class Host implements Rent {
    public void rent(){
        System.out.println("房东出租房子");
    }
}
```



+ 代理角色

```java
package com.ahulearn.demo03;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class ProxyInvocationHandler implements InvocationHandler {
    //被代理的接口
    private Object target;

    public void setTarget(Object target) {
        this.target = target;
    }

    //生成代理类
    public Object getProxy() {
        return Proxy.newProxyInstance(this.getClass().getClassLoader(), target.getClass().getInterfaces(), this);
    }

    //处理代理示例，并返回结果
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        //前处理
        seeHouse();
        //动态代理的本质，就是使用反射机制实现！
        Object result = method.invoke(target, args);
        //后处理
        fare();
        return result;
    }

    public void seeHouse() { System.out.println("中介带看房子"); }
    public void fare() { System.out.println("收中介费"); }
}
```



+ 用户角色

```java
package com.ahulearn.demo03;

public class Client {
    public static void main(String[] args) {
        //真实角色
        Host host = new Host();
        //代理角色生成程序
        ProxyInvocationHandler pih = new ProxyInvocationHandler();
        //通过调用处理程序来设置要代理的抽象类或接口
        pih.setTarget(host);
        //根据传入的类对应的接口生成抽象类
        Rent proxy = (Rent) pih.getProxy(); //proxy是动态生成的
        //租房
        proxy.rent();
    }
}
```



动态代理的好处：

+ 可以使真实角色的操作更加纯粹！不用去关注一些公共的业务
+ 公共业务交给代理角色，实现业务分工
+ 公共业务发生扩展的时候，方便集中管理！

+ 一个动态代理类代理的是一个接口，一般就是对应一类业务
+ 一个动态代理类可以代理多个类，只要是实现了同一个接口即可！





## 11. AOP

### 11.1 什么是AOP?

AOP（Aspect Oriented Programming）意为：面向切面编程，通过预编译方式和运行期动态代理实现程序功能的统一维护的一种技术。AOP是OOP的延续，是软件开发中的一个热点，也是Spring框架中的一个重要内容，是函数式编程的一种衍生范型。利用AOP可以对业务逻辑的各个部分进行隔离，从而使得业务逻辑各部分之间的耦合度降低，提高程序的可重用性，同时提高了开发的效率。

AOP可以说是OOP（Object-Oriented Programing，面向对象编程）的补充和完善。OOP引入封装、继承和多态性等概念来建立一种对象层次结构，用以模拟公共行为的一个集合。当我们需 要为分散的对象引入公共行为的时候，OOP则显得无能为力。也就是说，**OOP允许你定义从上到下的关系，但并不适合定义从左到右的关系**。例如日志功能。日志代码往往水平地散布在所有对象层次中，而与它所散布到的对象的核心功能毫无关系。对于其他类型的代码，如安全性、异常处理和透明的持续性也是如此。这种散布在各处的无关的代码被称为横切（cross-cutting）代码，在OOP设计中，它导致了大量代码的重复，而不利于各个模块的重用。

而AOP技术则恰恰相反，它利用一种称为“横切”的技术，剖解开封装的对象内部，并将那些影响了多个类的公共行为封装到一个可重用模块，并将其名为 “Aspect”，即方面。所谓“方面”，简单地说，就是将那些与业务无关，却为业务模块所共同调用的逻辑或责任封装起来，便于减少系统的重复代码，降低 模块间的耦合度，并有利于未来的可操作性和可维护性。AOP代表的是一个横向的关系，如果说“对象”是一个空心的圆柱体，其中封装的是对象的属性和行为； 那么面向方面编程的方法，就仿佛一把利刃，将这些空心圆柱体剖开，以获得其内部的消息。而剖开的切面，也就是所谓的“方面”了。然后它又以巧夺天功的妙手将这些剖开的切面复原，不留痕迹。

![图片](../img/spring/11.2_0.jpg)

### 11.2 AOP在Spring中的作用

+ 提供声明式事务；允许用户自定义切面

以下名词需要了解：

| 名称                | 说明                                                         |
| ------------------- | ------------------------------------------------------------ |
| Joinpoint（连接点） | 指那些被拦截到的点，在 Spring 中，可以被动态代理拦截目标类的方法。 |
| Pointcut（切入点）  | 指要对哪些 Joinpoint 进行拦截，即被拦截的连接点。            |
| Advice（通知）      | 指拦截到 Joinpoint 之后要做的事情，即对切入点增强的内容。    |
| Target（目标）      | 指代理的目标对象。                                           |
| Weaving（植入）     | 指把增强代码应用到目标上，生成代理对象的过程。               |
| Proxy（代理）       | 指生成的代理对象。                                           |
| Aspect（切面）      | 切入点和通知的结合。                                         |

![图片](../img/spring/11.2_1.jpg)



SpringAOP中，通过Advice定义横切逻辑，Spring中支持5种类型的Advice:

![图片](../img/spring/11.2_2.jpg)

即 Aop 在 不改变原有代码的情况下 , 去增加新的功能 .



### 11.3 使用Spring实现Aop

**【重点】使用AOP织入包，需要导入一个依赖包！**

```xml
<!-- https://mvnrepository.com/artifact/org.aspectj/aspectjweaver -->
<dependency>
   <groupId>org.aspectj</groupId>
   <artifactId>aspectjweaver</artifactId>
   <version>1.9.4</version>
</dependency>
```



#### 11.3.1 第一种方式：通过 Spring API 实现

首先编写我们的业务接口和实现类

```java
package com.ahulearn.service;

public interface UserService {
    public void add();
    public void delete();
    public void update();
    public void query();
}
```

```java
package com.ahulearn.service;

public class UserServiceImpl implements UserService {
    public void add() {
        System.out.println("增加用户");
    }

    public void delete() {
        System.out.println("删除用户");
    }

    public void update() {
        System.out.println("更新用户");
    }

    public void query() {
        System.out.println("查询用户");
    }
}
```

然后去写我们的增强类 , 我们编写两个 , 一个前置增强 一个后置增强

```java
package com.ahulearn.log;

import org.springframework.aop.MethodBeforeAdvice;
import java.lang.reflect.Method;

public class Log implements MethodBeforeAdvice {
    //method: 要执行的目标对象的方法
    //objects: args 参数
    //target: target 对象
    public void before(Method method, Object[] objects, Object target) throws Throwable {
        System.out.println(target.getClass().getName()+"的"+
                method.getClass().getName()+"被执行了");
    }
}
```



```java
package com.ahulearn.log;

import org.springframework.aop.AfterReturningAdvice;
import java.lang.reflect.Method;

public class AfterLog implements AfterReturningAdvice {
    //returnValue是返回值
    public void afterReturning(Object returnValue, Method method, Object[] args, Object target) throws Throwable {
        System.out.println(target.getClass().getName()+"的"+
                method.getClass().getName()+"执行,返回结果："+
                returnValue);
    }
}
```



最后去spring的文件中注册 , 并实现aop切入实现 , 注意导入约束 .

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd

       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--注册bean-->
    <bean id="userService" class="com.ahulearn.service.UserServiceImpl"/>
    <bean id="log" class="com.ahulearn.log.Log"/>
    <bean id="afterLog" class="com.ahulearn.log.AfterLog"/>
    <!--需要导入AOP的约束，配置AOP-->
    <aop:config>
        <!--切入点:pointcut; expression:表达式：execution(返回值类型 包名.类名.方法名(参数))
         * 通配符，前面指所有类型的方法，后面指所有方法，括号中两个点表示任意参数-->
        <aop:pointcut id="pointcut" expression="execution(* com.ahulearn.service.UserServiceImpl.*(..))"/>
        <!--设置切入方式: advice-ref执行方法 . pointcut-ref切入点-->
        <aop:advisor advice-ref="log" pointcut-ref="pointcut"/>
        <aop:advisor advice-ref="afterLog" pointcut-ref="pointcut"/>
    </aop:config>

</beans>
```



测试类

```java
import com.ahulearn.service.UserService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MyTest {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
        //注意动态代理是代理的接口
        UserService userService = context.getBean("userService", UserService.class);
        userService.add();
    }
}
```

Aop的重要性 : 很重要 . 一定要理解其中的思路 , 主要是思想的理解 .

Spring的Aop就是将公共的业务 (日志 , 安全等) 和领域业务结合起来 , 当执行领域业务时 , 将会把公共业务加进来 . 实现公共业务的重复利用 . 领域业务更纯粹 , 程序猿专注领域业务 , 其本质还是动态代理 . 



#### 11.3.2 第二种方式：自定义类来实现

目标业务类不变依旧是userServiceImpl

第一步 : 写我们自己的一个切入类

```java
package com.ahulearn.diy;

public class DiyPointCut {
    public void before() {
        System.out.println("==========方法执行前================");
    }

    public void after() {
        System.out.println("==========方法执行后================");
    }
}
```

去spring中配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd

       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--注册bean-->
    <bean id="userService" class="com.ahulearn.service.UserServiceImpl"/>
    <!--自定义切面类-->
    <bean id="diyadvisor" class="com.ahulearn.diy.DiyPointCut"/>
    <aop:config>
        <!--自定义切面，ref: 要引用的类-->
        <aop:aspect ref="diyadvisor">
            <!---切入点-->
            <aop:pointcut id="point" expression="execution(* com.ahulearn.service.UserServiceImpl.*(..))"/>
            <!--通知: 切面方法-->
            <aop:before method="before" pointcut-ref="point"/>
            <aop:after method="after" pointcut-ref="point"/>
        </aop:aspect>
    </aop:config>
</beans>
```

测试：

```java
import com.ahulearn.service.UserService;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MyTest {
    @Test
    public void diyPointCut() {
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        //注意动态代理是代理的接口
        UserService userService = context.getBean("userService", UserService.class);
        userService.add();
    }
}
```

#### 11.3.3 第三种方式: 注解实现

第一步：编写一个注解实现的增强类

```java
package com.ahulearn.diy;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Aspect;

//标记这是一个注解
@Aspect
public class AnnotationPointCut {
    //前置切面
    @Before("execution(* com.ahulearn.service.UserServiceImpl.*(..))")
    public void before() {
        System.out.println("************方法执行前************");
    }
    //前置切面
    @After("execution(* com.ahulearn.service.UserServiceImpl.*(..))")
    public void after() {
        System.out.println("************方法执行后************");
    }
    @Around("execution(* com.ahulearn.service.UserServiceImpl.*(..))")
    public void around(ProceedingJoinPoint jp) throws Throwable {
        System.out.println("环绕前");
        System.out.println("签名:"+jp.getSignature());
        //执行方法
        Object proceed = jp.proceed();

        System.out.println("环绕后");
    }
}
```

第二步：在Spring配置文件中，注册bean，并增加支持注解的配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd

       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--注册bean-->
    <bean id="userService" class="com.ahulearn.service.UserServiceImpl"/>
    <!--方式三-->
    <bean id="annotationPointCut" class="com.ahulearn.diy.AnnotationPointCut"/>
    <!--开启注解支持,默认JDK方式实现，下方设为true使用cglib方式-->
    <aop:aspectj-autoproxy proxy-target-class="false" />
</beans>
```

aop:aspectj-autoproxy：说明

通过aop命名空间的<aop:aspectj-autoproxy />声明自动为spring容器中那些配置@aspectJ切面的bean创建代理，织入切面。当然，spring 在内部依旧采用AnnotationAwareAspectJAutoProxyCreator进行自动代理的创建工作，但具体实现的细节已经被<aop:aspectj-autoproxy />隐藏起来了

<aop:aspectj-autoproxy />有一个proxy-target-class属性，默认为false，表示使用jdk动态代理织入增强，当配为<aop:aspectj-autoproxy  poxy-target-class="true"/>时，表示使用CGLib动态代理技术织入增强。不过即使proxy-target-class设置为false，如果目标类没有声明接口，则spring将自动使用CGLib动态代理。







## 12. 整合Mybatis

步骤：

1. 导入相关jar包
   + junit
   + mybatis
   + mysql数据库
   + spring相关
   + aop织入
   + mybatis-spring 【新包】

```xml
<dependencies>
    <!--mysql-connector-java,对应的dirver:com.mysql.jdbc.Driver-->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>5.1.45</version>
    </dependency>
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis</artifactId>
      <version>3.5.6</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>5.2.10.RELEASE</version>
    </dependency>
    <!-- spring操作数据库，需要spring-jdbc -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-jdbc</artifactId>
      <version>5.2.10.RELEASE</version>
    </dependency>
    <!-- aop织入包 -->
    <dependency>
      <groupId>org.aspectj</groupId>
      <artifactId>aspectjweaver</artifactId>
      <version>1.9.4</version>
    </dependency>
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis-spring</artifactId>
      <version>2.0.5</version>
    </dependency>
  </dependencies>
```

2. 编写配置文件

3. 测试

### 12.1 回顾mybatis

连接数据库：右侧边栏：Database打开数据库栏；+号点Data Source; 选择MySQL

![image-20210419192943451](../img/spring/12.1_0.png)

1. 编写实体类 User.java

```java
package com.ahulearn.pojo;

public class User {
    private int id;
    private String name;
    private String pwd;

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", pwd='" + pwd + '\'' +
                '}';
    }
}
```



2. 编写核心配置文件: mybatis-config.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<!--核心配置文件-->
<configuration>
    <typeAliases>
        <package name="com.ahulearn.pojo"/>
    </typeAliases>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/mybatis?useSSL=false&amp;serverTimezone=UTC"/>
                <property name="username" value="root"/>
                <property name="password" value="shenhuo"/>
            </dataSource>
        </environment>
    </environments>
    <!--每一个Mpapper.xml都需要在Mybatis核心配置文件中注册！-->
    <mappers>
        <!--resource方式，指定路径-->
        <!--<mapper resource="com/ahulearn/mapper/UserMapper.xml"/>-->
        <!--class方式，xml和class同名且放在同一个目录下-->
        <mapper class="com.ahulearn.mapper.UserMapper"/>
    </mappers>
</configuration>
```



3. 编写接口: UserMapper.java

```java
package com.ahulearn.mapper;

import com.ahulearn.pojo.User;
import java.util.List;

public interface UserMapper {
    public List<User> selectUser();
}
```



4. 编写指令配置：UserMapper.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!--namespace绑定一个对应的Dao/Mapper接口-->
<mapper namespace="com.ahulearn.mapper.UserMapper">
    <!--select查询语句
        id: 对应接口中的方法名
        返回结果: 完整路径类名, resultType，resultMap
    -->
    <select id="selectUser" resultType="user">
        select * from mybatis.user;
    </select>
</mapper>
```



5. 测试

```java
import com.ahulearn.mapper.UserMapper;
import com.ahulearn.pojo.User;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class MyTest {
    @Test
    public void test() throws IOException {
        String resource = "mybatis-config.xml";
        InputStream in = Resources.getResourceAsStream(resource);
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(in);
        SqlSession sqlSession = sessionFactory.openSession(true);

        UserMapper mapper = sqlSession.getMapper(UserMapper.class);
        List<User> userList = mapper.selectUser();
        for (User user : userList) {
            System.out.println(user);
        }
    }
}
```



### 12.2 Spring整合mybatis方式一

+ 保留上方回顾mybatis中的 `com.ahulearn.pojo.User`、`com.ahulearn.mapper.UserMapper`、`com.ahulearn.mapper.UserMapper.xml`



1. 配置数据源替换mybaits的数据源: `spring-mapper.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--DataSource: 这里使用Spring的数据源替换Mybatis配置，可以使用其他任意数据源：c3p0 dbcp druid-->
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
        <property name="url" value="jdbc:mysql://localhost:3306/mybatis?useSSL=false&amp;serverTimezone=UTC"/>
        <property name="username" value="root"/>
        <property name="password" value="shenhuo"/>
     </bean>
</beans>
```

原mybatis配置文件简化为下面的形式：`mybatis-config.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<!--核心配置文件-->
<configuration>
    <typeAliases>
        <package name="com.ahulearn.pojo"/>
    </typeAliases>
    <!--使用spring环境不需要再配置dataSource和mapper-->
</configuration>
```



2. sqlSessionFactory：beans.xml中

```xml
	<!--sqlSessionFactory: 工厂-->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource" />
        <!---绑定mybatis配置文件-->
        <property name="configLocation" value="classpath:mybatis-config.xml" />
        <!---相当于mybatis-config.xml中的mapper-->
        <property name="mapperLocations" value="classpath:com/ahulearn/mapper/*.xml"/>
    </bean>
```



3. sqlSessionTemplate：beans.xml中

```xml
 	<!--SqlSession模板-->
    <bean id="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
        <!--没有set方法，只能用构造器注入-->
        <constructor-arg index="0" ref="sqlSessionFactory"/>
    </bean>
```



4. 接口实现类: UserMapperImpl

```java
package com.ahulearn.mapper;

import com.ahulearn.pojo.User;
import org.mybatis.spring.SqlSessionTemplate;

import java.util.List;

public class UserMapperImpl implements UserMapper {
    //在原来所有操作，都使用sqlSession来执行；现在换成使用SqlSessionTemplate
    private SqlSessionTemplate sqlSession;
    public void setSqlSession(SqlSessionTemplate sqlSession) {
        this.sqlSession = sqlSession;
    }
    @Override
    public List<User> selectUser() {
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);
        return mapper.selectUser();
    }
}
```



5. 将实现类注入到Spring中

```xml
 	<!--注入接口实现类，执行的sql语句-->
    <bean id="userMapper" class="com.ahulearn.mapper.UserMapperImpl">
        <property name="sqlSession" ref="sqlSession"/>
    </bean>
```



6. 测试使用

```java
    //使用mybatis-spring
    @Test
    public void testSpring() throws IOException {
        ApplicationContext context = new ClassPathXmlApplicationContext("spring-mapper.xml");

        UserMapper userMapper = context.getBean("userMapper", UserMapper.class);
        List<User> userList = userMapper.selectUser();
        for (User user : userList) {
            System.out.println(user);
        }

    }
```



### 12.3 Spring整合mybatis方式二

1. 修改UserMapperImpl

```java
package com.ahulearn.mapper;

import com.ahulearn.pojo.User;
import org.apache.ibatis.session.SqlSession;
import org.mybatis.spring.support.SqlSessionDaoSupport;

import java.util.List;

public class UserMapperImpl2 extends SqlSessionDaoSupport implements UserMapper {
    public List<User> selectUser() {
        SqlSession sqlSession = getSqlSession();
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);
        return mapper.selectUser();
    }
}
```



2. 修改beans.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--DataSource: 使用Spring的数据源替换Mybatis配置，其他数据源：c3p0 dbcp druid-->
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
        <property name="url" value="jdbc:mysql://localhost:3306/mybatis?useSSL=false&amp;serverTimezone=UTC"/>
        <property name="username" value="root"/>
        <property name="password" value="shenhuo"/>
     </bean>

    <!--sqlSessionFactory: 工厂-->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource" />
        <!---绑定mybatis配置文件-->
        <property name="configLocation" value="classpath:mybatis-config.xml" />
        <!---相当于mybatis-config.xml中的mapper-->
        <property name="mapperLocations" value="classpath:com/ahulearn/mapper/*.xml"/>
    </bean>
    
    <!--不再需要注入sqlSessionTemplate，直接获取sqlSession-->
    <bean id="userMapper2" class="com.ahulearn.mapper.UserMapperImpl2">
        <!--配置sqlSessionFactory-->
        <property name="sqlSessionFactory" ref="sqlSessionFactory"/>
    </bean>

</beans>
```



3. 测试

```java
    @Test
    public void testSpring2(){
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        UserMapper mapper = (UserMapper) context.getBean("userMapper2");
        List<User> userList = mapper.selectUser();
        for (User user : userList) {
            System.out.println(user);
        }
    }
```



## 13. 声明式事务

### 1. 回顾事务

+ 把一组业务当成一个业务来做，要么都成功，要么失败
+ 事务在项目开发中，十分重要，涉及到数据的一致性问题！
+ 确保完整行和一致性

**事务四个属性ACID**

1. 原子性（atomicity）

2. - 事务是原子性操作，由一系列动作组成，事务的原子性确保动作要么全部完成，要么完全不起作用

3. 一致性（consistency）

4. - 一旦所有事务动作完成，事务就要被提交。数据和资源处于一种满足业务规则的一致性状态中

5. 隔离性（isolation）

6. - 可能多个事务会同时处理相同的数据，因此每个事务都应该与其他事务隔离开来，防止数据损坏

7. 持久性（durability）

8. - 事务一旦完成，无论系统发生什么错误，结果都不会受到影响。通常情况下，事务的结果被写到持久化存储器中

 

### 2. spring 中的事务管理

Spring在不同的事务管理API之上定义了一个抽象层，使得开发人员不必了解底层的事务管理API就可以使用Spring的事务管理机制。Spring支持编程式事务管理和声明式的事务管理。

**编程式事务管理**

- 将事务管理代码嵌到业务方法中来控制事务的提交和回滚
- 缺点：必须在每个事务操作业务逻辑中包含额外的事务管理代码

**声明式事务管理**

- 一般情况下比编程式事务好用。
- 将事务管理代码从业务方法中分离出来，以声明的方式来实现事务管理。
- 将事务管理作为横切关注点，通过aop方法模块化。Spring中通过Spring AOP框架支持声明式事务管理。

**使用Spring管理事务，注意头文件的约束导入 : tx**

```xml
xmlns:tx="http://www.springframework.org/schema/tx"

xsi:schemaLocation="http://www.springframework.org/schema/tx
http://www.springframework.org/schema/tx/spring-tx.xsd">
```

导入aop

```xml
xmlns:aop="http://www.springframework.org/schema/aop"
xsi:schemaLocation="http://www.springframework.org/schema/tx
   http://www.springframework.org/schema/tx/spring-tx.xsd"
```



**事务管理器**

- 无论使用Spring的哪种事务管理策略（编程式或者声明式）事务管理器都是必须的。
- 就是 Spring的核心事务管理抽象，管理封装了一组独立于技术的方法。

**JDBC事务**

```XML
<!--配置声明式事务-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource" />
</bean>
```

**配置好事务管理器后我们需要去配置事务的通知**

```XML
<!--配置事务通知-->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
   <tx:attributes>
       <!--配置哪些方法使用什么样的事务,配置事务的传播特性-->
       <tx:method name="add" propagation="REQUIRED"/>
       <tx:method name="delete" propagation="REQUIRED"/>
       <tx:method name="update" propagation="REQUIRED"/>
       <tx:method name="search*" propagation="REQUIRED"/>
       <tx:method name="get" read-only="true"/>
       <tx:method name="*" propagation="REQUIRED"/>
   </tx:attributes>
</tx:advice>
```

**spring事务传播特性：**

事务传播行为就是多个事务方法相互调用时，事务如何在这些方法间传播。spring支持7种事务传播行为：

- propagation_requierd：如果当前没有事务，就新建一个事务，如果已存在一个事务中，加入到这个事务中，这是最常见的选择。
- propagation_supports：支持当前事务，如果没有当前事务，就以非事务方法执行。
- propagation_mandatory：使用当前事务，如果没有当前事务，就抛出异常。
- propagation_required_new：新建事务，如果当前存在事务，把当前事务挂起。
- propagation_not_supported：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起。
- propagation_never：以非事务方式执行操作，如果当前事务存在则抛出异常。
- propagation_nested：如果当前存在事务，则在嵌套事务内执行。如果当前没有事务，则执行与propagation_required类似的操作

Spring 默认的事务传播行为是 PROPAGATION_REQUIRED，它适合于绝大多数的情况。

假设 ServiveX#methodX() 都工作在事务环境下（即都被 Spring 事务增强了），假设程序中存在如下的调用链：Service1#method1()->Service2#method2()->Service3#method3()，那么这 3 个服务类的 3 个方法通过 Spring 的事务传播机制都工作在同一个事务中。

就好比，我们刚才的几个方法存在调用，所以会被放在一组事务当中！



**配置AOP**

导入aop的头文件！

```XML
<!--配置aop织入事务-->
<aop:config>
    <aop:pointcut id="txPointcut" expression="execution(* com.ahulearn.mapper.*.*(..))"/>
    <aop:advisor advice-ref="txAdvice" pointcut-ref="txPointcut"/>
</aop:config>
```

**进行测试**

删掉刚才插入的数据，再次测试！

```java
@Test
public void test2(){
   ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
   UserMapper mapper = (UserMapper) context.getBean("userDao");
   List<User> user = mapper.selectUser();
   System.out.println(user);
}
```

为什么需要配置事务？

- 如果不配置，就需要我们手动提交控制事务；
- 事务在项目开发过程非常重要，涉及到数据的一致性的问题，不容马虎！