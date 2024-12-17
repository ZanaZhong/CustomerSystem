<template>
  <div id="app">
    <!-- 美化的導覽列 -->
    <nav class="navbar">
      <div class="logo">My System</div>
      <div class="nav-links">
        <router-link to="/customers" class="nav-item">客戶頁面</router-link>
        <router-link to="/transactions" class="nav-item">交易頁面</router-link>
      </div>
    </nav>

    <!-- 頁面內容 -->
    <div class="content">
      <router-view /> <!-- 用來顯示當前路由對應的頁面 -->
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

body {
  background-color: #f5f6fa;
  color: #333;
  line-height: 1.6;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2f3640;
  padding: 10px 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.logo {
  color: #f5f6fa;
  font-size: 1.5em;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 15px;
}

.nav-item {
  text-decoration: none;
  color: #f5f6fa;
  font-weight: bold;
  padding: 8px 12px;
  transition: background-color 0.3s, color 0.3s;
  border-radius: 4px;
}

.nav-item:hover {
  background-color: #4cd137;
  color: #fff;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #ffffff;
  margin: 20px auto;
  width: 90%;
  max-width: 1200px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
