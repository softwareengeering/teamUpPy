// pages/class_password/class_password.js
var app=getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  //表单提交
  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    wx.request({
      url: ' ',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_password': e.detail.value.class_password,
        'class_id': app.globalData.class_id
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        if (res.data.state == 1) {
          if (res.data.confirm == 1) {//confirm为1表明密码验证通过
            wx.navigateTo({
              url: '../class_set/class_set',
            })
          } else{
            wx.showToast({ //密码输入错误
              title: '班级管理密码输入错误',
              duration: 2000,
              mask: true,
              icon: 'loading'
            })
          }
        } else {
          wx.showToast({  //弹窗提醒错误
            title: "数据传输错误",
            duration: 2000,
            mask: true,
            icon: 'loading'
          });
        }
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
