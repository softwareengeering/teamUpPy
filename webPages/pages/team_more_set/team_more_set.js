// pages/team_more_set/team_more_set.js
var app=getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    team: { id: 321, count: 3, sup: 5, leader: "张一一", info: "这是一个神秘的队伍这是一个神秘的队伍这是一个神秘的队伍这是一个神秘的队伍这是一个神秘的队伍", member: ["张一一", "张二二", "张三三"] },
  },
  //处理成员复选框的结果,注意这里得到的是成员名字
  checkboxChange: function (e) {
    console.log('选中的有：', e.detail.value);
    this.data.team.member = e.detail.value  
  },
  //提交修改后的表单
  formSubmit: function (e) {
    if (e.detail.value.leader_name == '') { //队长默认为创建人
      e.detail.value.leader_name = this.data.leader_name
    };
    console.log('form发生了submit事件，携带数据为：', e.detail.value, this.data.invitors)
    wx.request({
      url: ' ',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'leader_name': e.detail.value.leader_name,
        'team_info': e.detail.value.info,
        'team_members': this.data.team.members,
        'team_id': this.data.team.id,
        'team_sup': this.data.team.sup,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        if (res.data.state == 1) {
          wx.showToast({   //弹窗提醒
            title: "更改已提交",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
          wx.navigateTo({
            url: '../team_more/team_more',
          })
        } else {
          wx.showToast({
            title: "更改失败",
            duration: 2000,
            mask: true,
            icon: 'loading'
          });
        }
      }
    })
  },

  go_back: function (e) {
    wx.navigateTo({
      url: '../team_list/team_list',
    })
  },

  delete_team: function (e) {
    wx.request({
      url: 'http://127.0.0.1:5000/create_class2 ',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_id': app.globalData.class_id,
        'team_id': app.globalData.team_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        if (res.data.state == 1) {
          wx.showToast({   //弹窗提醒
            title: "队伍删除成功",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
          wx.navigateTo({
            url: '../team_list/team_list',
          })
        } else {
          wx.showToast({
            title: "队伍删除失败",
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
        'team_id': app.globalData.team_id,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        if (res.data.state == 1) {
          that.setData({ team: res.data.team })  //上来班级信息
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