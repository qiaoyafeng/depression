<template>
  <div>
    <el-container>
      <el-header>
        <img src="../../src/assets/image/logo_hxq.png" alt="logo"
          style=" width: 100px; float: left;margin-left: 20px;margin-top: 5px;" />
        <el-menu active-text-color="#7B8E69" :default-active="activeIndex" class="el-menu-demo" mode="horizontal"
          @select="handleSelect" router style="float: right;padding-right: 20px;">
          <el-submenu index="/mdd">
            <template slot="title" @click="init">抑郁症</template>
            <el-menu-item index="/Test" @click="change">抑郁症测试</el-menu-item>
            <el-menu-item index="/HistoryView">研判分析</el-menu-item>
          </el-submenu>

        </el-menu>
      </el-header>
      <el-main style="background-color: #F3E9DF;">
        <router-view />
      </el-main>
      <el-footer style="text-align: center;vertical-align: middle;line-height: 60px;font-size: 13px;">
        <span style="font-size: 10px;"></span>
      </el-footer>
    </el-container>
  </div>
</template>
<script>
  import axios from 'axios'
  export default {
    name: 'Home',
    data () {
      return {
        activeIndex: '1',
        id: this.GLOBAL.id
      };
    },
    created () {
      let router_path = this.$route.path
      // console.log(router_path)
      if (router_path != '/Introduction') {
        this.$router.replace({ path: '/Introduction' });
      }

    },
    methods: {
      handleSelect (key, keyPath) {
        this.activeIndex = keyPath[0]
      },
      change () {
        console.log(this.id)
        this.GLOBAL.id = 3
        this.GLOBAL.other_result_num = 0
        // var message = { 'username': 'lyy' }
        // axios.post('/name', message).then(function (result) {
        //   console.log(result)
        // }).catch(error => (console.log(error)))
        // console.log(this.GLOBAL.id)
      },
      init () {
        this.GLOBAL.id = 2
        this.GLOBAL.other_result_num = 0
      }
    }
  }
</script>

<style scoped>
  a {
    text-decoration: none;
  }

  .router-link-active {
    text-decoration: none;
  }
</style>