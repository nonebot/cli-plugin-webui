interface RouteInfo {
  name: string;
  path: string;
}

export interface RouteRecordRawRebuild extends RouteInfo {
  component: () => Promise<any>;
}

export interface NavItem {
  googleIcon?: string;
  name: string;
  routeData: RouteRecordRawRebuild;
}

// WebUI default routes
export const defaultRoutes: NavItem[] = [
  {
    googleIcon: "team_dashboard",
    name: "概览",
    routeData: {
      path: "/dashboard",
      name: "Dashboard",
      component: () => import("@/views/Dashboard/DashboardIndex.vue"),
    },
  },
  {
    googleIcon: "settings_applications",
    name: "实例操作",
    routeData: {
      path: "/operation",
      name: "Operation",
      component: () => import("@/views/Operation/OperationIndex.vue"),
    },
  },
  {
    googleIcon: "extension",
    name: "拓展商店",
    routeData: {
      path: "/store",
      name: "Store",
      component: () => import("@/views/Store/StoreIndex.vue"),
    },
  },
  {
    googleIcon: "settings",
    name: "实例设置",
    routeData: {
      path: "/settings",
      name: "Settings",
      component: () => import("@/views/Settings/SettingsIndex.vue"),
    },
  },
];
