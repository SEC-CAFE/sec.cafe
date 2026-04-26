import wechatPayImg from '../images/wechatpay.jpg'
import alipayImg from '../images/alipay.jpg'
import noLogoImg from '../images/no_logo.jpg'

export default {
  intro: [
    '如果你有想法，欢迎提出你的建议或参与到这个项目。',
    '你也可以选择打赏该项目(直接扫描打赏)，帮助该项目持续运营下去；或者成为我们的赞助商，我们将在首页右侧挂上您的Logo。'
  ],
  qrcodes: [
    { id: 1, label: '微信', src: wechatPayImg, width: 100 },
    { id: 2, label: '支付宝', src: alipayImg, width: 100 }
  ],
  patreonUrl: 'https://www.patreon.com/user?u=93897763',
  sponsors: [
    {
      name: 'O*t',
      price: 188.88,
      comment: '赞助商要求：把赞助商的名字挂在上面(要挂什么名字请联系我哈，用打赏账号加我微信fooying)',
      time: '2024-11-15'
    },
    { name: '*夏', price: 66, comment: '', time: '2024-09-24' },
    { name: 'l*g', price: 5, comment: '', time: '2024-09-23' },
    { name: 'H*y', price: 9.9, comment: '奖励一杯瑞幸咖啡☕️', time: '2024-06-13' },
    { name: 'fs12', price: 5, comment: '', time: '2024-06-04' },
    { name: 'xidd', price: 50, comment: 'ai知识库不错', time: '2024-05-12' },
    { name: '匿名', price: 20, comment: '', time: '2023-05-01' },
    { name: 'w', price: 100, comment: '不错的项目', time: '2023-04-28' }
  ],
  yearlySponsors: [
    { name: 'Sponsor-1', href: '/about', logo: noLogoImg },
    { name: 'Sponsor-2', href: '/about', logo: noLogoImg }
  ]
}
