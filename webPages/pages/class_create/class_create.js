// pages/class_create/class_create.js
var app=getApp(); //初始化它以使用app.js中的全局变量

Page({
  data: {
    class_id: 1 //随便放一个，后面onload的时候会用全局的class_id来修改
  },
  //表单提交
  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    var that = this
    wx.request({
      url: app.globalData.Base_url + '/class_create2',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_id': this.data.class_id,
        'class_name': e.detail.value.class_name,
        'class_teacher': e.detail.value.class_teacher,
        'team_size': e.detail.value.team_size,
        'class_intro': e.detail.value.class_intro,
        'class_pwd': e.detail.value.class_password,
        'class_creater': app.globalData.OPEN_ID //班级创建人信息
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        console.log(res.data.info + "res info")
        if (res.data.state == 1) {
          wx.showToast({   //弹窗提醒
            title: "班级创建成功",
            duration: 2000,
            mask: true,
            icon: 'success'
          });
          wx.switchTab({
            url: '../class_list/class_list',
          })
        } else {
          wx.showToast({
            title: "班级创建失败",
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
    var that = this
    wx.request({
      url: app.globalData.Base_url + '/class_create1',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'OPEN_ID': this.data.OPEN_ID,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //获取php的返回值res，res里面要有一个state和一个info，如果成功就在info里说成功，下面的弹窗会提醒。
        if (res.data.state == 1) {
          that.setData({class_id: res.data.class_last_id+1})
        } else {
          wx.showToast({
            title: "班级列表信息获取失败",
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