 // pages/request_join_list/request_join_lixt.js
var app=getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    apply_data: [{ id: 1, applyer: "某某某", team_id: "002", member: ["aaa", "hhh"], time: "2019-05-20 13:14", me: "me", class_name: "软工" ,read:true}, { id: 1, applyer: "某某某", team_id: "002", member: ["aaa", "hhh"], time: "2019-05-20 13:14", me: "me", class_name: "软工" ,read:false}, { id: 1, applyer: "某某某", team_id: "002", member: ["aaa", "hhh"], time: "2019-05-20 13:14", me: "me", class_name: "软工",read:true }]
  },
  //进入某条消息详情
  read_more: function (e) {
    console.log('in>>>>>>>>>>>>>>>>>')
    app.globalData.apply_msg_id = e.currentTarget.dataset.msg_id //修改公共的msg_id值
    console.log('传入的消息id为：', e.currentTarget.dataset.msg_id)
    wx.switchTab({  //页面跳转
      url: '../request_join_more/request_join_more',
    })
  },
  //跳转至管理消息页面
  manage: function(e){
    wx.navigateTo({
      url: '../request_join_set/request_join_set',
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
         // const data = JSON.parse(res.data)
          console.log(res.data)
          that.setData({ apply_data: res.data.apply_data })
          console.log('see applydata', that.data.apply_data)
          
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