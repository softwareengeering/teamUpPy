// pages/request_join_set/request_join_set.js
var app=getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    apply_data: [{ id: 0, cap: "队长", team_id: "002", member: ["aaa", "hhh"], time: "2019-05-20 13:14", me: "me", read: true }, { id: 1, cap: "队长2", team_id: "003", member: ["rrr", "hhh"], time: "2019-05-20 13:17", me: "gaga", read: false }, { id: 2, cap: "队长4", team_id: "004", member: ["rrr", "hhh"], time: "2019-05-20 13:19", me: "gaaga", read: true }, { id: 3, cap: "队长2", team_id: "003", member: ["rrr", "hhh"], time: "2019-05-20 13:17", me: "gaga", read: false }],
    delete_msg_id_list: {}
  },

  // 获取多选框list中选中的值和对应的msg_id

  checkboxChange: function (e) {
    console.log('选中的有：', e.detail.value);
    this.data.delete_msg_id_list = e.detail.value
  },

  //提交表单
  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', this.data.delete_msg_id_list)
    wx.request({
      url: 'http://127.0.0.1:5000/applicationDelete',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'delete_msg_id_list': this.data.delete_msg_id_list,
        'student_id': app.globalData.student_id
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        if (res.data.state == 1) {
          wx.showToast({   //弹窗提醒
            title: "消息删除成功",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
          wx.switchTab({
            url: '../request_join_list/request_join_list',
          })
        } else {
          wx.showToast({
            title: "消息删除失败",
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
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/showJoinRequest',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'student_id': app.globalData.student_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res.data里面要有state、info、apply_data（页面主要数据），如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
        if (res.data.state == 1) { //用php返回的数据更新页面数据
          that.setData({ apply_data: res.data.apply_data })
        } else {
          wx.showToast({
            title: "加入申请信息读取失败",
            duration: 2000,
            mask: true,
            icon: 'loading'
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