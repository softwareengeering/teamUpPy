// pages/team_list/team_list.js
var app=getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    class_info: {id: 69321, name: "面向对象程序设计", sup: 5, teams_count: 5},
    teams: []
  },
  //“设置”按钮的跳转
  navi: function(e){
    wx.navigateTo({
      url: '../class_password/class_password',
    })
  },
  //选择进入某个队伍的传参
  go_into_team: function(e) {
    app.globalData.team_id = e.currentTarget.dataset.teamid //这里等式右边只能用小写的标识符
    console.log('传入的队伍id为：', e.currentTarget.dataset.teamid)
    wx.navigateTo({  //页面跳转
      url: '../team_more/team_more',
    })
  },
  //管理班级信息页面的跳转
  navi: function(e){
    wx.navigateTo({
      url: '../class_password/class_password',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {  //页面加载时向后台请求数据
  var that = this
    wx.request({
      url:  app.globalData.Base_url + '/team_list',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_id': app.globalData.class_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res.data里面要有state、info、class_info,teams（页面主要数据），如果成功就在info里说成功，下面的弹窗会提醒,不成功给出错误信息info。
        if (res.data.state == 1) { //用php返回的数据更新页面数据
          that.setData({ class_info:res.data.class_info, teams:res.data.teams })
        } else {
          wx.showToast({
            title: "班级队伍信息加载失败",
            duration: 2000,
            mask:true,
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
    this.onload();
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