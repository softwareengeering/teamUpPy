// pages/request_join_more/request_join_more.js
var ifagree = 0;//0表示拒绝，1表示同意，2表示取消
var app=getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    apply_data: { id: 1, applyer: "某某某", team_id: "002", member: ["aaa", "hhh"], time: "2019-05-20 13:14", me: "me", class_name:"软工" }
  },
  interact: function (ifagree) {
    console.log('传入的消息id为：', app.globalData.apply_msg_id)
    wx.request({
      url: 'http://127.0.0.1:5000/applicationHandle',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'student_id': app.globalData.student_id,
        'apply_msg_id': app.globalData.apply_msg_id,  //记得后台要将其标为已读
        'option': ifagree
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res.data里面要有state、info、invite_data（页面主要数据），如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
        if (res.data.state == 1) { 
          wx.redirectTo({  //页面跳转
            url: '../request_join_list/request_join_list',
          })
        } else {
          wx.showToast({
            title: res.data.info
          });
        }
      }
    });
  },

  cancel: function (e) {
    ifagree = 2;
    this.interact(ifagree);
  },
  refuse: function (e) {
    ifagree = 0;
    this.interact(ifagree);
  },
  agree: function (e) {
    ifagree = 1;
    this.interact(ifagree);
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that=this;
    wx.request({
      url: 'http://127.0.0.1:5000/applicationDetail',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'apply_msg_id': app.globalData.apply_msg_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res.data里面要有state、info、invite_data（页面主要数据），如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
        console.log(res.data)
        if (res.data.state == 1) { //用php返回的数据更新页面数据
          console.log(res.data)
          that.setData({ apply_data: res.data.invite_data })//??????????
        } else {
          wx.showToast({
            title: res.data.info
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