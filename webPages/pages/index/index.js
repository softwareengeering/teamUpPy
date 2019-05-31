//index.js
//获取应用实例
const app = getApp()
const APP_ID = 'wx03fd479f09d68fba';//输入小程序appid  
const APP_SECRET = 'b40c24002ba08d9fc5b55a40ecc6df38';//输入小程序app_secret  
var OPEN_ID = '' //储存获取到openid  
var SESSION_KEY = ''//储存获取到session_key 
Page({
  data: {
    motto: 'Welcome！',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    var that = this;
    wx.login({
      success: function (res) {
        wx.request({
          //获取openid接口  
          url: 'https://api.weixin.qq.com/sns/jscode2session',
          data: {
            appid: APP_ID,
            secret: APP_SECRET,
            js_code: res.code,
            grant_type: 'authorization_code'
          },
          method: 'GET',
          success: function (res) {
            console.log('成功获取OPENID和SESSION_KEY',res.data)
            app.globalData.OPEN_ID = res.data.openid;//获取到的openid 
            OPEN_ID = app.globalData.OPEN_ID; 
            SESSION_KEY = res.data.session_key;//获取到session_key  
            console.log(OPEN_ID.length)
            console.log(SESSION_KEY.length)
            that.setData({
              openid: res.data.openid,
              session_key: res.data.session_key
            })
            wx.request({  //将openID等数据传回后台
              url: app.globalData.Base_url + '/login',//在这里加上后台的php地址
              data: { //发送给后台的数据
                'open_id': OPEN_ID,
                'session_key': SESSION_KEY
              },
              dataType: JSON,
              method: 'POST',
              header: {
                'Content-Type': 'application/json'
              },
              success: function (res) { //获取php的返回值res，res.data里面要有返回的数据信息，如果数据库中查到它还没有名字学号。那就跳转到login页面让它填写，如果有了，就跳转到它的列表页面，如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
                console.log(res);
                console.log(res.data.state)
                const data = JSON.parse(res.data)
                console.log( data )
                if (data.state == 1) { //用php返回的数据成功
                  console.log('>>>>>>>')
                  if (data.student_id != null) {
                    console.log('>>>>>>> student_id != NULL')
                    app.globalData.student_id = res.data.student_id;
                    wx.switchTab({  //页面跳转
                      url: '../class_list/class_list',
                    });
                  } else {
                    wx.navigateTo({  //页面跳转
                      url: '../login/login',
                    });
                  }
                } else {
                  wx.showToast({
                    title: data.info
                  });
                }
              }
            });
          }
        })
      }
    });

  },

  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
