export default {

  install(Vue) {
    // 防止重复点击

    Vue.directive('preventReClick', {
      inserted(el, binding) {
        // console.log('binding-7', binding)
        el.addEventListener('click', (event) => {
          // 节流
          // console.log(event)
          // console.log(el)
          if (!el.disabled) {
            el.disabled = true
            setTimeout(() => {
              el.disabled = false
            }, binding.value || 1000)
          }
        })
      }

    })
  }

}

