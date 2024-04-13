interface RouteRecordRawRebuild {
  path: string
  name: string
  component: () => Promise<any>
}

export interface RouteItem {
  googleIcon?: string
  name: string
  routeData: RouteRecordRawRebuild
}

// WebUI default routes
export const defaultRoutes: RouteItem[] = [
  {
    googleIcon: 'team_dashboard',
    name: '概览',
    routeData: {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard/DashboardIndex.vue')
    }
  },
  {
    googleIcon: 'extension',
    name: '拓展商店',
    routeData: {
      path: '/store',
      name: 'Store',
      component: () => import('@/views/Store/StoreIndex.vue')
    }
  },
  {
    googleIcon: 'settings',
    name: '实例设置',
    routeData: {
      path: '/settings',
      name: 'Settings',
      component: () => import('@/views/Settings/SettingsIndex.vue')
    }
  }
]
