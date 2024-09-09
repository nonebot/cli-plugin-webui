import { defineStore } from 'pinia'
import { ref } from 'vue'
import router from '@/router'

export interface RouteRecordRawRebuild {
  name?: string
  path: string
  component: () => Promise<any>
  children?: RouteRecordRawRebuild[]
}

export interface NavItem {
  googleIcon?: string
  name: string
  enabled?: boolean
  routeData?: RouteRecordRawRebuild[]
}

export const useNavStore = defineStore('navStore', () => {
  const navItems = ref<NavItem[]>([])

  const checkRouteItem = (routeItem: RouteRecordRawRebuild) => {
    routeItem.children?.forEach((child) => {
      child.children?.forEach((child) => {
        if (child.children) {
          throw new Error('至多支持两层路由嵌套')
        }
      })
    })
  }

  const addNavItem = (navItem: NavItem) => {
    const index = navItems.value.findIndex((item) => item.name === navItem.name)
    if (index !== -1) {
      throw new Error('已经存在同名的导航项')
    }

    navItem.routeData?.forEach((routeItem) => {
      checkRouteItem(routeItem)
    })

    navItem.routeData?.forEach((routeItem) => {
      router.addRoute('WebUI', routeItem)
    })

    navItems.value.push(navItem)
  }

  const removeNavItem = (navItem: NavItem) => {
    const index = navItems.value.findIndex((item) => item.name === navItem.name)
    if (index === -1) {
      return
    }

    navItems.value.splice(index, 1)
    router.removeRoute(navItem.name)
  }

  const addRouteItemToNav = (navItemName: string, routeItem: RouteRecordRawRebuild) => {
    checkRouteItem(routeItem)

    for (const nav in navItems.value) {
      const data = navItems.value[nav]
      if (data.name !== navItemName) {
        continue
      }

      data.routeData?.forEach((route) => {
        if (route.name === routeItem.name) {
          throw new Error('已经存在同名的路由')
        }
        route.children?.forEach((child) => {
          if (child.name === routeItem.name) {
            throw new Error('已经存在同名的路由')
          }
        })
      })

      data.routeData = data.routeData ?? []
      data.routeData?.push(routeItem)
      router.addRoute('WebUI', routeItem)
    }
  }

  const removeRouteItemFromNav = (navItem: NavItem, routeItem: RouteRecordRawRebuild) => {
    navItems.value.forEach((item) => {
      if (item.name === navItem.name) {
        const index = item.routeData?.findIndex((route) => route.name === routeItem.name) ?? -1
        if (index !== -1) {
          item.routeData?.splice(index, 1)
          router.removeRoute(routeItem.name ?? '')
        }
      }
    })
  }

  const addRouteChildItem = (targetRouteName: string, routeItem: RouteRecordRawRebuild) => {
    // TODO: 实现需要优化

    const navItemsCopy: NavItem[] = JSON.parse(JSON.stringify(navItems.value))
    navItemsCopy.forEach((item) => {
      item.routeData?.forEach((route) => {
        if (route.name === targetRouteName) {
          route.children?.push(routeItem)
        } else {
          route.children?.forEach((child) => {
            if (child.name === targetRouteName) {
              child.children?.push(routeItem)
            }
          })
        }
      })
    })

    checkRouteItem(routeItem)

    navItems.value.forEach((item) => {
      item.routeData?.forEach((route) => {
        if (route.name === targetRouteName) {
          route.children?.push(routeItem)
          router.addRoute(route.name, routeItem)
        } else {
          route.children?.forEach((child) => {
            if (child.name === targetRouteName) {
              child.children?.push(routeItem)
              router.addRoute(child.name, routeItem)
            }
          })
        }
      })
    })
  }

  const removeRouteChildItem = (targetRouteName: string) => {
    navItems.value.forEach((item) => {
      item.routeData?.filter((route) => route.name === targetRouteName)
    })
  }

  return {
    navItems,
    addNavItem,
    removeNavItem,
    addRouteItemToNav,
    removeRouteItemFromNav,
    addRouteChildItem,
    removeRouteChildItem
  }
})
