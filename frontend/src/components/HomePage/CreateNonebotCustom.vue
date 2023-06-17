<template>
  <div class="modal" id="create-nonebot">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">创建/添加 NoneBot 实例</h3>
      <a href="#" class="btn btn-sm btn-circle absolute right-2 top-2">✕</a>

      <div class="custom-flex mt-4 p-8 w-full">
        <div class="flex flex-col justify-center">
          <div>没有 NoneBot 实例？</div>
          <a
            href="#create-nonebot-user"
            class="mt-2 btn btn-primary rounded-lg h-10 min-h-0 text-white"
            >创建一个！</a
          >
        </div>

        <div class="flex flex-col justify-center">
          <div>已有 NoneBot 实例？</div>
          <a class="mt-2 btn btn-primary rounded-lg h-10 min-h-0 text-white"
            >即刻添加！</a
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.custom-flex {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

@media screen and (max-width: 640px) {
  .custom-flex {
    flex-direction: column;
  }
}
</style>
