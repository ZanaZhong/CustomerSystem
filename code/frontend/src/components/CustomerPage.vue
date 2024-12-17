<template>
  <div class="customer-page">
    <!-- 標題 -->
    <h1>客戶資料</h1>

    <!-- 新增客戶表單 -->
    <div class="form-section">
      <h2>新增客戶</h2>
      <form @submit.prevent="submitNewCustomer" class="form">
        <div class="form-group">
          <label for="name">名稱</label>
          <input type="text" id="name" v-model="newCustomer.name" required />
        </div>
        <div class="form-group">
          <label for="email">電子郵件</label>
          <input type="email" id="email" v-model="newCustomer.email" required />
        </div>
        <button type="submit" class="btn btn-primary">新增客戶</button>
      </form>
    </div>

    <!-- 客戶表格 -->
    <div class="table-section">
      <table class="customer-table">
        <thead>
          <tr>
            <th>客戶名稱</th>
            <th>電子郵件</th>
            <th>去年總交易金額</th>
            <th>/</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(customer, index) in customers" :key="customer.id">
            <!-- 編輯模式：只允許更動 "名稱" 和 "電子郵件" -->
            <template v-if="editingIndex === index">
              <td>
                <input
                  type="text"
                  v-model="editingCustomer.name"
                  class="form-control"
                  placeholder="名稱"
                />
              </td>
              <td>
                <input
                  type="email"
                  v-model="editingCustomer.email"
                  class="form-control"
                  placeholder="電子郵件"
                />
              </td>
              <!-- 唯讀欄位 -->
              <td>
                <span>{{ customer.total_amount_last_year }}</span>
              </td>
              <td>
                <button
                  @click="submitUpdate(index)"
                  :disabled="isUpdating"
                  class="btn btn-success btn-sm"
                >
                  {{ isUpdating ? "更新中..." : "儲存" }}
                </button>
                <button
                  @click="cancelEdit"
                  :disabled="isUpdating"
                  class="btn btn-secondary btn-sm"
                >
                  取消
                </button>
              </td>
            </template>

            <!-- 預設顯示模式 -->
            <template v-else>
              <td>{{ customer.name }}</td>
              <td>{{ customer.email }}</td>
              <td>{{ customer.total_amount_last_year }}</td>
              <td>
                <button
                  @click="editCustomer(index, customer)"
                  class="btn btn-warning btn-sm"
                >
                  編輯
                </button>
              </td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      customers: [],
      newCustomer: {
        name: "",
        email: "",
      },
      editingCustomer: null,
      editingIndex: null,
      isUpdating: false,
    };
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      try {
        const response = await axios.get("http://localhost:8888/customers");
        this.customers = response.data;
      } catch (error) {
        console.error("無法取得客戶資料", error);
      }
    },

    async submitNewCustomer() {
      try {
        await axios.post("http://localhost:8888/customers", this.newCustomer);
        await this.fetchCustomers();
        alert("新增成功！");
        this.newCustomer = { name: "", email: "" };
      } catch (error) {
        console.error("新增失敗", error);
        alert("新增失敗");
      }
    },

    editCustomer(index, customer) {
      this.editingIndex = index;
      this.editingCustomer = { ...customer };
    },

    async submitUpdate() {
      this.isUpdating = true;
      try {
        await axios.put(
          `http://localhost:8888/customers/${this.editingCustomer.id}`,
          this.editingCustomer
        );
        await this.fetchCustomers();
        alert("更新成功！");
        this.editingCustomer = null;
        this.editingIndex = null;
      } catch (error) {
        console.error("更新失敗", error);
      } finally {
        this.isUpdating = false;
      }
    },

    // 取消編輯
    cancelEdit() {
      this.editingIndex = null;
      this.editingCustomer = null;
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Arial", sans-serif;
}

.customer-page {
  background-color: #f4f6f8;
  padding: 20px;
}

h1,
h2,
h3 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 10px;
}

/* 表單區塊 */
.form-section {
  background-color: #ffffff;
  padding: 20px;
  margin: 20px auto;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #34495e;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  border-color: #3498db;
  outline: none;
}

/* 按鈕樣式 */
.btn {
  padding: 8px 16px;
  margin: 0px 2px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.btn-success {
  background-color: #2ecc71;
  color: #fff;
}

.btn-success:hover {
  background-color: #27ae60;
}

.btn-primary {
  background-color: #3498db;
  color: #fff;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #f39c12;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #e67e22;
}

.btn-warning {
  background-color: #e74c3c; /* 警告紅色 */
  color: #fff;
}

.btn-warning:hover {
  background-color: #c0392b;
}

/* 禁用按鈕樣式 */
.btn:disabled {
  background-color: #d3d3d3;
  cursor: not-allowed;
  color: #fff;
}

/* 表格區塊 */
.table-section {
  margin: 20px auto;
  max-width: 1000px;
}

.customer-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.customer-table th,
.customer-table td {
  padding: 10px 15px;
  border: 1px solid #ddd;
  text-align: center;
}

.customer-table th {
  background-color: #2c3e50;
  color: #ffffff;
}

.customer-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.customer-table tr:hover {
  background-color: #f1f1f1;
}
</style>
