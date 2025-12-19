# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bifrost is an iOS Business Modular Architecture (BMA) library that removes code dependencies between business modules using Router URLs and Remote APIs. The name comes from Norse mythology - a rainbow bridge connecting different realms.

**Key Concept**: Business modules have no code dependencies on each other, only on the Common and Mediator modules. This allows independent development and building of modules.

## Architecture

### Three-Layer Structure

1. **Business Modules** (Home, Shop, Sale, Goods)
   - Each module has two targets: static library for code + bundle for resources
   - Modules communicate via Mediator, never directly
   - Each module implements `BifrostModuleProtocol`

2. **Mediator Module**
   - Contains all `*ModuleService.h` protocol files
   - Defines public APIs and router URLs for each business module
   - Acts as the contract layer between modules

3. **Common Module**
   - Shared utilities and dependencies (YYModel, SigmaTableViewModel)
   - Used by all business modules

### Core Components

- **Bifrost Library** (`Bifrost/Lib/`): Core framework with two main features
  - `Bifrost.h`: Module registration and Remote API system
  - `Bifrost+Router.h`: URL routing system
  - `BifrostProtocol.h`: Module protocol definitions

## Development Commands

### Building the Demo

```bash
# Navigate to Demo directory
cd Demo

# Install dependencies
pod install

# Open workspace (required - do not open .xcodeproj directly)
open BifrostDemo.xcworkspace
```

Build the `BifrostDemo` scheme in Xcode.

### Running Module Quality Checks

```bash
# From project root, run the Swift script
cd Script
./module_check.swift
```

This script checks:
- ModuleService file synchronization across modules
- Duplicate .m/.mm files
- Duplicate .h files
- Version consistency in ModuleService protocols

## Key Patterns

### Module Registration

Modules register themselves in `+load` method:

```objective-c
@implementation GoodsModule

+ (void)load {
    BFRegister(GoodsModuleService);  // Macro: [Bifrost registerService:@protocol(GoodsModuleService) withModule:self.class]
}

+ (instancetype)sharedInstance {
    static GoodsModule *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
    });
    return instance;
}

- (void)setup {
    // Module initialization
}
```

### Router URL Binding

URLs are bound in `+load` method:

```objective-c
+ (void)load {
    [Bifrost bindURL:kRouteGoodsDetail toHandler:^id _Nullable(NSDictionary * _Nullable parameters) {
        GoodsDetailsViewController *vc = [[self alloc] init];
        vc.goodsId = parameters[kRouteGoodsDetailParamId];
        return vc;
    }];
}
```

URL invocation:

```objective-c
NSString *routeURL = BFStr(@"%@?%@=%@", kRouteGoodsDetail, kRouteGoodsDetailParamId, goods.goodsId);
UIViewController *vc = [Bifrost handleURL:routeURL];
```

### Remote API Usage

Calling another module's service:

```objective-c
id<GoodsProtocol> goods = [BFModule(GoodsModuleService) goodsById:item.goodsId];
// BFModule macro: ((id<GoodsModuleService>)[Bifrost moduleByService:@protocol(GoodsModuleService)])
```

### ModuleService Protocol Structure

Each `*ModuleService.h` file in Mediator contains:

```objective-c
///<v1.0>  // Semantic versioning: major.minor

#pragma mark - Notifications
// Module notification names

#pragma mark - URL routers
// Router URL constants and parameter keys
static NSString *const kRouteGoodsDetail = @"//goods/detail";
static NSString *const kRouteGoodsDetailParamId = @"id";

#pragma mark - Model Protocols
// Data model protocols for cross-module communication
@protocol GoodsProtocol <NSObject>
- (NSString*)goodsId;
- (NSString*)name;
@end

#pragma mark - Module Protocol
// Service methods exposed to other modules
@protocol GoodsModuleService <NSObject>
- (NSArray<id<GoodsProtocol>>*)allGoodsList;
@end
```

## Important Macros

- `BFRegister(service_protocol)`: Register module with service protocol
- `BFModule(service_protocol)`: Get module instance by service protocol
- `BFStr(fmt, ...)`: String formatting shorthand
- `BFComplete(Params, Result)`: Complete router handler with result

## Module Communication Rules

1. **Never import** business module headers directly in other business modules
2. **Only import** `*ModuleService.h` from Mediator module
3. **Use protocols** for all cross-module data models
4. **Router URLs** for navigation and simple parameter passing
5. **Remote APIs** for complex data exchange and method invocation

## CocoaPods Integration

The library is distributed via CocoaPods:

```ruby
pod 'Bifrost'
```

Source files: `Bifrost/Lib/*.{h,m}`

## Performance Notes

- Module registration in `+load` is lightweight (~60ms for 10,000 URLs + 100 modules)
- `[Bifrost setupAllModules]` should be called in `AppDelegate`'s `willFinishLaunchingWithOptions`
- Modules can implement `+setupModuleSynchronously` to control setup threading

## Version Management

ModuleService protocols use semantic versioning (x.y):
- **major (x)**: Breaking changes to public APIs
- **minor (y)**: New APIs added
- Versions < 1.0 are considered unstable

The `module_check.swift` script validates version consistency across copied ModuleService files.
