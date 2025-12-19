# 08 - Demo项目解析

本章详细解析Bifrost Demo项目的结构和实现，帮助你理解实际项目中如何使用Bifrost。

## 📖 目录
- [Demo项目概述](#demo项目概述)
- [项目结构](#项目结构)
- [模块功能说明](#模块功能说明)
- [运行和调试](#运行和调试)
- [学习建议](#学习建议)

---

## Demo项目概述

Bifrost Demo是一个模拟电商应用的示例项目，展示了如何使用Bifrost实现业务模块化架构。

### 包含的模块

- **Home模块**：首页，展示商品推荐
- **Goods模块**：商品管理，提供商品列表和详情
- **Shop模块**：店铺管理
- **Sale模块**：销售管理，包含购物车功能
- **Common模块**：公共组件和工具类
- **Mediator模块**：中介层，定义所有模块的Service协议

---

## 项目结构

```
BifrostDemo/
├── App/                        # 主应用
│   └── App.xcodeproj
├── Modules/                    # 业务模块
│   ├── Home/                   # 首页模块
│   ├── Goods/                  # 商品模块
│   ├── Shop/                   # 店铺模块
│   ├── Sale/                   # 销售模块
│   ├── Common/                 # 公共模块
│   └── Mediator/               # 中介模块
├── Pods/                       # CocoaPods依赖
├── Podfile                     # CocoaPods配置
└── BifrostDemo.xcworkspace     # 工作空间
```

---

## 模块功能说明

### Home模块

**功能**：
- 展示首页
- 显示热卖商品
- 跳转到商品详情

**关键代码**：
```objective-c
// 跳转到商品详情
NSString *url = BFStr(@"%@?%@=%@", kRouteGoodsDetail, kRouteGoodsDetailParamId, goodsId);
UIViewController *vc = [Bifrost handleURL:url];
```

### Goods模块

**功能**：
- 提供商品列表
- 提供商品详情
- 提供商品查询API

**关键代码**：
```objective-c
// 实现GoodsModuleService协议
- (NSArray<id<GoodsProtocol>>*)allGoodsList {
    return [self.goodsCache copy];
}
```

### Sale模块

**功能**：
- 购物车管理
- 调用商品模块获取商品信息

**关键代码**：
```objective-c
// 调用商品模块
id<GoodsModuleService> goodsModule = BFModule(GoodsModuleService);
id<GoodsProtocol> goods = [goodsModule goodsById:goodsId];
```

---

## 运行和调试

### 运行步骤

1. **安装依赖**
```bash
cd Demo
pod install
```

2. **打开工作空间**
```bash
open BifrostDemo.xcworkspace
```

3. **选择scheme**
- 选择BifrostDemo scheme

4. **运行项目**
- 按Cmd+R运行

### 调试技巧

1. **查看模块注册**
```objective-c
// 在AppDelegate中打印所有注册的模块
NSArray *modules = [Bifrost allRegisteredModules];
NSLog(@"已注册的模块：%@", modules);
```

2. **调试Router URL**
```objective-c
// 检查URL是否可以处理
if ([Bifrost canHandleURL:url]) {
    NSLog(@"URL可以处理：%@", url);
} else {
    NSLog(@"URL无法处理：%@", url);
}
```

3. **调试Remote API**
```objective-c
// 检查模块是否存在
id<GoodsModuleService> goodsModule = BFModule(GoodsModuleService);
if (goodsModule) {
    NSLog(@"商品模块已注册");
} else {
    NSLog(@"商品模块未注册");
}
```

---

## 学习建议

### 学习路径

1. **理解项目结构**
   - 查看Podfile，了解模块依赖关系
   - 查看Mediator模块，了解Service协议定义

2. **学习模块实现**
   - 从Goods模块开始，学习Module类的实现
   - 学习如何实现Service协议
   - 学习如何注册Router URL

3. **学习模块调用**
   - 查看Sale模块，学习如何调用其他模块
   - 学习如何使用BFModule宏
   - 学习如何使用Router URL

4. **实践练习**
   - 尝试添加新的模块
   - 尝试添加新的Service方法
   - 尝试添加新的Router URL

### 关键文件

1. **Mediator模块**
   - `GoodsModuleService.h`：商品模块Service协议
   - `SaleModuleService.h`：销售模块Service协议
   - `HomeModuleService.h`：首页模块Service协议

2. **Goods模块**
   - `GoodsModule.m`：模块实现
   - `GoodsModel.m`：数据模型
   - `GoodsManager.m`：业务逻辑

3. **Sale模块**
   - `SaleModule.m`：模块实现
   - `ShoppingCartViewController.m`：购物车界面

---

## 小结

通过学习Demo项目，你应该掌握：

1. ✅ 如何组织Bifrost项目结构
2. ✅ 如何实现业务模块
3. ✅ 如何定义和实现Service协议
4. ✅ 如何使用Router URL和Remote API
5. ✅ 如何调试和测试模块

现在你可以开始在自己的项目中使用Bifrost了！

---

## 相关资源

- [Bifrost GitHub](https://github.com/youzan/Bifrost)
- [官方README](../README.md)
- [返回文档首页](./README.md)
