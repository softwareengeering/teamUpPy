 // pages/myindex_set/myindex_set.js
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    user: { name:'', id: ''  }
  },

  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value,this.data.user.id,this.data.user.name)
    if (this.data.user.name !== app.globalData.User_name || this.data.user.name !== app.globalData.student_id  ){
      this.data.user.name = app.globalData.User_name
      this.data.user.name = app.globalData.student_id
      console.log('submitting ..... ')
      var that = this
      wx.request({
        url: app.globalData.Base_url + '/modifyName',//在这里加上后台的php地址
        data: { //发送给后台的数据
          'student_name': e.detail.value.student_name,
          'student_id': e.detail.value.student_id,
          'open_id': app.globalData.OPEN_ID
        },
        method: 'POST',
        header: {
          'Content-Type': 'application/json'
        },
        success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒,不成功给出原因的info返回，比如邀请码错误。
          if (res.data.state == 1) {
            app.globalData.student_id = e.detail.value.student_id;  //更新全局变量中的class_id
            app.globalData.User_name = e.detail.value.student_name;
            

            wx.switchTab({ //跳转到我的资料页
              url: '../class_list/class_list',
            });
          } else {
            wx.showToast({  //弹窗提醒邀请码错误
	            title: "信息错误",
	            duration: 2000,
	            mask: true,
	            icon: 'loading'
            });
          }
        }
      })
    };
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.data.user.name = app.globalData.user_name
    this.data.user.id = app.globalData.user_id
    wx.request({
      url: app.globalData.Base_url + '/get_user_info',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'open_id': app.globalData.OPEN_ID,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res.data里面要有state、info、student_info等，如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
        if (res.data.state == 1) { //用php返回的数据更新页面数据
          this.setData({ user: res.data.student_info })
        } else {
          wx.showToast({
            title: "我的信息加载失败",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
        }
      }
    })
    // wx.request({
    //   url: ' ',//在这里加上后台的php地址
    //   data: { //发送给后台的数据
    //     'student_id': app.globalData.student_id,
    //   },
    //   method: 'POST',
    //   header: {
    //     'Content-Type': 'application/x-www-form-urlencoded'
    //   },
    //   success: function (res) { //获取php的返回值res，res.data里面要有state、info、student_info等，如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
    //     if (res.data.state == 1) { //用php返回的数据更新页面数据
    //       this.setData({ user: res.data.student_info })
    //     } else {
    //       wx.showToast({
    //         title: res.data.info
    //       });
    //     }
    //   }
    // });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.onLoad()
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})