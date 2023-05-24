<script lang="ts">
export default {
  data: () => {
    return {
      navList: [
        { tip: "主页", icon: "/svgs/home.svg", to: "/" },
        { tip: "插件列表", icon: "/svgs/package.svg", to: "/plugin" },
      ],
      activeNav: null as { tip: string; icon: string; to: string } | null,
    };
  },
  created() {
    const nowRoute = window.location.pathname;
    const activeNav = this.navList.find((navItem) => nowRoute === navItem.to);

    if (activeNav) {
      this.activeNav = activeNav;
    }
  },
  methods: {
    setActiveNav(item: { tip: string; icon: string; to: string }) {
      this.activeNav = item;
    },
  },
};
</script>

<template>
  <div class="side-nav">
    <ul class="menu bg-base-100">
      <div
        v-for="i in navList"
        :key="i.tip"
        :class="{
          'tooltip-active': i === activeNav,
          'tooltip tooltip-right': true,
        }"
        :data-tip="i.tip"
        @click="setActiveNav(i)"
      >
        <RouterLink :to="i.to">
          <li :class="{ bordered: i === activeNav }">
            <a
              :class="{
                'active-padding': i !== activeNav,
                'icon-padding': true,
              }"
            >
              <img class="side-nav-icon" :src="i.icon" />
            </a>
          </li>
        </RouterLink>
      </div>
    </ul>
  </div>
</template>

<style>
.side-nav
  .menu
  :where(li:not(.menu-title):not(:empty))
  > :where(*:not(ul):focus),
.side-nav
  .menu
  :where(li:not(.menu-title):not(:empty))
  > :where(*:not(ul):hover) {
  background-color: unset;
}

.side-nav .menu :where(li.bordered > *) {
  border-left-width: 2px;
}

.side-nav .menu .tooltip {
  background: hsl(var(--b2));
}

.active-padding {
  padding-left: calc(1rem - 11px) !important;
}

.tooltip-active {
  opacity: 1;
  background: hsl(var(--b1)) !important;
}

.side-nav {
  height: 100%;
  width: 55px;

  display: flex;
  flex-direction: column;
  align-items: center;

  background: hsl(var(--b2));
}

.side-nav-icon {
  height: 30px;
  width: 55px;

  opacity: 0.5;
}

.tooltip:hover .side-nav-icon,
.tooltip-active .side-nav-icon {
  opacity: 1;
}

.icon-padding {
  padding-left: calc(1rem - 13px);
  padding-right: calc(1rem - 9px);
}
</style>
