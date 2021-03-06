// pages/myindex/myindex.js
var app=getApp();

Page({
  /**
   * 页面的初始数据
   */
  data: {
    user:{}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.request({
      url: app.globalData.Base_url + '/get_user_info',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'student_id': app.globalData.student_id,
        'open_id': app.globalData.OPEN_ID
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res.data里面要有state、info、student_info等，如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
        console.log('>>>>>>>>>> myindex success')
        if (res.data.state == 1) { //用php返回的数据更新页面数据
          console.log(res.data.student_info)
          that.setData({ user: res.data.student_info})
          app.globalData.user_name = res.data.student_info.name
          app.globalData.user_id = res.data.student_info.id
        } else {
          wx.showToast({
            title: "我的信息加载失败",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
        }
      }
    });
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