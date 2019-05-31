// pages/class_download/class_download.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    wx.request({
      url: ' ',//在这里加上后台的php地址
      data: { //发送给后台的数据
        'class_password': e.detail.value.class_password,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) { //若验证通过，返回satus=1，允许下载文件
        if (res.data.state == 1) {
          wx.downloadFile({
            url: '', //所要下载文件的链接
            success: function (res) {
              // 只要服务器有响应数据，就会把响应内容写入文件并进入 success 回调，业务需要自行判断是否下载到了想要的内容
              console.log(res)
              if (res.statusCode === 200) {
                wx.showToast({  //弹窗提醒邀请码错误
                  title: "队伍信息表格下载成功"
                });               
              }
            }
          });
        } else {
          wx.showToast({  //弹窗提醒邀请码错误
            title: "邀请码错误"
          });
          wx.navigateTo({ //跳转到班级首页
            url: '../team_list/team_list',
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