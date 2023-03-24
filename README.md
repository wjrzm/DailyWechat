# 微信每日早安推送

    要想实现此仓库功能需要修改少量代码，若未曾了解过Python请不要复刻仓库

![墨菲安全](https://s.murphysec.com/badge/fromann/DailyWechat.svg)
[本项目已通过**墨菲安全**检测](https://www.murphysec.com/p/fromann/DailyWechat)


## 开源协议 [GNU GPLv3](./LICENSE)

>[General Public License v3.0 ](./LICENSE)
允许个人使用、商业使用、专利授权，允许复制、分发、修改，并且作者不承担用户使用的一切后果。但是它有很多限制：
- 必须开源
一旦使用了这个协议，如果他人想要进行分发、修改，那么他们修改后的源代码也必须开源。这是开源的核心保障，如果没有这条规定，就没有人愿意持续公开自己的源码了。
- 保留协议和版权
保留对协议和版权的叙述。
- 不允许更换协议
一旦最原始的源码使用了GPL，其衍生的所有代码都必须使用GPL。这也是开源保障之一
- 声明变更
对于代码的变更需要有文档进行说明改了哪些地方。

## 正文
### 效果
<img src="https://raw.githubusercontent.com/wjrzm/PicGO/main/2022/202303241455930.jpg" style="zoom:50%;" />

### 思路
本项目实现单公众号对多用户发送模板信息
#### 使用GitHub Action进行部署
##### Secrets/Action Key表
将公众号的`APP_ID` , `APP_SECRET` , `Template_ID`填入Key表
![2](https://raw.githubusercontent.com/fromann/CDN/main/img/githubpic/sendcard/2.png)
##### 用户信息文件
用户信息文件储存于json文件中，实现用户信息的差异化储存，便于差异化分发

    开源平台也要保护好自己的名字资料
~~~json
{
  "data": [
    {
      "user_name": "用户1的名字",
      "user_id": "用户1的ID",
      "born_date": "用户1设置的起始日，已经过去的节日",
      "birthday": "用户1的生日",
      "setday": "用户1设置的倒数日，未来计划的节日",
      "city": "城市名",
      "district": "区名"
    },
    {
      "user_name": "用户2的名字",
      "user_id": "用户2的ID",
      "born_date": "用户2设置的起始日，已经过去的节日",
      "birthday": "用户2的生日",
      "setday": "用户2设置的倒数日，未来计划的节日",
      "city": "城市名",
      "district": "区名"
    }
    ]
}
~~~
以上是基本结构
若想新增用户可以按照以下格式花括号（`{}`）之间添加用`,`分割
~~~json
{
      "user_name": "用户2的名字",
      "user_id": "用户2的ID",
      "born_date": "用户2设置的起始日，已经过去的节日",
      "birthday": "用户2的生日",
      "setday": "用户2设置的倒数日，未来计划的节日",
      "city": "城市名",
      "district": "区名"
}
~~~

#### 使用GitLab CI/CD进行部署

由于GitHub相较于GitLab偏重于开源代码的共享，不适合进行一些个人信息以及用户密钥等信息的设置，所以计划用GitLab个人仓库进行部署。

##### 首先进入CI/CD中的编辑器

```yml
image: python:3.7

stages:          # List of stages for jobs, and their order of execution
  - build
  - deploy

build-job:       # This job runs in the build stage, which runs first.
  stage: build
  script:
    - echo "Compiling the code..."
    - echo "Compile complete."

deploy-job:      # This job runs in the deploy stage.
  stage: deploy  # It only runs when *both* jobs in the test stage complete successfully.
  environment: production
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed."
    - pip install -r ./requirements.txt && python ./main.py
```

然后进入`计划`模块，进行流水线计划的设定，循环周期`0 9 * * *`，第一位表示分钟，第二位表示小时，以此类推，此例表示每天上午九点进行流水线的执行，即`MoriningCard`的推送。

这样可以在配置文件中直接设置任何你想要的API密钥，包括一些很私密的个人信息。

#### 微信模板

~~~txt
{{time.DATA}}

坐标城市：{{city.DATA}}
当前天气：{{weather.DATA}}
当前风向：{{wind.DATA}}
今日温度：{{tem_low.DATA}}℃~{{tem_high.DATA}}℃ 
空气质量：{{air.DATA}}
紫外线强度：{{uv.DATA}}级

今天是我们恋爱第{{born_days.DATA}}天
距离宝贝生日还有{{birthday_left.DATA}}天
距离五一出游还有{{setday_left.DATA}}天

{{words.DATA}}
~~~
## 注意事项

- 生日的日期格式是：`05-20`，
- 纪念日的格式是 `2022-08-09`
- 由于个人微信公众号的个人认证需要粉丝量500以上，才可以使用模板分发的功能（本项目主要使用模板消息功能），所以个人用户可以在`开发者工具`->`公众平台测试账号`实现本功能

## 声明变更

- 修改`.github\workflows\main.yml`中的设定时间
- 修改`main.py`中的天气调用API，和密钥管理方式
- 修改`users_info.json`格式
- 修改README，新增解释
- 新增`Template.txt`
- 新增`.gitlab-ci.yml`
