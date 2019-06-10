// pages/class_set/class_set.js
var app=getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    class_id: 1,
    class_name:{},
    class_teacher:{},
    team_size:{},
    class_info:{},
    class_password:{}
  },

  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    wx.request({
      url: 'http://127.0.0.1:5000/create_class2 ',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_id': this.data.class_id,
        'class_name': e.detail.value.class_name,
        'class_teacher': e.detail.value.class_teacher,
        'team_size': e.detail.value.team_size,
        'class_intro': e.detail.value.class_intro,
        'class_creater': app.globalData.student_id, //班级创建人信息
        'class_password': e.detail.value.class_password  //班级管理密码
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        if (res.data.state == 1) {
          wx.showToast({   //弹窗提醒
            title: "班级信息修改成功",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
          wx.navigateTo({
            url: '../class_list/class_list',
          })
        } else {
          wx.showToast({
            title: "班级信息修改失败",
            duration: 2000,
            mask: true,
            icon: 'loading'
          });
        }
      }
    })
  },

  go_back: function(e){
    wx.navigateTo({
      url: '../class_list/class_list',
    })
  },

  delete_class: function(e){
    wx.request({
      url: 'http://127.0.0.1:5000/create_class2 ',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_id': app.globalData.class_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        if (res.data.state == 1) {
          wx.showToast({   //弹窗提醒
            title: "班级删除成功",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
          wx.navigateTo({
            url: '../class_list/class_list',
          })
        } else {
          wx.showToast({
            title: "班级删除失败",
            duration: 2000,
            mask: true,
            icon: 'loading'
          });
        }
      }
    })  
  },

  /**
   * 页面的初始数据
   */
  onLoad: function (options) {
    wx.request({
      url: 'http://127.0.0.1:5000/create_class1',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_id': app.globalData.class_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { 
        if (res.data.state == 1) {
          that.setData({ data:res.data.class })  //上来班级信息
        } else {
          wx.showToast({
            title: "班级数据获取失败",
            duration: 2000,
            mask: true,
            icon: 'loading'
          });
        }
      }
    })
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